import re
from datetime import date
from pathlib import Path

from openai import OpenAI
from markdown import markdown

from libs import config


def generate_newsletter(data, output_dir: str):
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    newsletter_md = [f"# Discord Newsletter {date.today().isoformat()}"]

    for server_name, channels in data.items():

        # Construct
        server_messages = []
        for channel_name, messages in channels.items():
            for message in messages:
                reactions_str = ' + '.join([f"{r['count']}*{r['emoji']}" for r in message['reactions']])
                if reactions_str:
                    reactions_str = f" [reactions: {reactions_str}]"
                content = message['content'].replace('\n', ' ')
                content = re.sub(' +', ' ', content)
                server_messages.append(f"[{message['datetime'].isoformat()}] {message['username']}: {content}{reactions_str}")
            server_messages.append('---')

        if len(server_messages) > 0:
            server_messages = '\n'.join(server_messages)

            # Call OpenAI
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": config.SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": server_messages,
                    },
                ],
                temperature=0.5,
                top_p=1,
            )

            response_md = response.choices[0].message.content
            newsletter_md += [f"# Serveur #{server_name}", response_md]

    output_file = Path(output_dir) / f"discord_newsletter_{date.today().isoformat()}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        if len(newsletter_md) > 0:
            f.write(markdown('\n'.join(newsletter_md)))
        else:
            f.write("No messages to process")

    return output_file
