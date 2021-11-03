#!/bin/bash

mkdir ./build
poetry export -f requirements.txt --output ./build/requirements.txt

docker-compose build --pull

docker-compose pull