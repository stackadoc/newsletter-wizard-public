# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies (curl, unzip, and libicu)
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libicu-dev \
    && rm -rf /var/lib/apt/lists/*

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

# Set the entrypoint to run the application
ENTRYPOINT ["poetry", "run", "python", "app/send_newsletter.py"]

# Default command arguments
CMD ["--nb_days", "7"]