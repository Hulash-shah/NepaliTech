from functools import lru_cache
import os

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = os.environ.get("NLLB_MODEL", "facebook/nllb-200-distilled-1.3B")

LANG_CODES = {
    "english": "eng_Latn",
    "nepali": "npi_Deva",
}


@lru_cache(maxsize=1)
def _load_model():
    return AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


@lru_cache(maxsize=4)
def _load_tokenizer(src_lang: str):
    return AutoTokenizer.from_pretrained(MODEL_NAME, src_lang=src_lang)


def translate_text(
    text: str,
    source_lang: str = "eng_Latn",
    target_lang: str = "npi_Deva",
) -> str:
    if not text or not text.strip():
        return ""

    tokenizer = _load_tokenizer(source_lang)
    model = _load_model()

    inputs = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
        max_length=512,
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


def translate_batch(
    texts: list[str],
    source_lang: str = "eng_Latn",
    target_lang: str = "npi_Deva",
) -> list[str]:
    if not texts:
        return []

    tokenizer = _load_tokenizer(source_lang)
    model = _load_model()

    inputs = tokenizer(texts, return_tensors="pt", padding=True)
    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
        max_length=512,
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)


if __name__ == "__main__":
    test_sentences = [
        "Machine learning is a method of teaching computers to learn from data.",
        "A neural network is a computational model inspired by the human brain.",
        "An API allows two software systems to communicate with each other.",
    ]

    print(f"Loading model: {MODEL_NAME}")

    for sentence in test_sentences:
        translation = translate_text(sentence)
        print("EN:", sentence)
        print("NE:", translation)
        print("-" * 60)