import logging
import time
from datetime import datetime, date

from playwright.sync_api import sync_playwright
from libs import config
from lxml import html


class DiscordExtractor:

    def __init__(self):
        if not config.PLAYWRIGHT_STATE_PATH.exists():
            with open(config.PLAYWRIGHT_STATE_PATH, "w") as f:
                f.write("{}")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context(storage_state=config.PLAYWRIGHT_STATE_PATH)

        self.page = self.sign_in()

    def sign_in(self):
        page = self.context.new_page()
        page.goto("https://discord.com/login")

        logging.info("Please, connect to discord (5 minutes remaining).")

        page.wait_for_url("https://discord.com/channels/**", timeout=5 * 60 * 1000)

        logging.info("Connected")

        self.context.storage_state(path=config.PLAYWRIGHT_STATE_PATH)

        return page

    def get_messages(self, date_start: date):
        data = {}
        for server in config.DISCORD_CONFIG:
            # Open server page
            for channel in server["channels"]:
                logging.debug(f"Extracting messages from server [{server['name']}] channel #{channel['name']}")

                self.page.goto(channel["url"])
                time.sleep(3)

                all_messages = []
                while True:

                    messages_xpath = '//li[contains(@id, "chat-messages-")]'
                    messages = self.page.locator(messages_xpath).all()

                    # get first message timestamp
                    first_message = messages[0]
                    first_message_timestamp = first_message.locator('//time[contains(@id, "message-timestamp-")]')
                    datetime_str = first_message_timestamp.get_attribute("datetime")
                    message_datetime = datetime.fromisoformat(datetime_str)

                    if message_datetime.date() < date_start:
                        break
                    else:
                        # Scroll to the first message
                        # self.page.evaluate(f"document.querySelector('({messages_xpath})[1]').scrollIntoView()")
                        js_script = f"document.evaluate('({messages_xpath})[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollIntoView({{ behavior: 'smooth' }})"
                        self.page.evaluate(js_script)
                        self.page.mouse.wheel(0, -100)
                        time.sleep(3)

                tree = html.fromstring(self.page.content())
                # with open(f"/tmp/server-{server['name']}-channel-{channel['name']}.html", "w") as f:
                #     f.write(self.page.content())

                # Get all messages
                messages = tree.xpath('//li[contains(@id, "chat-messages-")]')
                for message in messages:
                    # If it's a reply, get message content
                    message_content = message
                    if message.xpath('.//*[contains(@aria-labelledby, "message-reply-context-")]'):
                        message_content = message.xpath('.//*[contains(@class, "contents_")]')[0]

                    # Get message timestamp
                    timestamp = message_content.xpath('.//time[contains(@id, "message-timestamp-")]/@datetime')[0]
                    message_datetime = datetime.fromisoformat(timestamp)

                    # Get reactions
                    reactions = message.xpath('.//*[contains(@id, "message-reactions-")]//*[contains(@class, "reactionInner_")]')
                    all_reactions = []
                    for reaction in reactions:
                        img_alt = reaction.xpath('.//img/@alt')[0]
                        reaction_count = int(reaction.xpath('.//*[contains(@class, "reactionCount_")]/text()')[0])
                        all_reactions.append({
                            "emoji": img_alt,
                            "count": reaction_count,
                        })

                    # Get message content
                    content = ' '.join(message_content.xpath('.//*[contains(@id, "message-content-")]//text()')).strip()

                    all_messages.append({
                        "message_tree": message,
                        "message_content_tree": message_content,
                        "content": content,
                        "reactions": all_reactions,
                        "datetime": message_datetime,
                    })

                all_messages = sorted([message for message in all_messages if message["datetime"].date() >= date_start], key=lambda x: x["datetime"])

                # Get usernames
                previous_username = None
                for idx, message in enumerate(all_messages):
                    username = message["message_content_tree"].xpath('.//span[contains(@id, "message-username-")]')
                    if username:
                        username = ' '.join(username[0].xpath(".//text()")).strip()
                        previous_username = username
                    else:
                        username = previous_username
                    all_messages[idx]["username"] = username

                if server["name"] not in data:
                    data[server["name"]] = {}

                if channel["name"] not in data[server["name"]]:
                    data[server["name"]][channel["name"]] = []

                data[server["name"]][channel["name"]] = all_messages

        return data
