FROM python:3.12-alpine
WORKDIR /app

COPY . .
COPY ./entrypoint.sh entrypoint.sh

RUN apk update && \
    apk add --no-cache \
        build-base \
        linux-headers \
        librdkafka-dev && \
    pip install -r requirements.txt

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["sh", "entrypoint.sh"]