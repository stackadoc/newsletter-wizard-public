import json
import logging
from typing import Optional, Dict, Any

from openai import OpenAI


def chat(
    prompt: str,
    system_prompt: str,
    model: str,
    base_url: str,
    api_key: str,
    openai_chat_kwargs: Optional[Dict[str, Any]] = None,
):
    if not openai_chat_kwargs:
        openai_chat_kwargs = {}

    client = OpenAI(api_key=api_key, base_url=base_url)

    logging.debug(f"Prompt :\n{json.dumps(prompt, ensure_ascii=False, indent='\t')}")
    logging.debug(f"Args :\n{json.dumps(openai_chat_kwargs, ensure_ascii=False, indent='\t')}")

    user_message = {
        "role": "user",
        "content": [
           {"type": "text", "text": prompt},
        ]
    }

    logging.debug("Generating response...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            user_message
        ],
        stream=False,
        **openai_chat_kwargs,
    )

    return response