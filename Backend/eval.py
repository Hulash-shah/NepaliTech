import json
from pathlib import Path

import sacrebleu

from translator import translate_text

TEST_SET_PATH = Path(__file__).parent / "eval" / "test_set.json"


def load_test_set():
    with open(TEST_SET_PATH, encoding="utf-8") as f:
        return json.load(f)


def run_evaluation():
    test_set = load_test_set()

    hypotheses = []
    references = []
    rows = []

    for item in test_set:
        hypothesis = translate_text(item["source"])
        hypotheses.append(hypothesis)
        references.append(item["reference"])
        rows.append(
            {
                "source": item["source"],
                "reference": item["reference"],
                "hypothesis": hypothesis,
            }
        )

    bleu = sacrebleu.corpus_bleu(hypotheses, [references])
    chrf = sacrebleu.corpus_chrf(hypotheses, [references])

    print(f"{'SOURCE':<70} {'REFERENCE':<40} {'MODEL OUTPUT'}")
    print("-" * 160)
    for row in rows:
        print(f"{row['source']:<70} {row['reference']:<40} {row['hypothesis']}")

    print()
    print(f"Corpus BLEU: {bleu.score:.2f}")
    print(f"Corpus chrF: {chrf.score:.2f}")

    report = {
        "bleu": bleu.score,
        "chrf": chrf.score,
        "rows": rows,
    }
    report_path = Path(__file__).parent / "eval" / "eval_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nSaved detailed results to {report_path}")


if __name__ == "__main__":
    run_evaluation()