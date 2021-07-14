# syntax=docker/dockerfile:1
FROM python:3.9.6

# Server output displayed in the terminal
ENV PYTHONUNBUFFERED=1

# Docker Working Directory
WORKDIR /code

# Copy requirements.txt to WORKDIR
COPY ./docker/requirements.txt /code/

# Run on WORKDIR
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy BASEDIR(already setted on docker-compose) to WORKDIR
COPY . /code/
