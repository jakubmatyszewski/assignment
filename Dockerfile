# Base
FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
    
COPY ./requirements.txt /assignment/requirements.txt

# Install packages
RUN pip3 install -r /assignment/requirements.txt

# Copy files
COPY ./app /assignment/app

# Run
WORKDIR /assignment
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
