FROM joshava/uwsgi-nginx

WORKDIR /app

COPY kotori kotori
COPY run.py run.py
COPY requirements.txt requirements.txt

RUN apk add --no-cache build-base jpeg-dev zlib-dev && \
    pip install -r requirements.txt && \
    pip install uwsgi && \
    apk del build-base zlib-dev && \
    rm -rf /var/cache/apk/*
