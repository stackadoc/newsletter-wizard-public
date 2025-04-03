import logging
from datetime import date
from typing import List

from libs import config
from libs.db_helper import insert_extracts
from libs.extractors.extractors_config import extractors_config
from libs.types.ExtractorOutputType import ExtractorOutputType


def extract_all_newsletters(date_start: date):

    for newsletter in config.NEWSLETTERS_CONFIG:
        extractor_config = extractors_config.get(newsletter["type"])
        if not extractor_config:
            logging.warning(f"Type {newsletter['type']} for newsletter {newsletter['name']} is not available (ignored)")
            continue

        newsletter_config = extractor_config["config_type"](**newsletter)
        extractor = extractor_config["extractor_class"]()
        data: List[ExtractorOutputType] = extractor.extract(date_start, newsletter_config)
        insert_extracts(newsletter_config, data)


if __name__ == "__main__":
    from datetime import timedelta
    extract_all_newsletters(date.today() - timedelta(days=7))

    # import json
    # with open("/tmp/output.json", "w") as f:
    #     f.write(json.dumps(r, indent="\t", ensure_ascii=False))
