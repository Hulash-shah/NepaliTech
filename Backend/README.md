---
title: NepaliTech Backend
emoji: 🏔️
colorFrom: yellow
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# NepaliTech Backend

FastAPI service that translates technical English into Nepali and generates a simplified Nepali explanation. See `POST /translate` and `GET /health`.

Full project, frontend, and documentation: see the main NepaliTech repository.

## Configuration

Set these as Space Variables (Settings → Variables and secrets) to control which models load:

- `NLLB_MODEL` — default `facebook/nllb-200-distilled-1.3B`. Set to `facebook/nllb-200-distilled-600M` for faster, lighter translation on limited hardware.
- `QWEN_MODEL` — default `Qwen/Qwen2.5-0.5B-Instruct`. Set to `Qwen/Qwen2.5-1.5B-Instruct` for higher-quality explanations if the Space's hardware can handle it.
