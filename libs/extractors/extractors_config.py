from libs.extractors.extractors.DiscordExtractor import DiscordExtractor
from libs.types.NewsletterConfigType import DiscordNewsletterConfig

extractors_config = {
    "discord": {
        "config_type": DiscordNewsletterConfig,
        "extractor_class": DiscordExtractor,
    }
}