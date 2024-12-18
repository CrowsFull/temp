FROM python:3.12-alpine
WORKDIR /app

COPY . .
COPY ./entrypoint.sh entrypoint.sh

RUN apk update && \
    apk add --no-cache \
        build-base \
        python3-dev \
        linux-headers \
        librdkafka-dev \
        librdkafka

RUN ["chmod", "+x", "entrypoint.sh"]

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]