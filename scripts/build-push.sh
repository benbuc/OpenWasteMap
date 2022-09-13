#! /usr/bin/env sh

# Exit in case of error
set -e

TAG=${TAG?Variable not set} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
VERSION=$(git describe --tags) \
sh ./scripts/build.sh

docker-compose -f docker-compose.yml push
