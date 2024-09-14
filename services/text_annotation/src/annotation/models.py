import os
from typing import Iterable

import laserembeddings
import numpy
import tensorflow as tf


models_dir = os.path.join(os.path.dirname(__file__), "data")

embeddings = laserembeddings.Laser(
    bpe_codes=os.path.join(models_dir, "93langs.fcodes"),
    bpe_vocab=os.path.join(models_dir, "93langs.fvocab"),
    encoder=os.path.join(models_dir, "bilstm.93langs.2018-12-26.pt"),
    embedding_options=dict(cpu=True),
)
impact_model = tf.keras.models.load_model(os.path.join(models_dir, "impacts.h5"))
flood_model = tf.keras.models.load_model(os.path.join(models_dir, "floods.h5"))


def vectorize(texts: Iterable[str]) -> numpy.ndarray:
    return embeddings.embed_sentences(texts, lang="ml")


def annotate(vectors: numpy.ndarray):
    y = dict(
        impact=impact_model(vectors).numpy()[:, 1].tolist(),
        flood=flood_model(vectors).numpy()[:, 1].tolist(),
    )
    # clear tensorflow session cache
    tf.keras.backend.clear_session()
    return y
