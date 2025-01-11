# Discord Newsletter

## Install

```shell
poetry install
```

Add your settings:
    
```shell
cp config/example.settings.yaml config/settings.yaml
nano config/settings.yaml
# Edit the content of config/settings.yaml
```

## Run

```shell
poetry run python app/discord_newsletter.py --nb_days 7
```

# Todo

- [ ] Use [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) 