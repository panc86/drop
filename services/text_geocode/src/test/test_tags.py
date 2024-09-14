import pandas

from geocode.tags import (
    parse_location_tags,
    match_geo_political_entities,
)


# test gazetteer
g = pandas.DataFrame(
    [
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": "Amlapura City",
            "coordinates": {
                "lat": -8.44869,
                "lon": 115.60621
            }
        },
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": None,
            "coordinates": {
                "lat": None,
                "lon": None
            }
        },
        {
            "country_name": "Italia",
            "region_name": "Puglia",
            "city_name": "Roccacannuccia",
            "coordinates": {
                "lat": 0,
                "lon": 0
            }
        },
    ]
)


def test_return_a_list_type():
    assert isinstance(parse_location_tags([["1"], ["2"]], [["O"], ["O"]]), list)


def test_IO_have_same_length():
    assert len(parse_location_tags([["1"], ["2"]], [["O"], ["O"]])) == 2


def test_return_multiple_tags():
    # titlecase helps DeepPavlov to recognize locations
    tokens, tags = [
        [["Crollo", "In", "Via", "Fasulla", "A", "Rocca", "Cannuccia", ",", "Puglia"]],
        [["O", "O", "B-FAC", "I-FAC", "O", "B-GPE", "I-GPE", "O", "B-GPE"]],
    ]
    expected = [dict(FAC=["Via Fasulla"], GPE=["Rocca Cannuccia", "Puglia"])]
    assert parse_location_tags(tokens, tags) == expected


def test_return_more_than_one_begin_tag_sequentially():
    tokens, tags = [[["Russia", "China", "USA"]], [["B-GPE", "B-GPE", "B-GPE"]]]
    expected = [dict(GPE=["Russia", "China", "USA"])]
    assert parse_location_tags(tokens, tags) == expected


def test_match_geo_political_entities_unfiltered_gazetteer():
    tags = [{"GPE": ["Amlapura City"]}]
    places = match_geo_political_entities(tags, g)
    expected = [[
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": "Amlapura City",
            "coordinates": {
                "lat": -8.44869,
                "lon": 115.60621
            }
        },
    ]]
    assert places == expected


def test_match_geo_political_entities_with_unmatched_GPE():
    tags = [{"GPE": ["Indonesia", "Bali"]}]
    places = match_geo_political_entities(tags, g)
    expected = [[
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": None,
            "coordinates": None
        }
    ]]
    assert places == expected
