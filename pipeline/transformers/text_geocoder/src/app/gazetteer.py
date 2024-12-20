from collections import Counter
from typing import Iterable

import pandas


class GeocoderError(Exception):
    pass


class OutOfBoundError(Exception):
    pass


def load_gazetteer(
    filepath: str = "https://github.com/panc86/gazetteer/releases/download/v0.3.0/gazetteer.json.zip",
) -> pandas.DataFrame:
    g = pandas.read_json(filepath, orient="records", lines=True).dropna(
        axis=1, how="all"
    )
    g = g.rename(columns={"name_0": "country_name", "region_name_1": "region_name"})
    # title location names for 1:1 matching
    names = [f for f in g if "name" in f]
    g.loc[:, names] = g.loc[:, names].apply(lambda s: s.str.title())
    # verify coordinates
    if "latitude" not in g and "longitude" not in g:
        raise GeocoderError("Missing latitude/longitude fields")
    # format coordinates
    g["coordinates"] = [
        dict(lat=lat, lon=lon) for lat, lon in zip(g.latitude, g.longitude)
    ]
    return g


def find_most_common(locations: Iterable[str]) -> Iterable[str]:
    # get locations with maximum frequency
    count = Counter(locations)
    max_count = max(count.values())
    return [item for item, freq in count.items() if freq == max_count]


def match_geo_political_entities(
    gpes: Iterable[str], gazetteer: pandas.DataFrame
) -> Iterable[dict] | None:
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
    if not countries or not regions:
        return

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
    return result or None
