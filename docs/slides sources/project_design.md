# Project Design Context

This project is an offline, privacy-preserving AI text simplification tool with a
full-stack architecture: a Python backend and an Electron/React desktop frontend.

## Scope and Mode Support

The system supports three accessibility-oriented modes through a unified architecture.
All three modes are fully implemented in both the Python backend and the React frontend.

Implemented modes:
- Dyslexia (sentence simplification, hyphenation, one-sentence-per-line, dyslexia typography)
- ADHD (progress markers, bullet formatting, key term bolding, cognitive focus navigator)
- Autism (idiom replacement with literal meanings, clean paragraph output)

## ADHD Mode

ADHD mode formats simplified text to reduce cognitive load and help users maintain
attention. Python backend features (`adhd_mode.py`):

- Progress markers: Each sentence is prefixed with `[i/N]` where N is the total
  sentence count. This gives users a concrete sense of how far through the text they are.
- Bullet-style layout: One sentence per line, visually chunked.
- Key term bolding: The first significant content word in each sentence is wrapped in
  `**bold**` markers to anchor the reader's attention.

Frontend (`ADHDFocusMode.jsx`): A cognitive focus reading navigator where a sidebar
shows the dimmed source document and the main panel shows the active sentence enlarged,
with Previous/Next navigation buttons and a "Sentence N of Total" badge.

## Autism Mode

Autism mode targets literal interpretation by replacing figurative and idiomatic
language with explicit, unambiguous alternatives. Python backend features (`autism_mode.py`):

- Idiom replacement: A curated dictionary of 20 common English idioms is applied
  via regex, replacing each with its literal meaning.
  Example: "piece of cake" → "easy", "under the weather" → "feeling sick"
- Case-insensitive matching with word-boundary constraints to avoid false positives.

Frontend (`AutismOutput.jsx`): Clean paragraph rendering of the literal output.

## Model Selection

The CLI supports four model selection strategies via `--model`:

- `small` (default): Uses the fine-tuned `./t5-simplifier` local model. Fast, CPU-friendly.
- `medium`: Uses `t5-medium` from HuggingFace Hub. Better quality, slower.
- `auto-task`: Selects model based on text complexity (avg word length, token count).
- `auto-device`: Selects model based on available system RAM via `psutil`.

## Core Constraints

- Must run fully offline
- CPU-only inference
- T5-based text simplification
- CLI tool + Electron desktop app (both implemented)
- Sentence-by-sentence output in Dyslexia mode

## Architecture

```
User Input (Electron UI or CLI)
        │
        ▼
simplify_server.py (JSON stdin/stdout bridge)
        │
        ▼
simplify.py (model loading, T5 inference, mode dispatch)
        │
        ├── dyslexia_mode.py
        ├── adhd_mode.py
        └── autism_mode.py
                │
                ▼
        utils.py (split_sentences, compute_metrics, print_metrics)
```

- Shared AI simplification core (`simplify_with_t5`)
- Mode-specific post-processing (separate files per mode)
- No cloud calls
- Electron frontend communicates with Python via IPC → `python-bridge.js` → spawns `simplify_server.py`

## T5 Task Conditioning Strategy

Text simplification uses a fine-tuned T5-small model (`./t5-simplifier/`).
The model was fine-tuned on a filtered subset of GEM/wiki_auto_asset_turk with the
`simplify:` task prefix. Data curation was critical: raw WikiLarge contains many
near-identical pairs (source ≈ target), so we filtered for pairs with <80% word
overlap, enforcing that the target is shorter and meaningfully different. This teaches
the model actual simplification patterns rather than copying.

## Dyslexia-Oriented Linguistic Heuristics

Following neural simplification, rule-based post-processing is applied to optimize
readability for dyslexic users (`dyslexia_mode.py`). These heuristics include:

- Splitting compound sentences into single-idea statements
- One sentence per line with additional spacing
- Conservative punctuation and capitalization

These heuristics are intentionally simple and transparent, aligning with accessibility
writing guidelines and avoiding opaque transformations.

## Electron Frontend

A full desktop application built with Electron + React + Vite + Tailwind CSS.

Key UI features:
- Split-pane editor: input (left) / output (right)
- Three theme modes: Light, Dark, High-Contrast (WCAG AAA)
- Mode-specific output renderers per accessibility mode
- Settings panel: font family (Lexend, OpenDyslexic, Merriweather, Mono), font size,
  line spacing, cognitive focus toggle, reduce motion
- Metrics bar: word count, sentence count, readability grade before/after
- Privacy badge: "Processed Locally On Your Device"
- Text-to-speech via Web Speech API in DyslexiaOutput

IPC wiring: `preload.js` exposes `window.electronAPI.simplify(payload)` which routes
via `main.js` → `python-bridge.js` → `simplify_server.py` over stdin/stdout JSON.
