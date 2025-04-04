import datetime
import io
import logging
import os
from typing import Dict, List
from venv import logger

import requests
from PIL import Image
from markdown import markdown
from openai import OpenAI
from slugify import slugify

from libs import config
from libs.config import create_session
from libs.db_models import Extract, Newsletter, NewsletterConfig, Source, LLMConfig
from libs.extractors.ExtractorABC import ExtractorABC
from libs.extractors.extractors_config import extractors_config
from libs.openai_chat import chat
from libs.s3_helper import upload_file_from_url, upload_from_bytes


def generate_newsletter():
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with create_session() as session:
        # Get all newsletter configs
        newsletter_configs = session.query(NewsletterConfig).all()

        # Get all sources
        sources = session.query(Source).all()

        for idx, newsletter_config in enumerate(newsletter_configs):
            logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generating newsletter...")
            # Get the last newsletter date for this config
            last_newsletter = (
                session.query(Newsletter)
                .filter(Newsletter.newsletter_config_id == newsletter_config.id)
                .order_by(Newsletter.created_at.desc())
                .first()
            )
            last_newsletter_date = (
                last_newsletter.created_at.date() if last_newsletter else None
            )

            # Get all extracts since last newsletter (filter only if last_newsletter_date is not None)
            # Order by content_date asc
            extracts = (
                session.query(Extract)
                .join(Extract.source) # Join using the relationship attribute
                # Filter based on the Source model's relationship
                .filter(Source.newsletter_configs.any(NewsletterConfig.id == newsletter_config.id))
                .filter(
                    Extract.content_date > last_newsletter_date
                    if last_newsletter_date
                    else True
                )
                .order_by(Extract.content_date.asc())
                .all()
            )

            # Group by Source
            grouped_extracts: Dict[int, List[Extract]] = {}
            for extract in extracts:
                if extract.source.id not in grouped_extracts:
                    grouped_extracts[extract.source.id] = []
                grouped_extracts[extract.source.id].append(extract)

            # For each source, convert to text with the extractor
            source_texts_list = {}
            for source_id, source_extracts in grouped_extracts.items():
                source: Source = session.get(Source, source_id)
                extractor = extractors_config[source.type]["extractor_class"]
                extractor_instance: ExtractorABC = extractor()
                for row in source_extracts:
                    # Convert each extract to text
                    text = extractor_instance.row_to_string(row.content)
                    # Append to the source text
                    if source.id not in source_texts_list:
                        source_texts_list[source.id] = []
                    source_texts_list[source.id].append(text)

            # Merge the texts for each source
            source_text_str = []
            for source_id, texts in source_texts_list.items():
                source = next(s for s in sources if s.id == source_id)
                source_text_str.append(f"# {source.name}\n\n{'\n'.join(texts)}")

            # Concatenate the texts for each source
            source_text = "\n\n---\n\n".join(source_text_str)

            # Get the LLM config for this newsletter
            llm_config = session.get(LLMConfig, newsletter_config.llm_config_id)

            response = chat(
                prompt=source_text,
                system_prompt=llm_config.system_prompt,
                model=llm_config.model_name,
                base_url=llm_config.base_url,
                api_key=os.environ[llm_config.api_key_name],
                openai_chat_kwargs=llm_config.params,
            )

            response_markdown = response.choices[0].message.content

            # Convert to HTML
            response_html = markdown(response_markdown)

            today_str = datetime.date.today().strftime("%Y-%m-%d")

            # Generate a title for the newsletter
            logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generating newsletter title...")
            title_response = chat(
                prompt=response_markdown,
                system_prompt="Generate a title for this newsletter that I can use for my Blog. Give me only the title and nothing else.",
                model="gpt-4o",
                base_url="https://api.openai.com/v1",
                api_key=os.environ["OPENAI_API_KEY"],
                openai_chat_kwargs={},
            )
            title = title_response.choices[0].message.content.strip('"')
            logger.info(f"{newsletter_config} | Generated title: {title}")
            title_slug = slugify(title)

            # Generate an image from the newsletter
            logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generating newsletter image...")
            image_prompt_response = chat(
                prompt=response_markdown,
                system_prompt="Generate a prompt for DALLE3 to create an image for this newsletter that I can use for my Blog. Give me only the prompt and nothing else.",
                model="gpt-4o",
                base_url="https://api.openai.com/v1",
                api_key=os.environ["OPENAI_API_KEY"],
                openai_chat_kwargs={},
            )
            image_prompt = image_prompt_response.choices[0].message.content.strip('"')
            image_response = openai_client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1792x1024",
                quality="hd",
                n=1,
            )
            image_url = image_response.data[0].url

            # Convert image to webp format
            response = requests.get(image_url)
            response.raise_for_status()

            original_image_bytes = io.BytesIO(response.content)
            img = Image.open(original_image_bytes)
            webp_buffer = io.BytesIO()
            img.save(webp_buffer, format="WEBP")
            webp_buffer.seek(0)
            image_bytes = webp_buffer.getvalue()


            image_url = upload_from_bytes(
                image_bytes=image_bytes,
                bucket_name=config.CUSTOM_AWS_BUCKET_NAME,
                s3_key=f"generated-image/{newsletter_config.slug}/{today_str}/{title_slug}.png",
                extra={
                    "ACL": "public-read",
                    "ContentType": "image/webp",
                },
            )
            logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generated image: {image_url}")


            # Save the newsletter
            newsletter = Newsletter(
                base_url=llm_config.base_url,
                model_name=llm_config.model_name,
                params=llm_config.params,
                system_prompt=llm_config.system_prompt,
                input_text=source_text,
                output_markdown=response_markdown,
                output_html=response_html,
                newsletter_config_id=newsletter_config.id,
                title=title,
                slug=title_slug,
                image_url=image_url,
            )

            session.add(newsletter)
            session.commit()

if __name__ == "__main__":
    r = generate_newsletter()
