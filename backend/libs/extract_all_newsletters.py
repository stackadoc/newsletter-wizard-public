import logging
from datetime import datetime, timedelta
from typing import List

from libs.config import create_session
from libs.db_helper import insert_extracts
from libs.db_models import Source, Extract
from libs.extractors.ExtractorABC import ExtractorABC
from libs.extractors.extractors_config import extractors_config
from libs.types.ExtractorOutputType import ExtractorOutputType


def extract_all_newsletters():

    # Get all Sources
    with create_session() as session:
        sources: List[Source] = (
            session
            .query(Source)
            .all()
        )

    for source in sources:
        # Get last Extract date
        with create_session() as session:
            last_extract: Extract | None = (
                session
                .query(Extract)
                .filter(Extract.source_id == source.id)
                .order_by(Extract.content_date.desc())
                .first()
            )
            if not last_extract:
                logging.info(f"First extract for {source}. Will extract all messages sice 7 days.")
                date_start = datetime.now() - timedelta(days=7)
            else:
                date_start = last_extract.content_date

        extractor_config = extractors_config.get(source.type)
        if not extractor_config:
            logging.warning(f"Type {source.type} for {source} is not available (ignored)")
            continue

        extractor: ExtractorABC = extractor_config["extractor_class"]()
        logging.info(f"Get messages for {source} (start date = {date_start})...")
        data: List[ExtractorOutputType] = extractor.extract(date_start, source)
        if data:
            logging.info(f"Insert {len(data)} messages for {source}...")
            insert_extracts(source, data)
        else:
            logging.info(f"No messages found for {source}")



if __name__ == "__main__":
    extract_all_newsletters()
