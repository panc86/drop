import numpy
import os

from core.cleaner import clean_text


embeddings_dir = os.path.join(os.path.dirname(__file__), "data")
models_dir = os.path.join(os.path.dirname(__file__), "models")


def merge_predictions(original: list[dict], impacts: list[float], floods: list[float]):
    return [
        dict(**origin, annotation=dict(impact=impact, flood=flood))
        for origin, impact, flood in zip(original, impacts, floods)
    ]


def get_model():
    import laserembeddings
    import tensorflow as tf

    embeddings = laserembeddings.Laser(
        bpe_codes=os.path.join(embeddings_dir, "93langs.fcodes"),
        bpe_vocab=os.path.join(embeddings_dir, "93langs.fvocab"),
        encoder=os.path.join(embeddings_dir, "bilstm.93langs.2018-12-26.pt"),
        embedding_options=dict(cpu=True),
    )
    impact_model = tf.keras.models.load_model(os.path.join(models_dir, "impacts.h5"))
    flood_model = tf.keras.models.load_model(os.path.join(models_dir, "floods.h5"))

    def predict(model, vectors: numpy.ndarray) -> list[float]:
        y_hat = model(vectors).numpy()[:, 1].tolist()
        tf.keras.backend.clear_session()
        return y_hat

    def annotate(data_points: list[dict]):
        texts = [clean_text(data_point["text"]) for data_point in data_points]
        vectors = embeddings.embed_sentences(texts, lang="ml")
        return merge_predictions(data_points, predict(impact_model, vectors), predict(flood_model, vectors))

    return annotate
