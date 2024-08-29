#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

REGISTRY=${REGISTRY:-index.docker.io}
IMAGE=${REGISTRY}/drop/transformers/text-geocoder:${1:-local}

echo Building $IMAGE
docker build \
    --force-rm \
    --rm=true \
    -f "$CWD/Dockerfile" \
    --platform linux/amd64 \
    --build-arg REGISTRY=$REGISTRY \
    --build-arg http_proxy=${http_proxy:-} \
    --build-arg https_proxy=${https_proxy:-} \
    -t $IMAGE \
    "$CWD/.."
