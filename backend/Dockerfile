# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies (curl, unzip, libicu, and cron)
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libicu-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy the crontab file to the cron directory
COPY app-cron /etc/cron.d/app-cron

# Give execution rights on the cron job and create log file
RUN chmod 0644 /etc/cron.d/app-cron \
    && crontab /etc/cron.d/app-cron \
    && touch /app/cron.log

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Set Poetry virtualenvs path to a writable directory
ENV POETRY_VIRTUALENVS_PATH=/app/.venv

# Create the .venv directory and set permissions
RUN mkdir -p /app/.venv && chown -R 1000:1000 /app/.venv

# Install dependencies
RUN poetry install --no-root

# Determine architecture and download the correct version of DiscordChatExporter
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        URL="https://github.com/Tyrrrz/DiscordChatExporter/releases/download/2.44/DiscordChatExporter.Cli.linux-x64.zip"; \
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then \
        URL="https://github.com/Tyrrrz/DiscordChatExporter/releases/download/2.44/DiscordChatExporter.Cli.linux-arm64.zip"; \
    else \
        echo "Unsupported architecture: $ARCH"; exit 1; \
    fi && \
    mkdir -p discord_chat_exporter && \
    curl -L -o discord_chat_exporter/DiscordChatExporter.Cli.zip "$URL" && \
    unzip -o discord_chat_exporter/DiscordChatExporter.Cli.zip -d discord_chat_exporter && \
    rm discord_chat_exporter/DiscordChatExporter.Cli.zip

# Set PYTHONPATH
ENV PYTHONPATH="/app"

# Run cron in the foreground
CMD ["cron", "-f"]