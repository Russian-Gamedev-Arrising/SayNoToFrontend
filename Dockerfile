FROM python:3.12.7-alpine3.20

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
COPY . /backend
WORKDIR /backend
EXPOSE 8000

RUN apk update && \
    apk add postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user
USER service-user