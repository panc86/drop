from core.model import merge_geocodes


def test_merge_predictions():
    data = [
        {"text": "Probe with location"},
        {"text": "Probe without location"},
    ]
    tags = [dict(GPE=["Probe"]), None]
    locations = [[dict(country="Probe", region="Probe")], None]
    result = merge_geocodes(data, tags, locations)
    assert result == [
        {
            "text": "Probe with location",
            "geo": {
                "tags": {"GPE": ["Probe"]},
                "locations": [{"country": "Probe", "region": "Probe"}],
            },
        },
        {"text": "Probe without location", "geo": {"tags": None, "locations": None}},
    ]


def test_merge_predictions_with_missing_locations():
    data = [
        {"text": "probe 1"},
        {"text": "probe 2"},
    ]
    tags = [None, None]
    locations = None
    result = merge_geocodes(data, tags, locations)
    assert result == [
        {"text": "probe 1", "geo": {"tags": None, "locations": None}},
        {"text": "probe 2", "geo": {"tags": None, "locations": None}},
    ]
