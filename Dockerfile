FROM python:3.12-alpine
WORKDIR /app

COPY . .
COPY ./entrypoint.sh entrypoint.sh

RUN apk update \
    && apk add \
           build-base \
           linux-headers && \
    pip install -r requirements.txt

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["sh", "entrypoint.sh"]