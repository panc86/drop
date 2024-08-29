import pandas

# from core.gazetteer import filter_places_by_buffer
from core.gazetteer import match_geo_political_entities


# test gazetteer
g = pandas.DataFrame(
    [
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": "Amlapura City",
            "coordinates": {"lat": -8.44869, "lon": 115.60621},
        },
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": None,
            "coordinates": None,
        },
        {
            "country_name": "Italia",
            "region_name": "Puglia",
            "city_name": "Roccacannuccia",
            "coordinates": {"lat": 0, "lon": 0},
        },
    ]
)
#
# def test_filter_places_by_buffer():
#    latitude = -8.45
#    longitude = 115.61667
#    result = filter_places_by_buffer(g, latitude, longitude, radius=50)
#    assert len(result) == 1
#    assert (result.loc[0, "latitude"] == -8.44869) and (
#        result.loc[0, "longitude"] == 115.60621
#    )


def test_match_geo_political_entities_unfiltered_gazetteer():
    gpes = [["Amlapura City"]]
    places = match_geo_political_entities(gpes, g)
    expected = [
        [
            {
                "country_name": "Indonesia",
                "region_name": "Bali",
                "city_name": "Amlapura City",
                "coordinates": {"lat": -8.44869, "lon": 115.60621},
            },
        ]
    ]
    assert places == expected


def test_match_geo_political_entities_with_unmatched_GPE():
    gpes = [["Indonesia", "Bali"]]
    places = match_geo_political_entities(gpes, g)
    expected = [
        [
            {
                "country_name": "Indonesia",
                "region_name": "Bali",
                "city_name": None,
                "coordinates": None,
            }
        ]
    ]
    assert places == expected
