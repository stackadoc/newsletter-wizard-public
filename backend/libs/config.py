import datetime
import logging
import os
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

PROJECT_DIR = Path(__file__).parent.parent

# ========== LOGGING ============================================================================= #

logging_formatter_str = "[%(asctime)s] %(levelname)s : %(name)s %(module)s.%(funcName)s :%(lineno)d - %(message)s"

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

    FORMATS = {
        logging.DEBUG: grey + logging_formatter_str + reset,
        logging.INFO: blue + logging_formatter_str + reset,
        logging.WARNING: yellow + logging_formatter_str + reset,
        logging.ERROR: red + logging_formatter_str + reset,
        logging.CRITICAL: bold_red + logging_formatter_str + reset,
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
logging.getLogger("PIL").setLevel(logging.WARNING)

root_logger = logging.getLogger()

root_logger.setLevel(logging.DEBUG)
# root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomColorFormatter())

root_logger.addHandler(console_handler)

# --- File Handler (New) ---
# Create logs directory if it doesn't exist
log_dir = PROJECT_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# Generate filename with timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_dir, f"{timestamp}.txt")

# Create file handler
file_handler = logging.FileHandler(log_filename)

# Create a standard formatter for the file (without colors)
file_formatter = logging.Formatter(logging_formatter_str)
file_handler.setFormatter(file_formatter)

# Add file handler to the root logger
root_logger.addHandler(file_handler)
# --- End of File Handler ---

# ========== CONFIGURATION ======================================================================= #

PLAYWRIGHT_STATE_PATH = PROJECT_DIR / "local/playwright_state.json"

LAST_RUN_FILE = PROJECT_DIR / "config/last_run.txt"

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# ========== DATABASE ============================================================================ #

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_name = os.environ["DB_NAME"]
db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
create_session = sessionmaker(
    bind=create_engine(db_uri, client_encoding="utf8", pool_size=50)
)

# ========= AWS ================================================================================== #

CUSTOM_AWS_ENDPOINT_URL = os.environ["CUSTOM_AWS_ENDPOINT_URL"]
CUSTOM_AWS_ACCESS_KEY_ID = os.environ["CUSTOM_AWS_ACCESS_KEY_ID"]
CUSTOM_AWS_SECRET_ACCESS_KEY = os.environ["CUSTOM_AWS_SECRET_ACCESS_KEY"]
CUSTOM_AWS_REGION_NAME = os.environ["CUSTOM_AWS_REGION_NAME"]
CUSTOM_AWS_BUCKET_NAME = os.environ["CUSTOM_AWS_BUCKET_NAME"]

# ========== REDDIT ============================================================================== #

REDDIT_CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
REDDIT_USER_AGENT = os.environ["REDDIT_USER_AGENT"]
REDDIT_USERNAME = os.environ["REDDIT_USERNAME"]
REDDIT_PASSWORD = os.environ["REDDIT_PASSWORD"]