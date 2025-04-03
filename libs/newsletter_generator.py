import logging
import os

from libs import config
from libs.config import create_session
from libs.db_models import Extract, Newsletter
from libs.extractors.ExtractorABC import ExtractorABC
from libs.extractors.extractors_config import extractors_config
from libs.openai_chat import chat


def generate_newsletter():
    # Get last newsletter date
    with create_session() as session:
        last_newsletter = (
            session.query(Newsletter).order_by(Newsletter.created_at.desc()).first()
        )
        last_newsletter_date = (
            last_newsletter.created_at.date() if last_newsletter else None
        )

    # Get all extracts since last newsletter (filter only if last_newsletter_date is not None)
    # Order by content_date asc
    with create_session() as session:
        extracts = (
            session.query(Extract)
            .filter(
                Extract.content_date > last_newsletter_date
                if last_newsletter_date
                else True
            )
            .order_by(Extract.content_date.asc())
            .all()
        )

    # Group by config
    grouped_extracts = {}
    for extract in extracts:
        config_name = extract.name
        if config_name not in grouped_extracts:
            grouped_extracts[config_name] = {
                "config": extract.config,
                "texts": [],
            }
        # Convert to text
        extractor_config = extractors_config.get(extract.config["type"])
        if not extractor_config:
            logging.warning(f"Extractor config not found for {config_name}")
            continue
        extractor_class = extractor_config["extractor_class"]
        extractor_instance: ExtractorABC = extractor_class()
        text = extractor_instance.row_to_string(extract.content)
        grouped_extracts[config_name]["texts"].append(text)

    source_texts = []
    for config_name, config_data in grouped_extracts.items():
        source_text = f"# {config_name}\n\n{'\n'.join(config_data['texts'])}"
        source_texts.append(source_text)

    # Join all texts
    source_text = "\n\n---\n\n".join(source_texts)

    response = chat(
        prompt=source_text,
        system_prompt=config.LLM_CONFIG["system_prompt"],
        model=config.LLM_CONFIG["model_name"],
        base_url=config.LLM_CONFIG["base_url"],
        api_key=os.environ[config.LLM_CONFIG["api_key_name"]],
        openai_chat_kwargs=config.LLM_CONFIG["params"],
    )

    response_message = response.choices[0].message.content

    return response_message


if __name__ == "__main__":
    r = generate_newsletter()
