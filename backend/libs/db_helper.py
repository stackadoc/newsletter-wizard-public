import json
from typing import List

from sqlalchemy.dialects.postgresql import insert
from tqdm import tqdm

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

    batch_size = 100
    with create_session() as session:
        # Use tqdm to iterate over batches
        for i in tqdm(range(0, len(items_to_insert), batch_size), desc="Inserting extracts"):
            batch = items_to_insert[i:i + batch_size]
            if not batch:
                continue

            stmt = insert(Extract).values(batch)
            # Specify the constraint name or the columns involved in the unique constraint
            stmt = stmt.on_conflict_do_nothing(
                index_elements=['source_id', 'content_id']
            )
            session.execute(stmt)
        session.commit()
