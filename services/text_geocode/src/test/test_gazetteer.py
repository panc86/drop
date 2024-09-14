import pandas

from geocode.gazetteer import filter_places_by_buffer


# test gazetteer
g = pandas.DataFrame(
    [
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": "Amlapura City",
            "latitude": -8.44869,
            "longitude": 115.60621,
        },
        {
            "country_name": "Indonesia",
            "region_name": "Bali",
            "city_name": None,
            "latitude": None,
            "longitude": None,
        },
        {
            "country_name": "Italia",
            "region_name": "Puglia",
            "city_name": "Roccacannuccia",
            "latitude": 0,
            "longitude": 0,
        },
    ]
)

def test_filter_places_by_buffer():
    latitude = -8.45
    longitude = 115.61667
    result = filter_places_by_buffer(g, latitude, longitude, radius=50)
    assert len(result) == 1
    assert (result.loc[0, "latitude"] == -8.44869) and (
        result.loc[0, "longitude"] == 115.60621
    )

