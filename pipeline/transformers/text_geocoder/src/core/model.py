import logging
from deeppavlov import build_model

from core import config
from core.gazetteer import load_gazetteer, match_geo_political_entities
from core.tags import parse_location_tags, titlecase, get_gpes


logger = logging.getLogger("deeppavlov")
logger.setLevel(logging.ERROR)


def merge_geocodes(original: list[dict], tags_by_data_point: list[list[dict]], locations_by_data_point: list[list[dict]]):
    locations_by_data_point = locations_by_data_point or [None] * len(original)
    return [
        dict(**origin, geo=dict(tags=tags, locations=locations))
        for origin, tags, locations in zip(original, tags_by_data_point, locations_by_data_point)
    ]


def get_geocoder():
    # initialize components
    bert_model = build_model("ner_ontonotes_bert_mult", download=False, install=False)
    gazetteer = load_gazetteer(config.gazetteer_filepath)

    def geocode(data_points: list[dict]):
        texts = [data_point["text"] for data_point in data_points]
        tags = parse_location_tags(*bert_model(titlecase(texts)))
        locations = match_geo_political_entities(get_gpes(tags), gazetteer)
        return merge_geocodes(data_points, tags, locations)

    return geocode
