# TechNews

**An automated news collection system built with Django, Scrapy, Celery, Redis, and PostgreSQL.**

TechNews collects technology news from [Zoomit](https://www.zoomit.ir/), extracts article data, and stores it in PostgreSQL. Scrapy handles crawling and data extraction, Playwright supports browser-based page rendering, and Celery runs scraping jobs in the background. Celery Beat schedules recurring jobs.

Docker Compose runs the application and its supporting services in separate containers.

## Features

-   **Automated news scraping:** Collects news from Zoomit's archive.
-   **Browser automation:** Uses Playwright and Chromium for pages that require browser rendering.
-   **Background processing:** Runs scraping jobs through Celery.
-   **Periodic scheduling:** Uses Celery Beat and `django-celery-beat` to schedule scraping every 10 minutes.
-   **Persistent storage:** Stores articles and their associated tags in PostgreSQL.
-   **Duplicate handling:** Uses Django's `update_or_create()` to update an article with a matching URL or create it if it does not exist.
-   **Redis integration:** Uses Redis as the Celery message broker and a caching layer, caching newly scraped and saved data for 5 minutes, making recent results easier to access and verify.
-   **Containerization:** Uses Docker and Docker Compose to run the application and its supporting services.
-   **Database migrations:** Uses Django migrations to prepare the database schema.

## Technology Stack

  Technology           Purpose
  -------------------- ------------------------------------------
  Python               Main programming language
  Django               Backend framework and ORM
  Scrapy               Web crawling and data extraction
  Playwright           Browser automation and page rendering
  Celery               Background task processing
  Celery Beat          Periodic task scheduling
  django-celery-beat   Database-backed Celery Beat schedules
  PostgreSQL           Relational database
  Redis                Celery message broker and caching layer
  Docker               Application containerization
  Docker Compose       Multi-container application management

## Architecture

The main scraping workflow is:

1.  Celery Beat schedules the scraping task.
2.  Celery places the task in Redis.
3.  The Celery worker executes the task.
4.  The task starts the Scrapy spider.
5.  Scrapy extracts article details from Zoomit, using Playwright when browser rendering is needed.
6.  The pipeline saves articles and their tags to PostgreSQL through Django's ORM.
7.  Newly scraped and saved data is cached in Redis for 5 minutes, allowing recent results to be accessed quickly and verified.
8.  When an article URL already exists, the record is updated instead of creating another article.

The periodic task is configured to run every 10 minutes.

### Services

  Service         Responsibility
  --------------- -------------------------------------------------------
  `web`           Runs the Django application
  `celery`        Executes background scraping tasks
  `celery_beat`   Schedules recurring tasks
  `migrate`       Applies Django database migrations
  `db`            Stores application data in PostgreSQL
  `redis`         Provides the Celery message broker and caching layer

## Project Structure

The main parts of the project are organized as follows:

TechNews_dir/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── TechNews/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── ...
├── News_app/
│   ├── models.py
│   ├── tasks.py
│   ├── beat_setup.py
│   └── ...
└── News_scraper/
    └── News_scraper/
        ├── spiders/
        │   └── ...
        ├── items.py
        ├── pipelines.py
        └── settings.py

This is a representative overview. The repository may contain additional
files and configuration modules.

## Requirements

To run the containerized application, you need:

-   Docker Engine or Docker Desktop
-   Docker Compose
-   An internet connection to download container images, Python packages, and browser dependencies

You do not need to install Python or PostgreSQL separately on the host
when using the Docker Compose setup.

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/Maedemdi/tech_news.git
cd tech_news
```

### 2. Configure environment variables

Create a `.env` file in the project root. The variable names must match 
those referenced by your Django settings and `docker-compose.yml`.

A typical configuration may look like this:

``` dotenv
POSTGRES_DB=technews_db
POSTGRES_USER=technews_dbuser
POSTGRES_PASSWORD=change_this_password

DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

Adjust the names and values to match the project's actual configuration.
Use a strong password outside local development.

Inside the Compose network, Django should connect to PostgreSQL using
the service hostname `db` and port `5432`. A host-mapped PostgreSQL port
is for connections from the host machine, not from other containers.

Do not commit `.env` or real credentials to Git. Consider providing a
sanitized `.env.example` file instead.

### 3. Build and start the services

Run this command from the directory containing `docker-compose.yml`:

``` bash
docker compose up -d --build
```

Check the service status:

``` bash
docker compose ps
```

### 4. View logs

Django application logs:

``` bash
docker compose logs -f web
```

Celery worker logs:

``` bash
docker compose logs -f celery
```

Celery Beat logs:

``` bash
docker compose logs -f celery_beat
```

Migration service logs:

``` bash
docker compose logs migrate
```

Press `Ctrl+C` to stop following logs. This does not stop the
containers.

### 5. Open the Django application

Visit:

http://localhost:8000/

The pages and API endpoints available depend on the routes configured in
the project.

## Automated Scraping

The scraping task is defined in `News_app/tasks.py`, and the periodic
scheduling setup is defined in `News_app/beat_setup.py`.

The scheduled task is named `Run Zoomit Spider` and calls
`News_app.tasks.run_spider`. The configured interval is 10 minutes, and
`django-celery-beat` stores the schedule in the database.

To inspect the worker and scheduler logs, run:

``` bash
docker compose logs --tail=100 celery
docker compose logs --tail=100 celery_beat
```

A task being reported as successful does not, by itself, prove that
articles were collected. Check the worker logs and the database when
verifying a scrape.

## Database

PostgreSQL stores the collected news articles and their associated tags.
The pipeline uses Django's ORM to create or update articles based on
their URLs.

Check the number of stored articles:

``` bash
docker compose exec web python manage.py shell -c "from News_app.models import News; print(News.objects.count())"
```

Print the titles of up to five articles:

``` bash
docker compose exec web python manage.py shell -c "from News_app.models import News; print(list(News.objects.values_list('title', flat=True)[:5]))"
```

## Limitations: Website Structure Changes

The spider relies on CSS selectors to locate article elements and
extract their content from Zoomit. If Zoomit changes its HTML structure,
element attributes, or CSS classes, existing selectors may stop matching
the expected elements.

This can lead to missing articles, incomplete records, or scraping
failures.

To help detect and address these changes:

-   Periodically verify that the spider's selectors still match the intended elements.
-   Monitor logs and scraped item counts for unexpected changes.
-   Update the selectors when Zoomit's page structure changes.
-   Validate extracted fields before saving items to the database.

A scraping task can finish without collecting any articles, so
successful task execution should not be treated as proof that scraping
worked correctly.

## Useful Docker Commands

Rebuild the Celery image after changing its Dockerfile or dependencies:

``` bash
docker compose build celery
```

Restart the services:

``` bash
docker compose restart
```

Stop the services:

``` bash
docker compose down
```

**Warning:** The following command also removes named volumes, which may
contain PostgreSQL data:

``` bash
docker compose down -v
```

Use it only when you intentionally want to delete the data stored in
those volumes.

## Development Notes

-   Keep credentials and environment-specific settings out of source
    control.
-   Use Django migrations to manage database schema changes.
-   Keep crawling and extraction logic in Scrapy spiders and pipelines.
-   Use Celery for scraping jobs that should run outside normal web
    requests.
-   Use Celery Beat to schedule recurring jobs.
-   Check logs and database counts when troubleshooting scraping runs.
-   Avoid exposing PostgreSQL or Redis ports to the host unless
    development or operational needs require it.

## Potential Improvements

-   Improve retry handling and make scraping task failures propagate
    correctly to Celery.
-   Add structured logging and monitoring for scraping runs.
-   Add automated tests for models, pipelines, and task behavior.
-   Validate required fields before saving scraped items.
-   Add news search, filtering, or pagination if these are part of the
    planned API.
-   Add a production deployment configuration using a production-grade
    Django application server.

## License

No license is specified in this README. Add a `LICENSE` file if you
intend to distribute the project under an open-source license.
