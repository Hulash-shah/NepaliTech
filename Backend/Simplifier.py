from functools import lru_cache
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_num_threads(os.cpu_count())

MODEL_NAME = os.environ.get("QWEN_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")

SYSTEM_PROMPT = (
    "You are a patient teacher explaining technical computer science "
    "concepts to a complete beginner. Rewrite the given technical "
    "sentence as a short, simple explanation (2-3 sentences max). "
    "Use everyday language and, if helpful, a simple real-world analogy. "
    "Do not just repeat the original sentence in different words - "
    "actually explain the underlying idea. Do not add greetings or "
    "meta-commentary, just give the explanation."
)


@lru_cache(maxsize=1)
def _load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32,
    )
    return tokenizer, model


def simplify_text(text: str, max_new_tokens: int = 100) -> str:
    if not text or not text.strip():
        return ""

    tokenizer, model = _load_model_and_tokenizer()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]

    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt")

    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )

    new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


if __name__ == "__main__":
    test_sentences = [
        "Machine learning is a method of teaching computers to learn from data.",
        "A neural network is a computational model inspired by the human brain.",
        "An API allows two software systems to communicate with each other.",
    ]

    print(f"Loading model: {MODEL_NAME}")

    for sentence in test_sentences:
        simplified = simplify_text(sentence)
        print("ORIGINAL :", sentence)
        print("SIMPLIFIED:", simplified)
        print("-" * 60)