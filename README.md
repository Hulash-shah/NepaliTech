# NepaliTech — Nepali Technical Content Translator & Simplifier

An NLP pipeline that turns technical English text into Nepali translation plus a beginner-friendly Nepali explanation, built as part of a 100 Days Data Science & Machine Learning learning journey at Skill Shikshya.

A plain translator isn't enough for this problem. Technical English often translates into Nepali that is grammatically correct but still hard to follow for a beginner, or mistranslates figurative language (see [Error Analysis](#error-analysis)). This project instead runs translation and explanation as two separate, purpose-built steps.

## How it works

```
                     ┌────────────────────┐
   English or        │  Language          │
   Nepali input  ──▶ │  Detection         │
                     │  (script-based)     │
                     └─────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                            │
          input is English             input is Nepali
                 │                            │
                 │                    translate NE → EN
                 │                            │
                 └─────────────┬──────────────┘
                               │
                        english_text
                               │
                 ┌─────────────┴─────────────┐
                 │                            │
        translate EN → NE              simplify_text()
        (shown as "translation")        (Qwen2.5-Instruct)
                 │                            │
                 │                    simple_explanation_en
                 │                            │
                 │                   translate EN → NE
                 │                            │
                 └─────────────┬──────────────┘
                               ▼
                   { translation, detected_language,
                     simple_explanation_en, simple_explanation_ne }
```

React frontend → FastAPI backend → this pipeline → JSON response back to the frontend.

## Design decisions, and why

**Simplify in English, then translate — not simplify directly in Nepali.**
Small local instruction-tuned LLMs are far more reliable following instructions in English than generating fluent, natural Nepali explanations from scratch. Rather than ask one model to understand a technical concept *and* produce good Nepali at once, the pipeline simplifies in English first, then reuses the already-validated NLLB translator on that output. One translation model, no duplicated logic.

**Two separate models, not one general-purpose one.**
NLLB-200 is purpose-built for translation; it does not follow instructions. Qwen2.5-Instruct follows instructions but is not a dedicated translation model. Rather than compromise on a single model doing both jobs poorly, the pipeline uses each for what it's actually good at.

**Script-based language detection, not a statistical detector.**
Since the project only needs to distinguish English from Nepali, and these use different Unicode scripts (Latin vs. Devanagari), a simple character-range check is more reliable than a general-purpose statistical language detector, which tends to perform poorly on short sentences. This wouldn't generalize to, say, distinguishing Nepali from Hindi (both Devanagari) — but that's out of scope here.

## Tech stack

| Layer | Choice |
|---|---|
| Translation | `facebook/nllb-200-distilled-1.3B` |
| Simplification | `Qwen/Qwen2.5-1.5B-Instruct` |
| Backend | FastAPI |
| Frontend | React (Vite) |
| Linting | Ruff (Python), ESLint (JS) |
| Evaluation | `sacrebleu` (BLEU, chrF) |

## Setup

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
pip install fastapi "uvicorn[standard]" sacrebleu
uvicorn main:app --reload --port 8000
```
First run downloads both models (~8GB combined) from Hugging Face.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit the printed local URL (typically `http://localhost:5173`). The backend must be running for the form to work.

## API reference

**`GET /health`** — liveness check, returns `{"status": "ok"}`.

**`POST /translate`**
```json
// Request
{ "text": "A neural network is the backbone of deep learning." }

// Response
{
  "original": "A neural network is the backbone of deep learning.",
  "detected_language": "english",
  "translation": "न्युरोनल नेटवर्क गहिरो सिकाइको मेरुदण्ड हो।",
  "simple_explanation_en": "...",
  "simple_explanation_ne": "..."
}
```

## Evaluation

Run with:
```bash
python eval.py
```
Scores a 20-sentence hand-built test set (`eval/test_set.json`) spanning ML, data structures, and general CS vocabulary, against hand-written Nepali reference translations.

| Metric | Score |
|---|---|
| chrF | 62.27 |
| BLEU | 24.73 |

**chrF is the more meaningful metric here.** BLEU penalizes valid word-order variation and spelling variants (e.g. मेशिन vs. मेसिन for "machine") as errors, even when a Nepali reader would read them as equivalent — this is a known weakness of BLEU for languages with flexible word order, not a translation quality problem. chrF's character-level scoring is more robust to this and better reflects actual quality on this test set.

## Error analysis

**Idiomatic language is where NLLB fails, and model size matters.**

Input: *"A neural network is the backbone of deep learning."*

| Model | Output | Issue |
|---|---|---|
| `nllb-200-distilled-600M` | "...गहिरो सिकाइको **हड्डीको हड्डी** हो।" | Literal translation of "backbone" as anatomical bone, duplicated into nonsense ("bone of bone") |
| `nllb-200-distilled-1.3B` | "...गहिरो सिकाइको **मेरुदण्ड** हो।" | Correct, idiomatic — मेरुदण्ड (spine) is used figuratively in Nepali the same way "backbone" is in English |

Root cause: idiomatic, figurative phrasing is rarer in parallel training data than literal usage, so smaller models default to the literal (wrong) interpretation. The larger model had enough capacity to learn the figurative pattern. This is a genuine model-capacity effect, not a random difference — reproducible by running the same sentence through both model sizes.

**Practical takeaway:** for a production version of this tool, either (a) always use the larger model despite the latency cost, or (b) add a lightweight terminology/idiom glossary that catches known problem phrases before translation — the original design plan for this project anticipated exactly this need.

## Known limitations

- **Difficulty level selector is currently a no-op.** The UI has a Beginner/Intermediate toggle, but `simplify_text()` doesn't yet take a level parameter — every explanation uses the same fixed prompt.
- **CPU-only inference is slow.** No GPU acceleration; a full request runs three sequential model calls (translate, generate, translate), which can take 20–40+ seconds depending on hardware.
- **Single-sentence input only.** Longer paragraphs aren't split or handled specially.
- **Language detection is English/Nepali only**, by design — see [Design decisions](#design-decisions-and-why).

## Possible future work

- Wire the difficulty level selector into `simplify_text()`'s prompt
- Terminology/idiom glossary pre-processing step
- `pytest` test suite + GitHub Actions CI (ruff, eslint, tests on push)
- Deploy to Hugging Face Spaces (better fit than Vercel, which can't run multi-GB PyTorch models server-side)
- Paragraph-level input support

## Acknowledgements

Built as part of a 100 Days Data Science & Machine Learning apprenticeship at Skill Shikshya.