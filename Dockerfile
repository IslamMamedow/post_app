FROM python:3.11-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY post /post
WORKDIR /post
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password post-user

USER post-user
