#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)
REGISTRY="${DOCKER_REGISTRY:-index.docker.io}"
IMAGE="${REGISTRY}/pipeline/transformers/text-annotator:$(<$CWD/src/RELEASE)"

echo Building $IMAGE
docker build \
    --force-rm \
    --rm=true \
    -f "$CWD/Dockerfile" \
    --platform linux/amd64 \
    --build-arg http_proxy=${http_proxy:-} \
    --build-arg https_proxy=${https_proxy:-} \
    --build-arg REGISTRY=$REGISTRY \
    -t $IMAGE \
    $CWD
