#!/bin/bash

mkdir -p ./build
poetry export -f requirements.txt --output ./build/requirements.txt --without-hashes

docker-compose build --pull

docker-compose pull