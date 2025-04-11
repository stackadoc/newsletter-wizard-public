# Discord Newsletter

## Development

### Requirements

Backend :
- Python 3.12
- Poetry

Website :
- Node 22
- pnpm

Database :
- Docker (or PostgreSQL 17 bare installed)

### Configuration

1. Create a `.env` file in the root directory of the project.
    ```shell
    cp .env.example .env
    nano .env # Edit the content of .env
    
    # Create symlinks to the .env file in app and backend directories
    ln -s ../.env app/.env && ln -s ../.env backend/.env
    ```
2. Start Database
    ```
    docker run -it --rm \
        --name newsletter-wizard-db \
        -p 5433:5432 \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_DB=newsletter_wizard \
        -v ./db/data:/var/lib/postgresql/data \
        postgres:latest \
        -c log_statement=all
    ```
3. Install frontend dependencies
    ```shell
    cd app
    pnpm install
    ```
4. Install backend dependencies
    ```shell
    cd backend
    poetry install
    ```
5. Create the database
    ```shell
    cd app
    npx drizzle-kit migrate
    ```

### Generate Newsletter

1. Execute the script in `backend/dev/init_db.py` to initialize the Newsletter configuration (do it only once).
2. Run the script from `backend/libs/extract_all_newsletters.py` to extract newsletter sources.
3. Run the script from `backend/libs/newsletter_generator.py` to generate the newsletter.

### Start client

Run the following command to start the client:
```shell
cd app
pnpm dev
```

## Production

> [!NOTE]
> Currently, only the website (app) is ready for production. The backend is not deployed yet.

1. Copy `.env.example` to `.env` and edit the content of `.env`.
    ```shell
    cp .env.example .env
    nano .env # Edit the content of .env
    ```
   
2. Start container
   ```shell
   # From the root directory of the project
   docker compose up -d
   ```