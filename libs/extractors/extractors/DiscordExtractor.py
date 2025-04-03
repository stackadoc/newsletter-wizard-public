import json
import logging
import re
import subprocess
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import List

from libs import config
from libs.extractors.ExtractorABC import ExtractorABC
from libs.types.ExtractorOutputType import ExtractorOutputType
from libs.types.NewsletterConfigType import DiscordNewsletterConfig


class DiscordExtractor(ExtractorABC):

    @staticmethod
    def _check_errors(log_line: str) -> str:
        error_type = None
        if "ERROR" in log_line:
            logging.error("Error in Discord chat exporter")
            error_type = "error"
        if "Authentication token is invalid" in log_line:
            logging.error("Invalid Discord token")
            error_type = "invalid_token"
        return error_type

    def row_to_string(self, row: dict) -> str:
        # Get reactions
        nb_reactions = sum([r["count"] for r in row["reactions"]])
        reactions_str_list = []
        nb_reactions_in_text = 0
        for reaction in sorted(
                row["reactions"], key=lambda x: x["count"], reverse=True
        )[:6]:
            reactions_str_list.append(f"{reaction['count']}*{reaction['emoji']['name']}")
            nb_reactions_in_text += reaction["count"]
        reactions_str = " + ".join(reactions_str_list)
        if len(row["reactions"]) > 6:
            reactions_str += f" + {nb_reactions - nb_reactions_in_text} more"
        reactions_str = f" [reactions: {reactions_str}]" if reactions_str else ""

        # Get message content
        content = row['content'].replace('\n', ' ')
        content = re.sub(' +', ' ', content)

        # Construct message for LLM
        message_str = f"[{row['timestamp']}] {row['author']['nickname']}: {content}{reactions_str}"

        return message_str

    def extract(self, date_start: date, newsletter_config: DiscordNewsletterConfig) -> List[ExtractorOutputType]:

        channels_params = ["-c", newsletter_config.channel]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "%G - %C.json"
            output_path = output_path.as_posix()
            command = [
                (config.PROJECT_DIR / "discord_chat_exporter/DiscordChatExporter.Cli").as_posix(),
                "export",
                "--fuck-russia",
                "-t",
                config.DISCORD_TOKEN,
                "--after",
                date_start.strftime("%Y-%m-%d %H:%M"),
                "-f",
                "Json",
                "-o",
                output_path,
            ] + channels_params

            logging.info(f"Get messages for newsletter \"{newsletter_config.name}\"...")
            logging.info(
                f"Command: {' '.join(command).replace(config.DISCORD_TOKEN, '<discord_token>')}"
            )
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Stream stdout and stderr in files
            for line in process.stdout:
                if self._check_errors(line) == "invalid_token":
                    raise ValueError("Invalid Discord token")
            for line in process.stderr:
                if self._check_errors(line) == "invalid_token":
                    raise ValueError("Invalid Discord token")

            process.wait()  # Wait for the process to complete

            # Read json file and format messages to text
            files = list(Path(temp_dir).glob("*.json"))
            if len(files) == 0:
                return []

            with open(files[0], "r") as f:
                extract_data = json.load(f)
                messages = [
                    ExtractorOutputType(
                        content_date=datetime.fromisoformat(message["timestamp"]),
                        content=message,
                        content_id=message["id"],
                    )
                    for message in extract_data["messages"]
                ]

            return messages

