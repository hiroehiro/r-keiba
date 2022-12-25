FROM python:3.10

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    && pip install -r requirements.txt

WORKDIR /opt/app