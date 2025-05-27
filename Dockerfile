FROM python:3.11-alpine3.20

WORKDIR /usr/src/app

ARG DB_HOST=db
ARG REDIS_HOST=redis

ENV DB_HOST="${DB_HOST}"
ENV REDIS_HOST="${REDIS_HOST}"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    libffi-dev \
    gcc \
    musl-dev \
    python3-dev \
    curl

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --with dev

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
