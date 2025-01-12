import logging
from datetime import date
from typing import Dict, Any

from libs import config

def extract_all_newsletters(date_start: date) -> Dict[str, Any]:

    # Get all newsletters types
    extractors_instances = {}
    newsletter_data_text = {}
    for newsletter in config.NEWSLETTERS_CONFIG:
        if newsletter["type"] not in config.EXTRACTORS:
            logging.warning(f"Type {newsletter['type']} for newsletter {newsletter['name']} is not available (ignored)")
        if newsletter["type"] == "discord":
            if not newsletter["type"] in extractors_instances:
                extractors_instances[newsletter["type"]] = config.EXTRACTORS[newsletter["type"]]()

    # Extract data for each newsletter
    for newsletter in config.NEWSLETTERS_CONFIG:
        newsletter_data_text[newsletter["name"]] = extractors_instances[newsletter["type"]].extract(date_start, newsletter)

    return newsletter_data_text


if __name__ == "__main__":
    from datetime import timedelta
    r = extract_all_newsletters(date.today() - timedelta(days=7))

    # import json
    # with open("/tmp/output.json", "w") as f:
    #     f.write(json.dumps(r, indent="\t", ensure_ascii=False))
