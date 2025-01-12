import logging
import os
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv

from libs.extractors.DiscordExtractor import DiscordExtractor

load_dotenv()

# ========== LOGGING ============================================================================= #


class CustomColorFormatter(logging.Formatter):
    # Color codes : https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    white = "\u001b[38;5;250m"
    blue = "\u001b[38;5;67m"
    yellow = "\u001b[38;5;214m"
    red = "\u001b[38;5;160m"
    grey = "\u001b[38;5;243m"
    dark_grey = "\u001b[38;5;240m"
    bold_red = "\u001b[1m\u001b[38;5;160m"
    title = "\u001b[1m\u001b[7m"
    reset = "\u001b[0m"
    format_str = (
            "[%(asctime)s] %(levelname)s : %(name)s %(module)s.%(funcName)s :%(lineno)d -"
            + " %(message)s"
    )

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record, **args):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)
logging.getLogger("torchaudio").setLevel(logging.WARNING)
logging.getLogger("numba").setLevel(logging.WARNING)
logging.getLogger("multipart").setLevel(logging.WARNING)
logging.getLogger("aiobotocore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

root_logger = logging.getLogger()

root_logger.setLevel(logging.DEBUG)
# root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomColorFormatter())

root_logger.addHandler(console_handler)


PROJECT_DIR = Path(__file__).parent.parent

PLAYWRIGHT_STATE_PATH = PROJECT_DIR / "local/playwright_state.json"

OUTPUT_DIR = (PROJECT_DIR / f"output/{date.today().strftime('%Y-%m-%d')}").as_posix()
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

EXTRACTORS = {
    "discord": DiscordExtractor,
}

with open(PROJECT_DIR / "config/settings.yaml") as f:
    settings = yaml.safe_load(f)

    # LLM
    LLM_CONFIG = settings["llm"]

    # Newsletters
    NEWSLETTERS_CONFIG = settings["newsletters"]

    # Email
    MAILGUN_DOMAIN = settings["email"]["mailgun_domain"]
    MAILGUN_IS_EU = settings["email"]["mailgun_is_eu"]
    EMAIL_TO = settings["email"]["email_to"]

    # Custom
    if (PROJECT_DIR / "config/custom.css").exists():
        with open(PROJECT_DIR / "config/custom.css") as custom_css_file:
            CUSTOM_CSS = custom_css_file.read()
    else:
        CUSTOM_CSS = ""

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
MAILGUN_API_KEY = os.environ["MAILGUN_API_KEY"]