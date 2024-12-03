from app.tags import get_gpes, parse_location_tags


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


def test_get_gpes():
    tags = [{"GPE": ["Amlapura City"]}]
    result = get_gpes(tags)
    assert result == [['Amlapura City']]
