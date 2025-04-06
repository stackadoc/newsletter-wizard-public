from typing import List, Union

import requests

from libs import config


def send_email(
    to: Union[str, List[str]], subject: str, html: str, sender: str = None
) -> requests.Response:
    sender = sender or f"Newsletter Wizard <mailgun@{config.MAILGUN_DOMAIN}>"

    url = f"https://api.{'eu.' if config.MAILGUN_IS_EU else ''}mailgun.net/v3/{config.MAILGUN_DOMAIN}/messages"

    return requests.post(
        url,
        auth=("api", config.MAILGUN_API_KEY),
        data={
            "from": sender,
            "to": to,
            "subject": subject,
            "html": html,
        },
    )


if __name__ == "__main__":
    r = send_email(
        to="paul.chaumeilv@gmail.com",
        subject="Test",
        html="<h1>Hello 2</h1>",
    )
    print(r.text)
