import logging
import re
from datetime import date
from pathlib import Path

from openai import OpenAI
from markdown import markdown

from libs import config


def generate_newsletter(discord_data, output_dir: str):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    max_reactions = 6
    newsletter_md = [f"# Discord Newsletter {date.today().isoformat()}"]
    for newsletter_name, newsletter_data in discord_data.items():
        logging.info(f"Generate newsletter for \"{newsletter_name}\"...")
        newsletter_messages = []
        for idx_channel, channel in enumerate(newsletter_data):
            for message in channel["data"]["messages"]:
                # Get reactions
                nb_reactions = sum([r["count"] for r in message["reactions"]])
                nb_reactions_unique = len(message["reactions"])
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

            if idx_channel < len(newsletter_data) - 1:
                newsletter_messages.append('---')

        if len(newsletter_messages) > 0:
            newsletter_messages = '\n'.join(newsletter_messages)

            # Call OpenAI
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": config.SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": newsletter_messages,
                    },
                ],
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
            )

            response_md = response.choices[0].message.content
            newsletter_md += [f"# {newsletter_name}", response_md]

    output_file = Path(output_dir) / f"discord_newsletter_{date.today().isoformat()}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        if len(newsletter_md) > 0:
            f.write(markdown('\n'.join(newsletter_md)))
        else:
            f.write("No messages to process")

    return output_file
