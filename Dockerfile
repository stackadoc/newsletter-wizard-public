# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install

# Set the entrypoint to run the application
ENTRYPOINT ["poetry", "run", "python", "app/discord_newsletter.py"]

# Default command arguments
CMD ["--nb_days", "7"]