from lang_detect import detect_language
from Simplifier import simplify_text
from translator import translate_text


def process(text: str) -> dict:
    language = detect_language(text)

    if language == "nepali":
        english_text = translate_text(
            text, source_lang="npi_Deva", target_lang="eng_Latn"
        )
        translation = english_text
    else:
        english_text = text
        translation = translate_text(
            text, source_lang="eng_Latn", target_lang="npi_Deva"
        )

    simple_explanation_en = simplify_text(english_text)
    simple_explanation_ne = translate_text(
        simple_explanation_en, source_lang="eng_Latn", target_lang="npi_Deva"
    )

    return {
        "original": text,
        "detected_language": language,
        "translation": translation,
        "simple_explanation_en": simple_explanation_en,
        "simple_explanation_ne": simple_explanation_ne,
    }


if __name__ == "__main__":
    test_sentences = [
        "Machine learning is a method of teaching computers to learn from data.",
        "मेशिन लर्निंग भनेको कम्प्युटरलाई डाटाबाट सिक्न सिकाउने विधि हो।",
    ]

    for sentence in test_sentences:
        result = process(sentence)
        print("Original:", result["original"])
        print("Detected language:", result["detected_language"])
        print()
        print("Translation")
        print(result["translation"])
        print()
        print("Simple Explanation in English")
        print(result["simple_explanation_en"])
        print()
        print("Simple Explanation in Nepali")
        print(result["simple_explanation_ne"])
        print("=" * 70)