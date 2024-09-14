#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

MODELS_DIR=$CWD/geocode/data
mkdir -p $MODELS_DIR

# download BERT Multilingual NLP models from DeepPavlov repo
HOME=$MODELS_DIR python -m deeppavlov download -i ner_ontonotes_bert_mult

# start service
pushd $CWD
exec uvicorn main:app --host 0.0.0.0 "$@"
