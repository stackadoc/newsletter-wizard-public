# Discord Newsletter

## Configuration

### Settings
```shell
# Create output dir
mkdir -p output

# Create settings file
cp config/example.settings.yaml config/settings.yaml
nano config/settings.yaml
# Edit the content of config/settings.yaml
```

### Environment variables
```shell
cp .env.example .env
nano .env
# Edit the content of .env
```

## Run with Docker

Do the build only once
```shell
docker build -t newsletter-wizard .
docker run --rm -v ./config:/app/config -v ./output:/app/output --user 1000:1000 newsletter-wizard --nb_days 7
```

## Run with Docker
    
```shell
docker run --rm -v ./config:/app/config -v ./output:/app/output --user 1000:1000 newsletter-wizard --nb_days 7
```

## Run with Python

Install DiscordChatExporter
```shell
# Download DiscordChatExporter
mkdir -p discord_chat_exporter && wget -O discord_chat_exporter/DiscordChatExporter.Cli.linux-x64.zip https://github.com/Tyrrrz/DiscordChatExporter/releases/download/2.44/DiscordChatExporter.Cli.linux-x64.zip

# Unzip the downloaded file
unzip discord_chat_exporter/DiscordChatExporter.Cli.linux-x64.zip -d discord_chat_exporter

# Delete archive
rm discord_chat_exporter/DiscordChatExporter.Cli.linux-x64.zip
```

```shell
poetry install
poetry run python app/discord_newsletter.py --nb_days 7
```

# Troubleshooting

If you receive the error `Invalid Discord token`, you may need to update the token in the `.env` file.
Then, if you're using Docker, you'll need to rebuild the image.

# Style

You can create your own style by creating a `custom.css` file in the `config/` folder.