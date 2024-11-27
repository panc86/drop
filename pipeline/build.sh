#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

bash $CWD/extractors/dockerize.sh $(<$CWD/extractors/RELEASE)
bash $CWD/transformers/text_annotator/dockerize.sh
bash $CWD/transformers/text_geocoder/dockerize.sh
