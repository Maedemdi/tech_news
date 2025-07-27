FROM python:3.12-slim

ENV PYTHONDONTWRITEBYCODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gcc \
    git \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    zlib1g-dev \
    postgresql-client \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm-dev \
    libgtk-3-0 \
    libxshmfence1 \
    libasound2 \
    libxtst6 \
    libxss1 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN playwright install --with-deps

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
CMD [ "gunicorn", "TechNews_project.wsgi:application", "--bind", "0.0.0.0:8000" ]