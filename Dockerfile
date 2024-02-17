ARG VERSION=3.11-slim

FROM --platform=linux/amd64 python:${VERSION}

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && apt-get install -y openjdk-17-jdk-headless \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
