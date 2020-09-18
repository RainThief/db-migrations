FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN  apt-get update &&  apt-get install -y --no-install-recommends \
    libpq-dev=11.7-0+deb10u1 \
    libc6-dev=2.28-10 \
    gcc=4:8.3.0-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

RUN apt-get purge -y gcc libpq-dev && apt-get autoremove -y && rm -Rf /var/cache/apt

WORKDIR /usr/app
