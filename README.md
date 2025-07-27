# TechNews Backend - Challenge 1: REST API

## What I Built

This is the first part of a news website backend. I used Django and Django REST Framework to create an API that serves news articles with filtering options.

## The Models

Three simple models were created:

### NewsItem
This is the main news article model. Each news item has A title (up to 100 characters), the full text content, creation and update timestamps, tags (can have multiple tags) and a source (where the news came from).

### Tag
Simple tagging system. Just has a caption/name for the tag.

### Source
Represents where the news came from. Has a name and optional URL.

## The API

I built a REST API using Django REST Framework's ViewSet. It gives you all the basic CRUD operations (create, read, update, delete) for news items.

### What You Can Do

**Get all news:**
```
GET /api/news/news-list/
```

**Filter by tags:**
```
GET /api/news/?tags=technology,sports
```
Also enabled in the filter section.

**Search in title and text:**
```
GET /api/news/?search=python
```
Also enabled in the search section.

**Exclude keywords:**
```
GET /api/news/?exclude_keywords=deprecated
```
Also enabled in the search section; begin a word with a dash(-) to exclude.

**Combine filters:**
```
GET /api/news/?tags=tech&search=django&exclude_keywords=tutorial
```
Only enabled using urls, since in the challenge details filtering and searching are seperated.

## Admin Panel

Set up a basic Django admin so you can easily add/edit news, tags, and sources through the web interface.


## Tests

Wrote unit tests to make sure everything works - testing the models, API endpoints, and all the filtering features.


# TechNews Backend - Challenge 2: Web Scraping

## What I Built

Web scraping capabilities were added so that Scrapy and Playwright could automatically gather news from Zoomit.ir. News articles are extracted by the scraper and stored in the Django database.

## The Spider

### ZoomitSpiderSpider
A Scrapy spider that crawls Zoomit.ir news archive and extracts article details.

**What it does:**
- Starts from Zoomit's archive page (sorted by newest)
- Extracts links to individual news articles
- Visits each article page to get details
- Avoids scraping already-visited URLs (checks against database)
- The ability to paginate through multiple pages (currently restricted to one page to save testing time; this can be altered in the code)

**Key Features:**
- Uses Playwright for JavaScript-heavy pages
- Waits for dynamic content to load: `wait_for_selector`
- Timeout set to 60 seconds
- Delay to remain undetected as a scraper
- Pagination by clicking associated button (using Playwright)
- Skips already-scraped articles
- Extracts: title, content, creation date, tags, writer, and source URL

## Data Pipeline

### SaveNewsToDBPipeline
Processes and saves scraped items to the Django database, by first createing or getting existing source record, creating new NewsItem in database, handling tags (creating new ones if needed), using threading to avoid blocking.

### Pipeline Configuration
Add to your `settings.py`:
```python
ITEM_PIPELINES = {
    'your_scraper.pipelines.SaveNewsToDBPipeline': 300,
}
```

## How the Scraper Works (overall steps):

1. **Start**: Goes to Zoomit archive page
2. **Extract Links**: Gets all article URLs from the page
3. **Filter**: Skips URLs already in database
4. **Scrape Details**: Visits each new article page
5. **Extract Data**: Gets title, text, date, tags, writer
6. **Save**: Pipeline saves everything to database


## What Gets Scraped

From each news article:
- **Title**: Main headline
- **Text**: Full article content (joined from multiple spans)
- **Created Date**: Publication date (since the model attribute is set to auto_now_add=True, the date is the date that the item is saved into the database - due to testing)
- **Tags**: Article categories/tags
- **Writer**: Article author
- **Source**: The article URL


### Prerequisites
```bash
pip install scrapy scrapy-playwright
playwright install --with-deps
```


This completes Challenge 2.

# TechNews Challenge 3 - Celery and Docker Implementation (Task automation and project dockerization)

In order to enable automated news scraping and scalable deployment architecture, Challenge 3 focuses on using Celery to implement background task processing and Docker to containerize the entire application.

## Celery Integration

- Used Celery to define a task and auto detect them (in the task.py file within the News_app)

### Beat Schedule Setup

- Used django-celery-beat to schedule automatic scraping ( currently set to 10 minutes - can be changed using admin panel or altering the code and build the container again) and Redis as the message broker. The task also uses `update_or_create` to avoid duplicates in the IntervalSchedule or PeriodicTask databases.
- Task name: 'Run Zoomit Spider'
- Target task: 'News_app.tasks.run_scraper'

### Monitoring
Used Flower dashboard to provide real-time task monitoring including information such as task success/failure tracking, worker status and other performance metrics.

## Architecture _ Docker-compose services
Five main services are included in containerized version of the app:

**Web Service**
- Runs the Django application using Gunicorn
- Exposed on port 8000
- Initializes Celery Beat schedule on startup
- Depends on database and Redis services

**Database Service**
- PostgreSQL 15 instance (Switched to Postgresql since sqlite3 does not support concurrency)
- Persistent data storage using Docker volumes
- Environment-based configuration

**Redis Service**
- Message broker for Celery task queue
- Standard Redis 7 image
- Handles task distribution between services

**Worker Service**
- Celery worker process
- Executes background tasks (news scraping)
- Uses custom entrypoint for dependency management

**Beat Service**
- Celery Beat scheduler
- Manages periodic task execution
- Requires database tables for schedule storage

**Flower Service**
- Celery monitoring dashboard
- Accessible on port 5555
- Provides task monitoring and management interface

## Docker Configuration

### Dockerfile

The Docker image is built on Python 3.12-slim with the following components:

**System Dependencies:**
- Build tools and PostgreSQL client
- Playwright browser dependencies
- Required libraries for web scraping functionality

**Python Environment:**
- Installs requirements from requirements.txt
- Configures Playwright with browser installation
- Sets up working directory and entrypoints


## Entrypoint Scripts

### Main Entrypoint (entrypoint.sh)
- Waits for PostgreSQL availability
- Executes database migrations
- Collects static files
- Starts the specified service command

### Celery Entrypoint (entrypoint-celery.sh)
- Waits for Celery Beat database tables
- Ensures proper initialization order
- Starts Celery services

Both scripts implement retry logic for service dependencies.

## Environment Configuration

The application uses environment variables for configuration:

- Database connection parameters
- Django settings (SECRET_KEY, DEBUG)
- Service hostnames and ports
- Authentication credentials

## How to run:

### Initial Setup
```bash
docker-compose build
```

### Running task in container
```bash
docker-compose up
```

### Start services in background
```bash
docker-compose up -d
```

### Stop all services
```bash
docker-compose down
```

### After building and running processes in container:
- The main api is accessed via localhost:8000/news
- Flower is access via localhost:5555

As a result, the  provided code and files satisfies the Challenge 3 requirements for Docker containerization and Celery integration and overall, the entire TechNews project.