import datetime
import logging
import re
from typing import List

import praw

from libs import config
from libs.db_models import Source
from libs.extractors.ExtractorABC import ExtractorABC
from libs.types.ExtractorOutputType import ExtractorOutputType


class RedditExtractor(ExtractorABC):

    def __init__(self):
        super().__init__()
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            password=config.REDDIT_PASSWORD,
            user_agent=config.REDDIT_USER_AGENT,
            username=config.REDDIT_USERNAME,
        )

    def row_to_string(self, row: dict) -> str:
        # Get title
        title = row["title"]

        # Get reactions
        nb_ups = row["ups"]

        # Get flair
        flair = row["link_flair_text"]

        # Get message content
        content = re.sub(r'\s+', ' ', row['body'])

        # Get comments
        comments = row["comments"]
        comments_str = []
        for comment in comments:
            comment_body = re.sub(r'\s+', ' ', comment['body'])
            comment_ups = comment['ups']
            author = comment['author_name'] if comment['author_name'] else "Unknown"
            comments_str.append(f"- {author}: {comment_body} (Upvotes: {comment_ups})")
        comments_str = "\n".join(comments_str)

        # Construct message for LLM
        messages_list = [
            f"### {title}",
            f"Flair: {flair}" if flair else None,
            f"Author: {row['author_name']}" if row['author_name'] else None,
            content,
            f"Upvotes: {nb_ups}",
            f"Comments:\n{comments_str}" if comments_str else None,
        ]
        messages_list = [message for message in messages_list if message]
        message_str = "\n\n".join(messages_list)

        message_str += "\n\n"

        return message_str

    def extract(self, date_start: datetime, newsletter_config: Source) -> List[ExtractorOutputType]:
        submissions = []
        for idx_submission, submission in enumerate(self.reddit.subreddit(newsletter_config.config["subreddit"]).new(limit=9999)):

            if submission.created_utc < date_start.timestamp():
                break

            if submission.stickied:
                continue

            if submission.author and submission.author.name == "AutoModerator":
                continue

            if submission.selftext == "[removed]" or submission.selftext == "[deleted]":
                continue

            if submission.title == "[removed]" or submission.title == "[deleted]":
                continue

            if not submission.selftext:
                continue

            submission_data = {
                "title": submission.title,
                "url": submission.url,
                "body": submission.selftext,
                "ups": submission.ups,
                "link_flair_text": submission.link_flair_text,
                "submission_id": submission.id,
                "author_name": submission.author.name if submission.author else None,
                "created_utc": datetime.datetime.fromtimestamp(submission.created_utc),
                "comments": [],
            }

            max_comments = 5
            for idx, comment in enumerate(submission.comments):
                submission_data["comments"].append({
                    "body": comment.body,
                    "ups": comment.ups,
                    "created_utc": datetime.datetime.fromtimestamp(comment.created_utc),
                    "author_name": comment.author.name if comment.author else None,
                })
                if idx+1 >= max_comments:
                    break

            logging.debug(f"Submission #{idx_submission+1}: {submission_data['created_utc']}")

            submissions.append(submission_data)

        return [
            ExtractorOutputType(
                content_date=submission["created_utc"],
                content_id=submission["submission_id"],
                content=submission,
            )
            for submission in submissions
        ]

if __name__ == '__main__':
    extractor = RedditExtractor()
    date_start = datetime.datetime(2024, 4, 4)

    newsletter_config = Source(
        name="test",
        type="reddit",
        config={
            "subreddit": "LocalLLaMA",
        }
    )

    submissions = extractor.extract(date_start, newsletter_config)

    texts = []
    for submission in submissions:
        texts.append(extractor.row_to_string(submission.content))