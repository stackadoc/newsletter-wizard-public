from datetime import datetime

from pydantic import BaseModel


class ExtractorOutputType(BaseModel):
    content_date: datetime
    content_id: str
    content: dict
