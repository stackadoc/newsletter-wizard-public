import argparse
from datetime import date, timedelta

from libs import config
from libs.DiscordExtractor import DiscordExtractor
from libs.newsletter import generate_newsletter

parser = argparse.ArgumentParser(description='Generate newsletter from Discord messages.')
parser.add_argument('--nb_days', type=int, default=30, help='Number of days to look back for messages.')
args = parser.parse_args()

d = DiscordExtractor()
data = d.get_messages(date_start=date.today() - timedelta(days=args.nb_days))

output_file = generate_newsletter(data, config.OUTPUT_DIR)
print(f"Generated newsletter: file://{output_file.as_posix()}")