# <div align="center"><img  src="app/public/logo-round-white-bg.svg" width="40"/> </br>Newsletter Wizard</div>

Newsletter Wizard is a tool that aggregates information from various sources like Reddit and
Discord, processes it, and generates with an LLM a blog-style website with curated articles.

- [Demo](https://news.stackadoc.com/)

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

**Backend:**
- Python 3.12+
- Poetry

**Website (Frontend):**
- Node.js 22+
- pnpm

**Database:**
- Docker (Recommended)
- *Alternatively:* PostgreSQL 17 installed directly

### Configuration

1. **Environment Variables:**
   - Copy the example environment file:
      ```shell
      cp .env.example .env
      ```
   - Edit the `.env` file with your specific configuration (API keys, database credentials, etc.). Use your preferred editor:
      ```shell
      nano .env
      ```
   - Create symbolic links for the backend and frontend apps to access the central `.env` file:
      ```shell
      ln -s ../.env app/.env && ln -s ../.env backend/.env
      ```

2. **Database Setup (Choose one):**
   - **Option A: Docker (Recommended)**
      
      Run the official PostgreSQL container:
      ```shell
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
   - **Option B: Bare Metal PostgreSQL**
      
      Ensure you have PostgreSQL 17 installed and running. Create a database and user matching the credentials specified in your `.env` file.

3. **Install Frontend Dependencies:**
    ```shell
    cd app
    pnpm install
    ```

4. **Install Backend Dependencies:**
    ```shell
    cd backend
    poetry install
    ```

5. **Database Migration:**
    Apply the database schema:
    ```shell
    cd app
    npx drizzle-kit migrate
    ```

6. **Install DiscordChatExporter:**
   
   This tool is required for extracting Discord messages.
   1. Navigate to the [DiscordChatExporter Releases Page](https://github.com/Tyrrrz/DiscordChatExporter/releases/latest).
   2. Download the appropriate version for your Operating System (e.g., `DiscordChatExporter.Cli.linux-x64.zip` for Linux).
   3. Extract the downloaded archive.
   4. Rename the extracted folder to `discord_chat_exporter`.
   5. Move this `discord_chat_exporter` folder into the `backend` directory of the project.

## 💻 Development Workflow

1. **Initialize Newsletter Configuration (One-time setup):**
   Run the initialization script located in the backend:
   ```shell
   # Ensure you are in the backend directory or provide the full path
   python backend/dev/init_db.py
   ```

2. **Extract Newsletter Sources:**
   Execute the extraction script:
   ```shell
   # Ensure you are in the backend directory or provide the full path
   python backend/libs/extract_all_newsletters.py
   ```

3. **Generate Newsletter Content:**
   Run the generation script:
   ```shell
   # Ensure you are in the backend directory or provide the full path
   python backend/libs/newsletter_generator.py
   ```

4. **Start Frontend Development Server:**
   Navigate to the `app` directory and start the development server:
   ```shell
   cd app
   pnpm dev
   ```
   The website should now be accessible, typically at `http://localhost:5173` (or the port configured by Vite/your setup).

## 📚 Resources & Documentation

- **LLM Integration:** [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction) (Used for various LLM interactions)
- **Frontend Routing:** [React Router v7](https://reactrouter.com/home)
- **Frontend File-Based Routing:** [React Router File Route Conventions](https://reactrouter.com/how-to/file-route-conventions)
- **Frontend UI Components:** [Shadcn/ui](https://ui.shadcn.com/)
- **CSS Framework:** [Tailwind CSS](https://tailwindcss.com/docs/styling-with-utility-classes)
- **Database ORM:** [Drizzle ORM](https://orm.drizzle.team/docs/overview)
- **Reddit Data Extraction:** [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/stable/)
- **Discord Data Extraction:** [DiscordChatExporter Documentation](https://github.com/Tyrrrz/DiscordChatExporter/tree/master/.docs)

## 🚢 Production Deployment

### Frontend Deployment (Docker Compose)

1. **Configure Production Environment:**
   Copy the example environment file specifically for production:
   ```shell
   cp .env.example .env
   ```
   Edit the `.env` file with your production database credentials, API keys, and other settings:
   ```shell
   nano .env
   ```

2. **Start Services:**
   From the root directory of the project, use Docker Compose to build and start the frontend container in detached mode:
   ```shell
   docker compose up -d
   ```
   This will start the frontend service and Caddy web server as defined in your `docker-compose.yml` file.

### Backend Automation (GitHub Actions)

The newsletter generation is automated using GitHub Actions. The workflow runs daily at 13:00 UTC and can also be triggered manually.

### Setting Up the Workflow

1. Fork this repository
2. Go to your repository's Settings > Secrets and variables > Actions
3. Copy the workflow: `mkdir -p .github/workflows/ && cp newsletter_workflow.example.yml .github/workflows/newsletter.yml`
4. Add all the required secrets from the `.env.example` file in the root of the project
5. The workflow will automatically run daily at 13:00 UTC (if schedule is uncommented)
6. You can also trigger it manually from the Actions tab
