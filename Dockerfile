FROM python:3.10-alpine3.20
LABEL authors="Yurii"

ENV PYTHONUNBUFFERED 1

WORKDIR /django_test_task

ENV PYTHONPATH=${PYTHONPATH}:/django_test_task/management/commands

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
