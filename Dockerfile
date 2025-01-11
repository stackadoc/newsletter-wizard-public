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

# Install DiscordChatExporter (x86_64 version)
RUN mkdir -p discord_chat_exporter && \
    curl -L -o discord_chat_exporter/DiscordChatExporter.Cli.linux-x64.zip https://github.com/Tyrrrz/DiscordChatExporter/releases/download/2.44/DiscordChatExporter.Cli.linux-x64.zip && \
    unzip -o discord_chat_exporter/DiscordChatExporter.Cli.linux-x64.zip -d discord_chat_exporter && \
    rm discord_chat_exporter/DiscordChatExporter.Cli.linux-x64.zip

# Set PYTHONPATH
ENV PYTHONPATH="/app"

# Set the entrypoint to run the application
ENTRYPOINT ["poetry", "run", "python", "app/discord_newsletter.py"]

# Default command arguments
CMD ["--nb_days", "7"]