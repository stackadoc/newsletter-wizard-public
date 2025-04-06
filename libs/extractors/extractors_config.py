from libs.extractors.extractors.DiscordExtractor import DiscordExtractor
from libs.extractors.extractors.RedditExtractor import RedditExtractor

extractors_config = {
    "discord": {
        "extractor_class": DiscordExtractor,
    },
    "reddit": {
        "extractor_class": RedditExtractor,
    }
}