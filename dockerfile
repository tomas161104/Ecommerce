# Dockerfile
FROM python:3.11-slim

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev gettext \
  && rm -rf /var/lib/apt/lists/*

# set workdir
WORKDIR /app

# copy requirements first for caching
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

# entrypoint will handle migrations/collectstatic in prod
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ecommerce.settings

CMD ["sh", "/entrypoint.sh"]
