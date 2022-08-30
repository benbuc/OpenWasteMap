#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=stag.openwastemap.org \
TRAEFIK_TAG=stag.openwastemap.org \
STACK_NAME=stag-openwastemap-org \
TAG=stag \
docker-compose \
-f docker-compose.yml \
-f docker-compose.stag.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml

docker stack deploy -c docker-stack.yml --with-registry-auth "stag-openwastemap-org"
