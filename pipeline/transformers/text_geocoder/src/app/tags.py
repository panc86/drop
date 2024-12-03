from typing import Iterable


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
