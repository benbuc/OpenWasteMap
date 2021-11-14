#!/bin/bash

mkdir -p ./build
poetry export -f requirements.txt --output ./build/requirements.txt --without-hashes

docker build --target applayer --tag owm_app_image .
docker build --target staticlayer --tag owm_static_image .
docker build --target mailerlayer --tag owm_mailer_image .