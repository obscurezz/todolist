FROM python:3.10-slim as base-image

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN adduser --disabled-password django
WORKDIR /home/django

EXPOSE 8000

RUN pip install poetry
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-ansi --no-root

ADD skypro skypro
COPY entrypoint.sh .

#ENTRYPOINT ["bash", "entrypoint.sh"]

FROM base-image as api-image
CMD gunicorn --pythonpath /home/django/skypro skypro.wsgi -w 2 --threads 2 -b 0.0.0.0:8000

FROM base-image as bot-image
CMD python skypro/manage.py runbot