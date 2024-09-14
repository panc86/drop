from collections import Counter
from typing import Iterable

import pandas


def parse_location_tags(
    tokens: Iterable[Iterable[str]], tags: Iterable[Iterable[str]]
) -> Iterable[dict]:
    """
    Filters tokens given a set of tags allowed by the user.
    DeepPavlov NER algorithm uses prefixes to indicate B-egin,
    and I-nside relative positions of tokens. For more details, visit
    # http://docs.deeppavlov.ai/en/master/features/models/ner.html#ner-task.
    """
    ner = list()
    b_tags = ["B-GPE", "B-FAC", "B-LOC"]
    i_tags = ["I-GPE", "I-FAC", "I-LOC"]

    for cur_tokens, cur_tags in zip(tokens, tags):
        pos = 0
        loc = dict()
        max_len = len(cur_tags)
        while pos < max_len:
            pos_token, pos_tag = cur_tokens[pos], cur_tags[pos]
            # begin of location token
            if pos_tag not in b_tags:
                pos += 1
                continue
            # start building token from begin tag
            token = pos_token
            # scan next tags
            next_pos = pos + 1
            # stop if index reaches end or tag not in i_tags
            # next tag could be I-<tag> or B-<tag>
            # e.g. [["Russia", "China"]], [["B-GPE", "B-GPE"]]
            while next_pos < max_len and cur_tags[next_pos] in i_tags:
                # suffix to extend built token
                if cur_tokens[next_pos] != token:
                    token = " ".join([token, cur_tokens[next_pos]])
                next_pos += 1
            # cache built location token
            hashtable = loc.setdefault(pos_tag[2:], list())
            if token not in hashtable:
                hashtable.append(token)
            # update pointer
            pos = next_pos
        ner.append(loc or None)
    return ner


def get_gpes(tags):
    return [None if not isinstance(tag, dict) else tag.get("GPE", {}) for tag in tags]


def titlecase(texts: Iterable[str]) -> Iterable[str]:
    return [text.title() for text in texts]


def find_most_common(locations: Iterable[str]) -> Iterable[str]:
    # get locations with maximum frequency
    count = Counter(locations)
    max_count = max(count.values())
    return [item for item, freq in count.items() if freq == max_count]


def match_geo_political_entities(
    tags: Iterable[str], gazetteer: pandas.DataFrame
) -> Iterable[dict]:
    gpes = get_gpes(tags)
    # get only matches
    flat_gpes = [tag for gpe in gpes if gpe for tag in gpe]
    matches = gazetteer.loc[gazetteer.isin(flat_gpes).any(axis=1), :]
    # extract features
    country_features = [c for c in matches if "country" in c]
    region_features = [c for c in matches if "region" in c]
    city_features = [c for c in matches if "city" in c]
    # get most common locations
    countries = []
    regions = []

    for gpe in gpes:
        if not gpe:
            continue
        country_match = matches.loc[
            matches.loc[:, country_features].isin(gpe).any(axis=1), "country_name"
        ]
        region_match = matches.loc[
            matches.loc[:, region_features].isin(gpe).any(axis=1),
            ["country_name", "region_name"],
        ]
        city_match = matches.loc[
            matches.loc[:, city_features].isin(gpe).any(axis=1),
            ["country_name", "region_name"],
        ]
        countries.extend(
            pandas.concat(
                [country_match, region_match.country_name, city_match.country_name]
            )
            .drop_duplicates()
            .tolist()
        )
        regions.extend(
            [
                r
                for r in pandas.concat(
                    [region_match.region_name, city_match.region_name]
                )
                .drop_duplicates()
                .tolist()
                if r not in regions
            ]
        )
    # filter gazetteer by most common
    if not countries:
        return [
            dict(country_name=None, region_name=None, city_name=None, coordinates=None)
        ]

    if not regions:
        return [
            dict(
                country_name=find_most_common(countries)[0].title(),
                region_name=None,
                city_name=None,
                coordinates=None,
            )
        ]
    # get most common
    most_common_country = find_most_common(countries)
    most_common_region = find_most_common(regions)
    common = matches.loc[
        matches.country_name.isin(most_common_country)
        & matches.region_name.isin(most_common_region),
        :,
    ]
    # get cities
    result = []
    for gpe in gpes:
        if not gpe:
            result.append(None)
            continue
        mask = common.loc[:, city_features].isin(gpe).any(axis=1)
        cities_ = common.loc[
            mask, ("country_name", "region_name", "city_name", "coordinates")
        ]
        regions_ = common.loc[
            common.loc[:, region_features].isin(gpe).any(axis=1),
            ("country_name", "region_name"),
        ].drop_duplicates()
        regions_["city_name"] = None
        regions_["coordinates"] = None
        result.append(
            cities_.to_dict(orient="records")
            if cities_.city_name.any()
            else regions_.to_dict(orient="records")
        )
    return result
