from core.model import merge_predictions


data = [
    {"id": 32, "text": "probe test no 32"},
    {"id": 33, "text": "probe test no 33"},
    {"id": 34, "text": "probe test no 34"},
]
predictions = {"flood": [0.3, 0.1, 0.2], "impact": [0.1, 0.1, 0.1]}

expected = [
    {"id": 32, "text": "probe test no 32", "annotation": {"flood": 0.3, "impact": 0.1}},
    {"id": 33, "text": "probe test no 33", "annotation": {"flood": 0.1, "impact": 0.1}},
    {"id": 34, "text": "probe test no 34", "annotation": {"flood": 0.2, "impact": 0.1}},
]


def test_merge_predictions():
    flood_pred = [0.3, 0.1, 0.2]
    impact_pred = [0.1, 0.1, 0.1]
    result = merge_predictions(data, impacts=impact_pred, floods=flood_pred)
    assert result == expected
