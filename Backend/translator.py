

from functools import lru_cache
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = "facebook/nllb-200-distilled-600M"

# NLLB uses FLORES-200 language codes, not ISO 639-1.
LANG_CODES = {
    "english": "eng_Latn",
    "nepali": "npi_Deva",
}


@lru_cache(maxsize=1)
def _load_model_and_tokenizer(src_lang: str):
   
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME, src_lang=src_lang
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model


def translate_text(
    text: str,
    source_lang: str = "eng_Latn",
    target_lang: str = "npi_Deva",
) -> str:
  
    if not text or not text.strip():
        return ""

    tokenizer, model = _load_model_and_tokenizer(source_lang)

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

    tokenizer, model = _load_model_and_tokenizer(source_lang)

    inputs = tokenizer(texts, return_tensors="pt", padding=True)
    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
        max_length=512,
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)


if __name__ == "__main__":
    # Quick manual test — run `python translator.py` to sanity-check
    # that the model downloads and produces plausible Nepali output.
    test_sentences = [
        "Machine learning is a method of teaching computers to learn from data.",
        "A neural network is a computational model inspired by the human brain.",
        "An API allows two software systems to communicate with each other.",
    ]

    print(f"Loading model: {MODEL_NAME} (this can take a minute on first run)\n")

    for sentence in test_sentences:
        translation = translate_text(sentence)
        print("EN:", sentence)
        print("NE:", translation)
        print("-" * 60)