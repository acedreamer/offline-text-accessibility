# Project Explanation: Offline Text Simplification Tool

## What We Built

A **privacy-first text simplification tool** that helps people with dyslexia, ADHD,
and autism read complex text more easily. The tool runs completely offline on your
laptop — no internet needed, no data sent anywhere.

It ships as both a **CLI tool** (`simplify.py`) and a **full Electron desktop app**
(`electron-app/`) with a React UI, theme switching, and accessibility-first design.

---

## The Problem We're Solving

People with reading difficulties struggle with:
- Long, complex sentences
- Dense paragraphs with multiple ideas
- Technical vocabulary
- Figurative/idiomatic language (autism)
- Distraction and loss of focus mid-reading (ADHD)

Existing solutions (like online AI tools) require sending your documents to the cloud.
This is a privacy problem — you might be simplifying personal emails, medical
documents, homework, or work files.

**Our solution:** Everything stays on your computer.

---

## How It Works

```
Input Text → T5 Neural Simplification → Mode Post-Processing → Output
```

1. **You provide text** (file via CLI, or paste into the Electron app)
2. **T5 model simplifies the language** — shorter words, simpler phrasing
3. **Mode-specific post-processing formats the output** for the user's accessibility need
4. **You see readable output** with metrics showing the improvement

---

## Technical Architecture

```
User Input (Electron UI or CLI)
        │
        ▼
simplify_server.py   ← JSON stdin/stdout bridge for Electron IPC
        │
        ▼
simplify.py          ← model loading, T5 inference, mode dispatch
        │
        ├── dyslexia_mode.py
        ├── adhd_mode.py
        └── autism_mode.py
                │
                ▼
        utils.py     ← split_sentences, compute_metrics, print_metrics
```

### Step 1: Neural Simplification
- Uses **T5-small fine-tuned** on GEM/wiki_auto_asset_turk (`./t5-simplifier/`)
- Runs on CPU only — no GPU required
- `"simplify:"` prefix for task conditioning
- Each sentence is processed individually for better results

### Step 2: Mode-Specific Post-Processing

| Mode | Post-Processing |
|------|----------------|
| `dyslexia` | Split compound sentences, one sentence per line, extra spacing |
| `adhd` | `[i/N]` progress markers, bullet layout, bold first content word |
| `autism` | Replace 20 idioms with literal meanings via regex |

### Step 3: Metrics
Before/after comparison:
- Word count
- Average sentence length
- Flesch Reading Ease score

---

## Model Selection

The `--model` flag (CLI) or `model` payload field (server) controls which model runs:

| Option | Model | When to use |
|--------|-------|-------------|
| `small` (default) | `./t5-simplifier` (fine-tuned local) | Fast, any hardware |
| `medium` | `t5-medium` (HuggingFace Hub) | Better quality, more RAM |
| `auto-task` | Picks based on text complexity | Automatic |
| `auto-device` | Picks based on available RAM | Automatic |

---

## Project Structure

```
chat editor ( mini project )/
├── simplify.py            # CLI tool
├── simplify_server.py     # JSON stdin/stdout server for Electron IPC
├── dyslexia_mode.py       # Dyslexia post-processing
├── adhd_mode.py           # ADHD post-processing
├── autism_mode.py         # Autism idiom replacement
├── utils.py               # Shared utilities (split_sentences, metrics)
├── t5-simplifier/         # Fine-tuned T5-small model weights
├── electron-app/          # Electron + React + Vite desktop app
│   ├── main.js            # Electron main process
│   ├── preload.js         # contextBridge (electronAPI)
│   ├── python-bridge.js   # Spawns simplify_server.py
│   └── src/
│       ├── App.jsx
│       ├── context/
│       │   ├── AppContext.jsx   # Global state
│       │   └── ThemeContext.jsx # Light/dark/high-contrast
│       └── components/
│           ├── layout/
│           │   ├── Header.jsx
│           │   ├── MetricsBar.jsx
│           │   └── SettingsPanel.jsx
│           ├── editor/
│           │   ├── InputPanel.jsx
│           │   └── OutputPanel.jsx
│           └── modes/
│               ├── DyslexiaOutput.jsx
│               ├── ADHDFocusMode.jsx
│               └── AutismOutput.jsx
├── stitch/                # UI design screens (5 reference designs)
└── docs/
    ├── design.md          # Design constraints and decisions
    ├── paper.tex          # Research paper (LaTeX)
    ├── paper.txt          # Research paper (plain text)
    ├── references.bib     # Bibliography
    ├── ui-plan.md         # Electron UI implementation plan
    ├── testing-instructions.md
    └── finetune_colab.ipynb  # Colab notebook for fine-tuning T5
```

---

## How to Use

### CLI

```bash
# Dyslexia mode
python simplify.py --input sample.txt --mode dyslexia

# ADHD mode with metrics
python simplify.py --input sample.txt --mode adhd --metrics

# Autism mode with medium model
python simplify.py --input sample.txt --mode autism --model medium

# Auto model selection
python simplify.py --input sample.txt --mode dyslexia --model auto-device
```

### Electron Desktop App

```bash
cd electron-app
npm run start
```

Launches the Vite dev server and Electron window. The Python server starts automatically.

---

## What Each Mode Does

| Mode | Status | CLI | UI |
|------|--------|-----|----|
| `dyslexia` | Fully implemented | Short sentences, one per line | Dyslexia typography, TTS, active sentence highlight |
| `adhd` | Fully implemented | `[i/N]` markers, bullet list, bold key term | Cognitive focus navigator (prev/next, dimmed context) |
| `autism` | Fully implemented | Idiom → literal replacement | Clean paragraph output |

---

## Design Decisions

### Why T5-small?
- Small enough for CPU inference (~60M parameters)
- Fine-tunable on consumer hardware
- Publicly available, easy to deploy

### Why `"simplify:"` prefix instead of `"summarize:"`?
- Summarization removes information
- Simplification preserves content but makes it easier to read
- For accessibility, we can't lose content

### Why rule-based post-processing?
- Transparent and auditable
- Deterministic (same input = same output)
- Easy to modify without retraining

### Why offline/local?
- Privacy: documents never leave your device
- Works without internet
- No API costs

### Why Electron for the UI?
- Cross-platform desktop app with native OS integration
- Can spawn Python subprocess directly (no web server needed)
- Existing React/Tailwind ecosystem

---

## Limitations (Be Honest About These)

1. **No user studies** — Not tested with actual dyslexic/ADHD/autistic users
2. **English only** — Doesn't work for other languages
3. **T5 imperfections** — Sometimes loses information or makes grammar errors
4. **ADHD/Autism not formally evaluated** — Only Dyslexia mode has quantitative metrics
5. **Autism idiom coverage is limited** — 20 idioms; no coreference resolution

---

## Future Work

1. **User studies** with target participants
2. **Quantitative evaluation** for ADHD and Autism modes
3. **Pronoun/coreference resolution** in Autism mode
4. **Model optimization** — quantization, ONNX export for speed
5. **More languages**

---

## Tech Stack

- **Python 3.x**
- **HuggingFace Transformers** — T5 model
- **textstat** — readability metrics
- **Electron** — desktop app shell
- **React + Vite** — UI framework
- **Tailwind CSS** — styling
- **No external APIs** — everything local

---

## Installation

### Python backend
```bash
pip install transformers torch textstat psutil
```

### Electron app
```bash
cd electron-app
npm install
npm run start
```
