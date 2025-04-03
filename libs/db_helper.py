from sqlite3 import IntegrityError
from typing import List

from sqlalchemy.dialects.postgresql import insert

from libs.config import create_session
from libs.db_models import Extract
from libs.types.ExtractorOutputType import ExtractorOutputType
from libs.types.NewsletterConfigType import BaseNewsletterConfig


def insert_extracts(
        newsletter_config: BaseNewsletterConfig,
        data_list: List[ExtractorOutputType],
) -> None:
    items_to_insert = [
        {
            "name": newsletter_config.name,
            "extractor_type": newsletter_config.type,
            "config": newsletter_config.model_dump(mode="json"),
            "content": data.content,
            "content_date": data.content_date,
            "content_id": data.content_id,
        }
        for data in data_list
    ]

    if not items_to_insert:
        return

    stmt = insert(Extract).values(items_to_insert)
    # Specify the constraint name or the columns involved in the unique constraint
    # Using the constraint name is generally more robust if columns change later
    stmt = stmt.on_conflict_do_nothing(
        constraint='uq_extract_name_content_id'
    )

    with create_session() as session:
        session.execute(stmt)
        session.commit()