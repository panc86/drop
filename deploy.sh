#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)


function get_release () {
    echo $(grep -oP '^version\s*=\s*"\K([0-9]\.[0-9]\.[0-9])' $1)
}


# export environment variables
export $(grep -v '^#' "$CWD/.env" | xargs)


# get app releases
if [ "$DEV" == "0" ]; then
    echo exporting relases
    export EXTRACTION_API_RELEASE=$(get_release "$CWD/pipeline/extraction_api/pyproject.toml")
    export TEXT_ANNOTATOR_RELEASE=$(get_release "$CWD/pipeline/transformers/text_annotator/pyproject.toml")
    export TEXT_GEOCODER_RELEASE=$(get_release "$CWD/pipeline/transformers/text_geocoder/pyproject.toml")
    export DOCKER_REGISTRY=localhost:8080
fi


# build app
bash $CWD/pipeline/extraction_api/build/build_image.sh $EXTRACTION_API_RELEASE
bash $CWD/pipeline/transformers/text_annotator/build/build_image.sh $TEXT_ANNOTATOR_RELEASE
bash $CWD/pipeline/transformers/text_geocoder/build/build_image.sh $TEXT_GEOCODER_RELEASE


# deploy app stack
docker stack deploy --detach=false -c compose.yaml -c compose.staging.yaml drop
