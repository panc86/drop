import re
import string


# regex compilations
user_mentions = re.compile(r"@[A-Za-z0-9_]+\b:?")
ampersand = re.compile(r"\s+&amp;?\s+")
datetimes = re.compile(
    r"\b\d\d?\s*[ap]\.?m\.?\b|\b\d\d?:\d\d\s*[ap]\.?m\.?\b|\b\d\d?:\d\d:\d\d\b|\b\d\d?:\d\d\b",
    flags=re.IGNORECASE,
)
url = re.compile(r"\bhttps?:\S+", flags=re.IGNORECASE)
url_broken = re.compile(r"\s+https?$", flags=re.IGNORECASE)
special_chars = re.compile(r'[^\w\d\s:\'",.\(\)#@\?!\/’_]+')

# remove !"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ from text
# Notes: underscores are required to highlight normalization tags
punct = string.punctuation.replace("_", "")
more_than_two_whitespaces = re.compile(r"\s{2,}")


def anonymize(text: str) -> str:
    """Remove user mentions from text."""
    return user_mentions.sub("", text)


def normalize_ampersand(text: str) -> str:
    """Replace ampersand symbol with `and`."""
    return ampersand.sub(" and ", text)


def normalize_hashtags(text: str) -> str:
    """Remove hash symbol from hashtag."""
    return text.replace("#", "")


def remove_datetimes(text: str) -> str:
    """Replace dates with spaces."""
    return datetimes.sub(" ", text)


def normalize_url(text: str) -> str:
    """Replace URL with tag `_url_`."""
    return url.sub("_url_", text)


def normalize_url_broken(text: str) -> str:
    return url_broken.sub(" _url_", text)


def normalize_new_lines(text: str) -> str:
    """Replace newline chars with spaces."""
    return text.replace("\r", " ").replace("\n", "")


def remove_special_chars(text: str) -> str:
    return special_chars.sub("", text)


def remove_quotes(text: str) -> str:
    return text.replace("'", "").replace('"', "")


def remove_backslashes(text: str) -> str:
    return text.replace("\\\\", "")


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans(punct, " " * len(punct))).strip()


def normalize_more_than_two_whitespaces(text: str) -> str:
    return more_than_two_whitespaces.sub(" ", text).strip()


def normalize_url_tag(text: str) -> str:
    if "_url_" in text:
        text = " ".join([text.replace("_url_", ""), "_urlincl_"])
    return text


def merge_neighbouring_word_duplicates(text: str) -> str:
    def merge(text: str) -> str:
        g = ""
        prev = None
        words = text.split()
        for word in words:
            if not prev:
                # cache first word
                g = prev = word
                continue
            if word != prev:
                # update only if new word
                g += " " + word
                prev = word
        return g
    return merge(text)


def lowercase(text: str) -> str:
    return text.lower()


# normalization functions
normalizers = (
    anonymize,
    normalize_ampersand,
    normalize_hashtags,
    remove_datetimes,
    normalize_url,
    normalize_url_broken,
    normalize_url_tag,
    normalize_new_lines,
    remove_special_chars,
    remove_quotes,
    remove_backslashes,
    remove_punctuation,
    normalize_more_than_two_whitespaces,
    merge_neighbouring_word_duplicates,
    lowercase,
)


def clean_text(text: str) -> str:
    for normalize in normalizers:
        text = normalize(text)
    return text

