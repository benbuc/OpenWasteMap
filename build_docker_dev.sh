#!/bin/bash

mkdir -p ./build
poetry export --dev -f requirements.txt --output ./build/requirements.txt --without-hashes

docker-compose --file docker-compose.dev.yml build --pull
docker-compose --file docker-compose.dev.yml pull