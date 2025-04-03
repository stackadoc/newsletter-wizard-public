import argparse
import logging
from datetime import date, timedelta

from libs import config
from libs.extractors.extract_all_newsletters import extract_all_newsletters
from libs.mailgun import send_email
from libs.newsletter_generator import generate_newsletter

def generate_and_send_newsletter(date_start: date):
    data = extract_all_newsletters(date_start)
    output_file = generate_newsletter(data)
    logging.info(f"Generated newsletter: file://{output_file.as_posix()}")
    with open(output_file) as f:
        html = f.read()
    r = send_email(
        to=config.EMAIL_TO,
        subject=f"Newsletter Wizard {date.today().strftime('%Y-%m-%d')}",
        html=html,
    )
    logging.info(f"Email sent to {config.EMAIL_TO}: {r.text}")

def main():
    parser = argparse.ArgumentParser(description='Generate newsletter from Discord messages.')
    parser.add_argument('--nb_days', type=int, default=30, help='Number of days to look back for messages.')
    args = parser.parse_args()

    date_start = date.today() - timedelta(days=args.nb_days)

    logging.info(f"Create newsletter from date {date_start}...")
    generate_and_send_newsletter(date_start)

if __name__ == "__main__":
    main()