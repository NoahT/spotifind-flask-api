FROM python:3.8-slim-buster

WORKDIR /workflow
COPY requirements.txt requirements.txt
COPY ./components ./components

RUN pip3 install -r requirements.txt
