# URL Shortener API

A production-style URL shortener built with FastAPI, PostgreSQL, and Redis.

## Features
- Shorten any URL to a 6-character code
- Redirect via short code
- Click analytics with timestamps
- Redis caching for high-frequency redirects
- Race condition handling with IntegrityError retry
- Fully containerized with Docker Compose

## Tech Stack
- **FastAPI** — API framework
- **PostgreSQL** — persistent storage
- **Redis** — caching layer
- **Docker Compose** — containerization
- **SQLAlchemy** — ORM

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Shorten a URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/stats/{short_code}` | Get click stats |

## Run Locally
```bash
# Clone the repo
git clone https://github.com/nagarjun-nagaraj/url-shortner.git
cd url-shortner

# Add .env file
echo "DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/urlshortener" > .env
echo "REDIS_URL=redis://localhost:6379" >> .env

# Start containers
docker compose up -d

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

## How Caching Works
First redirect hits PostgreSQL and caches the result in Redis (1hr TTL).
All subsequent redirects are served directly from Redis, no DB hit.