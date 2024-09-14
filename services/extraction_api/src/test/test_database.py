from api import database


def test_database_build_payload():
    data = [dict(id=1234, executed=False, tag="test")]
    result = database.build_payload(data)
    assert (
        '{"index": {"_id": 1234}}\n{"id": 1234, "executed": false, "tag": "test"}\n'
    ) == result
