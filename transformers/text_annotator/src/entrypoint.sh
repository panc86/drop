#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

MODELS_DIR=$CWD/annotation/data
mkdir -p $MODELS_DIR

# download embeddings from laserembeddings repo
if [[ ! -f $MODELS_DIR/93langs.fcodes || ! -f $MODELS_DIR/93langs.fvocab || ! -f $MODELS_DIR/bilstm.93langs.2018-12-26.pt ]]; then
     python -m laserembeddings download-models $MODELS_DIR
fi

# start service
exec python -B src/main.py "$@"
