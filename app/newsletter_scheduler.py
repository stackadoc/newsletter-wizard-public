import schedule
import time
import logging
import os
from datetime import datetime, timedelta
from app.send_newsletter import generate_and_send_newsletter
from libs import config


def get_last_run_time():
    """Read the last execution time from the file."""
    if config.LAST_RUN_FILE.exists():
        with open(config.LAST_RUN_FILE, "r") as f:
            last_run_str = f.read().strip()
            if last_run_str:
                return datetime.fromisoformat(last_run_str)
    return None

def update_last_run_time():
    """Update the last execution time in the file."""
    with open(config.LAST_RUN_FILE, "w") as f:
        f.write(datetime.now().isoformat())

def run_newsletter():
    """Run the newsletter script if the interval has passed."""
    last_run = get_last_run_time()
    if last_run and (datetime.now() - last_run) < timedelta(hours=interval_hours):
        logging.info("Skipping newsletter: Interval not yet passed.")
        return

    if not last_run:
        last_run = datetime.now() - timedelta(hours=interval_hours)

    logging.info("Starting newsletter generation and sending...")
    try:
        generate_and_send_newsletter(last_run)
        update_last_run_time()
        logging.info("Newsletter sent successfully.")
    except Exception as e:
        logging.error(f"Error during newsletter generation: {e}")

# Example: User provides an interval in hours
interval_hours = 6  # Replace with user input
schedule.every(interval_hours).hours.do(run_newsletter)

logging.info("Scheduler started. Waiting for the next run...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)