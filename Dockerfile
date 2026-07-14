FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user
RUN useradd -m -u 1000 app && \
    mkdir -p /data /app/staticfiles && \
    chown -R app:app /app /data
USER app

EXPOSE 8000

CMD ["/bin/sh", "-c", "\
    if [ ! -f /data/db.sqlite3 ] && [ -f /app/db.sqlite3 ]; then cp /app/db.sqlite3 /data/db.sqlite3; fi && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile -"]
