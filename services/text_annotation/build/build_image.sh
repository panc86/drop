#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

REGISTRY=${REGISTRY:-index.docker.io}
IMAGE=${REGISTRY}/drop/services/text-annotation:${1:-local}

# test before build
$CWD/../.venv/bin/pytest --disable-warnings $CWD/..

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
