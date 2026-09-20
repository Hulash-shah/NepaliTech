import re

DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
LATIN_RE = re.compile(r"[A-Za-z]")


def detect_language(text: str) -> str:
    devanagari_count = len(DEVANAGARI_RE.findall(text))
    latin_count = len(LATIN_RE.findall(text))

    if devanagari_count > latin_count:
        return "nepali"
    return "english"