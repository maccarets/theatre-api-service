FROM python:3.10.4-slim-buster
LABEL maintainers="maccarets@gmail.com"

ENV PYTHONUNBUFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt
RUN adduser --disabled-password --no-create-home django-user

COPY . .


USER django-user

