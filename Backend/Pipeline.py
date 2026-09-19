from Simplifier import simplify_text
from translator import translate_text


def process(text: str) -> dict:
    nepali_translation = translate_text(text)
    simple_explanation_en = simplify_text(text)
    simple_explanation_ne = translate_text(simple_explanation_en)

    return {
        "original": text,
        "nepali_translation": nepali_translation,
        "simple_explanation_en": simple_explanation_en,
        "simple_explanation_ne": simple_explanation_ne,
    }


if __name__ == "__main__":
    test_sentences = [
        "Machine learning is a method of teaching computers to learn from data.",
        "A neural network is a computational model inspired by the human brain.",
    ]

    for sentence in test_sentences:
        result = process(sentence)
        print("English:", result["original"])
        print()
        print("Nepali Translation")
        print(result["nepali_translation"])
        print()
        print("Simple Explanation in English")
        print(result["simple_explanation_en"])
        print()
        print("Simple Explanation in Nepali")
        print(result["simple_explanation_ne"])
        print("=" * 70)