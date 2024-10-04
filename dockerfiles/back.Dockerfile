FROM python:3.12-alpine

LABEL author="Sadialiou Diallo"
LABEL maintainer="SD"
LABEL version="1.2"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN apk update \
    && apk add --no-cache gcc musl-dev linux-headers mariadb-dev libffi-dev
COPY ./requirements.txt /tmp/requirements.txt


RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    adduser \
            --disabled-password \
            --no-create-home \
            django-user
COPY ./ /app
USER django-user