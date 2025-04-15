FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

WORKDIR /code

COPY ./api/Pipfile ./api/Pipfile.lock ./api/

WORKDIR /code/api

RUN pipenv install --system --deploy

COPY . .
