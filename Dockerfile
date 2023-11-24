FROM python:3.9.6-slim-buster as base

RUN  apt-get update \
  && apt-get -y install build-essential libssl-dev git libffi-dev libgfortran5 pkg-config cmake gcc \
  && apt-get clean \
  && pip install --upgrade pip

RUN mkdir /src

WORKDIR /src

COPY requirements.txt /src/
RUN  pip install --no-cache-dir -r requirements.txt
COPY . .
ADD ./ /src/
