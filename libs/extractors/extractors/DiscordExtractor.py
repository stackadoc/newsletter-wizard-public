import json
import logging
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Dict, Union

from libs import config
from libs.extractors.ExtractorABC import ExtractorABC


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

    @staticmethod
    def _format_discord_messages(extract_data: dict, max_reactions: int = 6) -> str:
        newsletter_messages = [
            f"# Server: {extract_data['guild']['name']} - Channel: #{extract_data['channel']['name']}",
        ]
        messages = extract_data["messages"]
        for message in messages:
            # Get reactions
            nb_reactions = sum([r["count"] for r in message["reactions"]])
            reactions_str_list = []
            nb_reactions_in_text = 0
            for reaction in sorted(
                    message["reactions"], key=lambda x: x["count"], reverse=True
            )[:max_reactions]:
                reactions_str_list.append(f"{reaction['count']}*{reaction['emoji']['name']}")
                nb_reactions_in_text += reaction["count"]
            reactions_str = " + ".join(reactions_str_list)
            if len(message["reactions"]) > max_reactions:
                reactions_str += f" + {nb_reactions - nb_reactions_in_text} more"
            reactions_str = f" [reactions: {reactions_str}]" if reactions_str else ""

            # Get message content
            content = message['content'].replace('\n', ' ')
            content = re.sub(' +', ' ', content)

            # Construct message for LLM
            message_str = f"[{message['timestamp']}] {message['author']['nickname']}: {content}{reactions_str}"
            newsletter_messages.append(message_str)

        return '\n\n'.join(newsletter_messages)

    def extract(self, date_start: date, newsletter_config: dict) -> Union[str, bool]:

        channels_params = []
        for channel in newsletter_config["channels"]:
            channels_params += ["-c", channel]

        newsletter_output_dir = self.get_extract_dir(newsletter_config)
        output_path = (newsletter_output_dir / "%G - %C.json").as_posix()
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

        logging.info(f"Get messages for newsletter \"{newsletter_config['name']}\"...")
        logging.info(
            f"Command: {' '.join(command).replace(config.DISCORD_TOKEN, '<discord_token>')}"
        )
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Stream stdout and stderr in files
        for line in process.stdout:
            if self._check_errors(line) == "invalid_token":
                return False
            with open(newsletter_output_dir / "stdout.txt", "a") as f:
                f.write(line)
        for line in process.stderr:
            if self._check_errors(line) == "invalid_token":
                return False
            with open(newsletter_output_dir / "stderr.txt", "a") as f:
                f.write(line)

        process.wait()  # Wait for the process to complete

        # Read json files and format messages to text
        files = newsletter_output_dir.glob("*.json")
        return "\n\n---\n\n".join([
            self._format_discord_messages(json.loads(file.read_text()))
            for file in files
        ])



