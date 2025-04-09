import datetime
import io
import logging
import os
from typing import Dict, List, Tuple

import requests
from PIL import Image
from openai import OpenAI
from slugify import slugify
from sqlalchemy import and_

from libs import config
from libs.config import create_session
from libs.db_models import Extract, Newsletter, NewsletterConfig, Source, LLMConfig
from libs.extractors.ExtractorABC import ExtractorABC
from libs.extractors.extractors_config import extractors_config
from libs.openai_chat import chat
from libs.s3_helper import upload_file_from_url, upload_from_bytes


def get_dates_boundaries(newsletter_config: NewsletterConfig, nb_days: int =3) -> List[Tuple[datetime.datetime, datetime.datetime]]:
    """
    Get a list of start and end dates for the newsletters.
    Each element must be maximum 3 days apart.
    If the last newsletter date is newer than 3 days ago, no dates are returned.
    """
    with create_session() as session:
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

        # Get the first extract date since the last newsletter
        first_extract = (
            session.query(Extract)
            .join(Extract.source)  # Join using the relationship attribute
            # Filter based on the Source model's relationship
            .filter(
                and_(
                    Source.newsletter_configs.any(NewsletterConfig.id == newsletter_config.id),
                    Extract.content_date > last_newsletter_date if last_newsletter_date else True,
                )
            )
            .order_by(Extract.content_date.asc())
            .first()
        )
        first_extract_date = first_extract.content_date

        # Get the last extract date for this config
        last_extract = (
            session.query(Extract)
            .join(Extract.source)  # Join using the relationship attribute
            # Filter based on the Source model's relationship
            .filter(Source.newsletter_configs.any(NewsletterConfig.id == newsletter_config.id))
            .order_by(Extract.content_date.desc())
            .first()
        )
        last_extract_date = last_extract.content_date

        # Make groups of nb_days
        dates_boundaries = []
        # if first_extract_date:
        # Check if the last newsletter date is newer than 3 days ago
        if (last_extract_date - first_extract_date).days > nb_days:
            # Create a list of dates from first_extract_date to last_extract_date
            current_date = first_extract_date
            while current_date < last_extract_date:
                start_date = current_date
                end_date = min(current_date + datetime.timedelta(days=nb_days), last_extract_date)
                dates_boundaries.append((start_date, end_date))
                current_date = end_date

        # Remove duplicates
        dates_boundaries = list(set(dates_boundaries))

        # Sort by start date
        dates_boundaries.sort(key=lambda x: x[0])

        # Remove dates range if it's less than 3 days
        dates_boundaries = [
            (start_date, end_date)
            for start_date, end_date in dates_boundaries
            if (end_date - start_date).days >= nb_days
        ]


    return dates_boundaries

def generate_newsletter():
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with create_session() as session:
        # Get all newsletter configs
        newsletter_configs = session.query(NewsletterConfig).all()

        # Get all sources
        sources = session.query(Source).all()

        for idx, newsletter_config in enumerate(newsletter_configs):
            dates_boundaries = get_dates_boundaries(newsletter_config)
            print(f"Dates boundaries for {newsletter_config}:")
            for start_date, end_date in dates_boundaries:
                print(f"  {start_date} - {end_date}")
            # continue
            for start_date, end_date in dates_boundaries:
                logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generating newsletter between {start_date} and {end_date}...")

                # Get all extracts between start_date and end_date
                # Order by content_date asc
                extracts = (
                    session.query(Extract)
                    .join(Extract.source) # Join using the relationship attribute
                    # Filter based on the Source model's relationship
                    .filter(Source.newsletter_configs.any(NewsletterConfig.id == newsletter_config.id))
                    .filter(
                        and_(
                            Extract.content_date > start_date,
                            Extract.content_date <= end_date,
                        )
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

                today_str = datetime.date.today().strftime("%Y-%m-%d")

                # Generate a title for the newsletter
                logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generating newsletter title...")
                title_response = chat(
                    prompt=response_markdown,
                    system_prompt="Generate a title for this newsletter that I can use for my Blog. Give me only the title and nothing else. The title must not contains any quotes or dates. It must contains at most 10 words. The title must be in English.",
                    model="gpt-4o",
                    base_url="https://api.openai.com/v1",
                    api_key=os.environ["OPENAI_API_KEY"],
                    openai_chat_kwargs={},
                )
                title = title_response.choices[0].message.content.strip('"')
                logging.info(f"{newsletter_config} | Generated title: {title}")
                title_slug = slugify(title)

                # Cut the slug to 50 characters. Cut on a dash.
                max_slug_length = 50
                if len(title_slug) > max_slug_length:
                    title_slug = title_slug[:max_slug_length]
                    last_dash = title_slug.rfind("-")
                    if last_dash != -1:
                        title_slug = title_slug[:last_dash]

                # Generate an image from the newsletter
                logging.info(f"[{idx+1}/{len(newsletter_configs)}] {newsletter_config} | Generating newsletter image...")
                image_prompt_response = chat(
                    prompt=response_markdown,
                    system_prompt="Generate a prompt for DALLE3 to create an image for this newsletter that I can use for my Blog. The image must be simple with few details. Give me only the prompt and nothing else.",
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
                    output_markdown=response_markdown,
                    newsletter_config_id=newsletter_config.id,
                    title=title,
                    slug=title_slug,
                    image_url=image_url,
                    published_at=end_date,
                )

                session.add(newsletter)
                session.commit()

if __name__ == "__main__":
    r = generate_newsletter()
