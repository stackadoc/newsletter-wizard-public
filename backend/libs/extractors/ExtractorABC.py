import abc
from datetime import datetime
from pathlib import Path
from typing import List

from libs import config
from libs.db_models import Source
from libs.types.ExtractorOutputType import ExtractorOutputType


class ExtractorABC(abc.ABC):

    @abc.abstractmethod
    def extract(self, date_start: datetime, newsletter_config: Source) -> List[ExtractorOutputType]:
        raise NotImplemented("Method not implemented")

    @abc.abstractmethod
    def row_to_string(self, row: dict) -> str:
        raise NotImplemented("Method not implemented")