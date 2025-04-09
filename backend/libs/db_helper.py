import json
from typing import List

from sqlalchemy.dialects.postgresql import insert

from libs.config import create_session
from libs.db_models import Extract, Source
from libs.types.ExtractorOutputType import ExtractorOutputType


def insert_extracts(
        source: Source,
        data_list: List[ExtractorOutputType],
) -> None:
    items_to_insert = [
        {
            "extractor_type": source.type,
            "config": source.config,
            "source_id": source.id,
            "content": json.loads(json.dumps(data.content, ensure_ascii=False, default=str)),
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
        index_elements=['source_id', 'content_id']
    )

    with create_session() as session:
        session.execute(stmt)
        session.commit()