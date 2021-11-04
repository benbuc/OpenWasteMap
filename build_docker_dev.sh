#!/bin/bash

mkdir -p ./build
poetry export -f requirements.txt --output ./build/requirements.txt --without-hashes

docker-compose --file docker-compose.dev.yml build --pull

docker-compose --file docker-compose.dev.yml pull