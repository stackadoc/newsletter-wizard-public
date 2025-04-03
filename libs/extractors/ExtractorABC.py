import abc
from datetime import date
from pathlib import Path
from typing import List

from libs import config
from libs.types.ExtractorOutputType import ExtractorOutputType
from libs.types.NewsletterConfigType import BaseNewsletterConfig


class ExtractorABC(abc.ABC):

    @staticmethod
    def get_extract_dir(newsletter_config: dict) -> Path:
        extract_dir = Path(config.OUTPUT_DIR) / f"extracts/{newsletter_config['name']}/"
        extract_dir.mkdir(parents=True, exist_ok=True)
        return extract_dir

    @abc.abstractmethod
    def extract(self, date_start: date, newsletter_config: BaseNewsletterConfig) -> List[ExtractorOutputType]:
        raise NotImplemented("Method not implemented")

    @abc.abstractmethod
    def row_to_string(self, row: dict) -> str:
        raise NotImplemented("Method not implemented")