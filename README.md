# Job Scraper - Backend API

Production-grade FastAPI backend for job scraping and management.

## Architecture

```
job-scraper-server/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/                # Config, database, security
│   ├── api/v1/endpoints/    # API routes
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic schemas
│   └── services/scraping/   # Abstract job scraping
├── alembic/                 # Database migrations
├── docker-compose/          # Docker configuration
├── .env.local               # Local environment
└── Dockerfile
```

## Tech Stack

- **Framework**: FastAPI 0.115
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Auth**: JWT tokens with bcrypt password hashing
- **Migrations**: Alembic

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/signup` | POST | Register new user |
| `/api/v1/auth/login` | POST | Login, get JWT token |
| `/api/v1/auth/me` | GET | Get current user info |
| `/api/v1/jobs` | GET | List all jobs |
| `/api/v1/jobs/{id}` | GET | Get job details |
| `/api/v1/jobs/scrape` | POST | Trigger job scraping |
| `/api/v1/applied-jobs` | GET | List applied jobs |
| `/api/v1/applied-jobs` | POST | Apply to a job |

## Environment Configuration

### Local Development (`.env.local`)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/job_scraper
```

### Docker (`docker-compose/.env`)
```env
DATABASE_URL=postgresql://postgres:password@db:5432/job_scraper
```

## Running Locally

### 1. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
# Copy environment file
copy .env.local .env   # Windows
cp .env.local .env     # Linux/Mac
```

### 4. Create Database

```sql
-- Run in PostgreSQL
CREATE DATABASE job_scraper;
```

### 5. Run Alembic Migrations

```bash
# Generate initial migration (first time only)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Start Server

```bash
uvicorn app.main:app --reload --port 8000
```

## Alembic Commands Reference

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Downgrade one migration
alembic downgrade -1

# View current migration
alembic current

# View migration history
alembic history
```

## Running with Docker

```bash
# Create shared network (once)
docker network create job-scraper-network

# Start services
cd docker-compose
docker-compose up -d --build
```

## All 4 Run Modes

| Mode | Backend | Frontend | Notes |
|------|---------|----------|-------|
| 1 | Local | Local | Both use localhost |
| 2 | Docker | Docker | Uses `api` network alias |
| 3 | Local | Docker | Frontend connects to host |
| 4 | Docker | Local | Backend on localhost:8000 |

## Job Scraping Design

Abstract `BaseJobScraper` class allows easy extension:

```python
class BaseJobScraper(ABC):
    @abstractmethod
    async def scrape(self, query, location) -> List[JobCreate]:
        pass
```

Currently implements `MockJobScraper` for demonstration.

## Security

- JWT tokens for authentication
- Bcrypt password hashing
- CORS configuration
- Environment-based secrets

## Swagger UI

Access API documentation at: `http://localhost:8000/docs`
