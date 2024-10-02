#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

EMBEDDINGS_DIR=$CWD/core/data
mkdir -p $EMBEDDINGS_DIR

# download embeddings from laserembeddings repo
if [[ ! -f $EMBEDDINGS_DIR/93langs.fcodes || ! -f $EMBEDDINGS_DIR/93langs.fvocab || ! -f $EMBEDDINGS_DIR/bilstm.93langs.2018-12-26.pt ]]; then
     python -m laserembeddings download-models $EMBEDDINGS_DIR
fi

# start service
exec python -B src/main.py "$@"
