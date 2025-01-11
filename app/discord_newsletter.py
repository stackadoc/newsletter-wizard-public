import argparse
import logging
from datetime import date, timedelta

from libs import config
from libs.discord_extractor import extract_messages
from libs.mailgun import send_email
from libs.newsletter import generate_newsletter

parser = argparse.ArgumentParser(description='Generate newsletter from Discord messages.')
parser.add_argument('--nb_days', type=int, default=30, help='Number of days to look back for messages.')
args = parser.parse_args()

date_start = date.today() - timedelta(days=args.nb_days)

logging.info(f"Create newsletter from date {date_start}...")

data = extract_messages(date_start)

if not data:
    raise ValueError("No data extracted from Discord")

output_file = generate_newsletter(data, config.OUTPUT_DIR)
logging.info(f"Generated newsletter: file://{output_file.as_posix()}")

with open(output_file) as f:
    html = f.read()
r = send_email(
    to=config.EMAIL_TO,
    subject=f"Newsletter Wizard {date.today().strftime('%Y-%-%d')}",
    html=html,
)
logging.info(f"Email sent to {config.EMAIL_TO}: {r.text}")