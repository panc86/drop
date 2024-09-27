#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

MODELS_DIR=$CWD/core/data
mkdir -p $MODELS_DIR

# download BERT Multilingual NLP models from DeepPavlov repo
HOME=$MODELS_DIR python -m deeppavlov download -i ner_ontonotes_bert_mult

# start service
exec python -B src/main.py "$@"
