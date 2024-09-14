import logging
from deeppavlov import build_model


logger = logging.getLogger("deeppavlov")
logger.setLevel(logging.ERROR)


def load_bert_model():
    return build_model("ner_ontonotes_bert_mult", download=False, install=False)
