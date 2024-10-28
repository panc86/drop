#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

bash $CWD/extraction_api/dockerize.sh
bash $CWD/transformers/text_annotator/dockerize.sh
bash $CWD/transformers/text_geocoder/dockerize.sh
