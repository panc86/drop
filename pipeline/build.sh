#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)


function get_release () {
    echo $(grep -oP '^version\s*=\s*"\K([0-9]\.[0-9]\.[0-9])' "$CWD/$1/pyproject.toml")
} 

# get app releases
if [ "${1}" == "--versioned" ]; then
    echo exporting relases
    export EXTRACTION_API_RELEASE=$(get_release extraction_api)
    export TEXT_ANNOTATOR_RELEASE=$(get_release transformers/text_annotator)
    export TEXT_GEOCODER_RELEASE=$(get_release transformers/text_geocoder)
fi

# build app
bash $CWD/extraction_api/build/build_image.sh $EXTRACTION_API_RELEASE 
bash $CWD/transformers/text_annotator/build/build_image.sh $TEXT_ANNOTATOR_RELEASE 
bash $CWD/transformers/text_geocoder/build/build_image.sh $TEXT_GEOCODER_RELEASE