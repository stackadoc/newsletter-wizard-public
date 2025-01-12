import json
import logging
import re
from datetime import date
from pathlib import Path
from typing import Dict

from openai import OpenAI
from markdown import markdown

from libs import config


def generate_newsletter(data: Dict[str, str]):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    newsletter_md = [f"# Newsletter {date.today().isoformat()}"]

    for newsletter_name, extracted_text in data.items():
        logging.info(f"Generate newsletter for \"{newsletter_name}\"...")

        newsletter_config = next(newsletter_conf for newsletter_conf in config.NEWSLETTERS_CONFIG if newsletter_conf["name"] == newsletter_name)

        llm_config = next((llm_conf for llm_conf in config.LLM_CONFIG if llm_conf["id"] == newsletter_config["llm"]), None)
        if not llm_config:
            raise ValueError(f"LLM config not found for newsletter {newsletter_name}")

        # Call OpenAI
        openai_args = dict(
            model=llm_config["model"],
            messages=[
                {
                    "role": "system",
                    "content": llm_config["system_prompt"],
                },
                {
                    "role": "user",
                    "content": extracted_text,
                },
            ],
            temperature=llm_config["temperature"],
            top_p=llm_config["top_p"],
        )
        with open(Path(config.OUTPUT_DIR) / f"{newsletter_name} - OpenAI args.json", "w") as f:
            json.dump(openai_args, f, indent="\t", ensure_ascii=False)
        response = client.chat.completions.create(**openai_args)

        response_md = response.choices[0].message.content
        newsletter_md += [
            "---",
            f"# {newsletter_name}",
            response_md,
        ]

    output_file = Path(config.OUTPUT_DIR) / f"newsletter.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        if len(newsletter_md) > 0:
            html_body = markdown('\n'.join(newsletter_md))
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <style>
                    {config.CUSTOM_CSS}
                </style>
            </head>
            <body>
            {html_body}
            </body>
            </html>
            """
            f.write(html)
        else:
            f.write("No messages to process")

    return output_file
