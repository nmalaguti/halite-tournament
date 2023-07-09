ARG PYTHON_VERSION=3.11-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY . /code
RUN poetry install --only-root --no-interaction

RUN DJANGO_CONFIGURATION=CollectStatic python manage.py collectstatic --noinput

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=project.settings
ENV DJANGO_CONFIGURATION=Prod

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "project.wsgi"]
