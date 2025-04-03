from pydantic import BaseModel
import abc


class BaseNewsletterConfig(BaseModel, abc.ABC):
    name: str
    type: str

class DiscordNewsletterConfig(BaseNewsletterConfig):
    type: str = "discord"
    channel: str