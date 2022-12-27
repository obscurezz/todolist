FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN adduser --disabled-password django
WORKDIR /home/django

RUN pip install poetry
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-ansi --no-root

ADD skypro skypro

EXPOSE 8000
CMD gunicorn --pythonpath /home/django/skypro skypro.wsgi -w 2 --threads 2 -b 0.0.0.0:8000