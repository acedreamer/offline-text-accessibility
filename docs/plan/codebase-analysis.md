# SimplifyAI - Comprehensive Codebase Analysis

**Date:** 2026-03-24
**Purpose:** Complete documentation of all files, functions, and their roles
**Audience:** Developers, maintainers, anyone needing to understand or modify the codebase

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [File Hierarchy](#2-file-hierarchy)
3. [Python Backend](#3-python-backend)
4. [Electron Main Process](#4-electron-main-process)
5. [React UI Layer](#5-react-ui-layer)
6. [Data Files](#6-data-files)
7. [Model Artifacts](#7-model-artifacts)
8. [Data Flow](#8-data-flow)
9. [How To Guide](#9-how-to-guide)

---

## 1. Project Overview

**What it is:** A privacy-first text simplification tool for people with dyslexia, ADHD, and autism. Runs completely offline with no data sent to external servers.

**Architecture:** Python backend (T5 model + mode-specific post-processing) + Electron/React frontend with IPC communication.

**Key Design Decisions:**
- Offline-first (everything stays on device)
- Mode-specific accessibility (dyslexia, ADHD, autism)
- Rule-based post-processing (transparent, auditable)
- CPU-only inference (no GPU required)

---

## 2. File Hierarchy

```
F:\chat_editor_mp\
│
├── Python Backend (Root Level)
│   ├── simplify.py              # CLI entry point
│   ├── simplify_server.py       # JSON stdin/stdout server for Electron
│   ├── utils.py                 # Shared utilities
│   ├── dyslexia_mode.py         # Dyslexia post-processing
│   ├── adhd_mode.py             # ADHD post-processing
│   ├── autism_mode.py           # Autism post-processing
│   ├── idiom_map.json           # Idiom → literal meaning mappings
│   └── jargon_map.json          # Jargon → plain language mappings
│
├── Electron App
│   └── electron-app/
│       ├── main.js              # Electron main process
│       ├── preload.js           # Context bridge for IPC
│       ├── index.html           # HTML template
│       ├── package.json         # npm config and dependencies
│       ├── vite.config.js       # Vite bundler config
│       ├── eslint.config.js     # ESLint rules
│       └── src/
│           ├── main.jsx         # React entry point
│           ├── App.jsx          # Root component
│           ├── App.css          # Component CSS (legacy)
│           ├── index.css        # Global styles + Tailwind
│           ├── context/
│           │   ├── AppContext.jsx    # Global application state
│           │   └── ThemeContext.jsx  # Theme switching
│           └── components/
│               ├── layout/
│               │   ├── Header.jsx         # App header with controls
│               │   ├── MetricsBar.jsx     # Readability metrics display
│               │   └── SettingsPanel.jsx  # Accessibility settings modal
│               ├── editor/
│               │   ├── InputPanel.jsx     # Text input area
│               │   └── OutputPanel.jsx    # Simplified output display
│               └── modes/
│                   ├── DyslexiaOutput.jsx # Dyslexia mode renderer
│                   ├── ADHDFocusMode.jsx  # ADHD focus navigator
│                   └── AutismOutput.jsx   # Autism mode renderer
│
├── Model Files
│   ├── t5-simplifier/           # Fine-tuned T5-small model
│   │   ├── config.json
│   │   ├── generation_config.json
│   │   ├── model.safetensors
│   │   ├── tokenizer.json
│   │   ├── tokenizer_config.json
│   │   ├── checkpoint-2500/     # Training checkpoint
│   │   └── checkpoint-5000/     # Training checkpoint
│   └── t5-base/                 # LoRA adapter experiments
│       └── adapter_only/
│
├── Documentation
│   └── docs/
│       ├── design.md
│       ├── project_explanation.md
│       ├── testing-instructions.md
│       └── finetune_colab.ipynb
│
├── Plan Folder (New)
│   └── plan/
│       ├── codebase-analysis.md         # This file
│       └── neurodivergent-improvements-design.md
│
└── UI Design Mockups
    └── stitch/
        └── [5 design folders with code.html and screen.png]
```

---

## 3. Python Backend

### 3.1 simplify.py - CLI Tool

**Location:** `F:\chat_editor_mp\simplify.py`
**Purpose:** Command-line interface for text simplification

#### Functions

| Function | Signature | Description | Use Case |
|----------|-----------|-------------|----------|
| `_select_by_task_complexity` | `(text: str) -> str` | Heuristic: returns "t5-medium" if avg word length >6 or word count >200 | Auto model selection based on text complexity |
| `_select_by_device` | `() -> str` | Uses psutil to check RAM; returns "t5-medium" if >4GB available | Auto model selection based on hardware |
| `_select_model` | `(choice: str, text: str) -> str` | Dispatcher for model selection strategies | CLI `--model` argument handling |
| `_load_model` | `(model_name: str) -> tuple[model, tokenizer]` | Load T5 model with LRU cache (max 3 models) | Efficient model reuse across requests |
| `simplify_with_t5` | `(text: str, model_name: str) -> str` | Sentence-by-sentence T5 inference with beam search | Core neural simplification |
| `process_text` | `(text, mode, model_name, use_hyphenation) -> str` | Orchestrates: T5 simplification → mode-specific formatter | Main processing pipeline |
| `main` | `() -> None` | CLI entry: argparse, file reading, processing, output | Running from terminal |

#### How to Modify

**Change model defaults:**
- Edit `_select_by_task_complexity` thresholds (line ~50)
- Modify `_MAX_MODEL_CACHE_SIZE` (line ~20) to cache more models

**Adjust T5 generation parameters:**
```python
# Around line 115-120
outputs = model.generate(
    inputs["input_ids"],
    max_length=128,      # Change max output length
    num_beams=4,         # Beam search width
    length_penalty=0.8,  # Lower = shorter outputs
    no_repeat_ngram_size=3,
    early_stopping=True,
)
```

---

### 1.2 simplify_server.py - JSON Server

**Location:** `F:\chat_editor_mp\simplify_server.py`
**Purpose:** Persistent server process for Electron IPC communication

#### Protocol

**Input (stdin JSON line):**
```json
{
  "text": "Input text to simplify",
  "mode": "dyslexia",
  "useHyphenation": false,
  "model": "./t5-simplifier"
}
```

**Output (stdout JSON line):**
```json
{
  "simplified": "Simplified text output",
  "metrics": {
    "before": {"word_count": 100, "avg_sentence_length": 15.5, "flesch_reading_ease": 65.2},
    "after": {...},
    "change": {...}
  }
}
```

**Error response:**
```json
{"error": "Error message here"}
```

#### How to Modify

**Add new request field:**
1. Add to JSON parsing section (~line 70)
2. Pass to `process_text()` call
3. Update Electron `main.js` to send the new field

**Change timeout behavior:**
- Timeout is handled in Electron `main.js` (30 seconds), not in Python

---

### 1.3 utils.py - Shared Utilities

**Location:** `F:\chat_editor_mp\utils.py`
**Purpose:** Common text processing and metrics functions

#### Functions

| Function | Signature | Description | Example Use |
|----------|-----------|-------------|-------------|
| `read_input_file` | `(file_path: str) -> str` | Read UTF-8 file, exit on error | CLI input reading |
| `split_sentences` | `(text: str) -> list[str]` | Split on `[.!?]` while protecting abbreviations | All modes use this |
| `get_words` | `(text: str) -> list[str]` | Extract words, expand 159 contractions | Metrics calculation |
| `count_syllables` | `(word: str) -> int` | Heuristic syllable count | Flesch score |
| `compute_avg_sentence_length` | `(text: str) -> float` | Words per sentence | Metrics |
| `compute_flesch_reading_ease` | `(text: str) -> float` | Standard Flesch formula | Metrics |
| `compute_word_count` | `(text: str) -> int` | Word count | Metrics |
| `compute_metrics` | `(before: str, after: str) -> dict` | Full metrics comparison | API response |
| `print_metrics` | `(metrics: dict) -> None` | CLI pretty-print table | Debug output |

#### How to Modify

**Add new abbreviation:**
```python
# Around line 15-25
abbreviations = [
    ...
    "newabbr",  # Add here
]
```

**Add new contraction:**
```python
# Around line 40-170
contractions = {
    ...
    "newcontraction": "expanded form",
}
```

**Add new metric:**
```python
def compute_new_metric(text: str) -> float:
    # Your implementation
    pass

def compute_metrics(before, after):
    return {
        ...
        "new_metric": {
            "before": compute_new_metric(before),
            "after": compute_new_metric(after),
            "change": ...
        }
    }
```

---

### 1.4 dyslexia_mode.py

**Location:** `F:\chat_editor_mp\dyslexia_mode.py`
**Purpose:** Dyslexia-specific post-processing

#### Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `_split_on_conjunctions` | `(sentence: str) -> list[str]` | Split on 32 conjunctions and clause markers |
| `_ensure_sentence_end` | `(sentence: str) -> str` | Add '.' if missing |
| `_capitalize_first` | `(sentence: str) -> str` | Capitalize first letter |
| `_hyphenate_word` | `(word: str) -> str` | VC-CV hyphenation for words >6 chars |
| `_hyphenate_text` | `(text: str) -> str` | Apply hyphenation preserving punctuation |
| `format_for_dyslexia` | `(text, split_sentences_func, use_hyphenation) -> str` | Main formatter |

#### Conjunction List (32 items)
`and, but, or, nor, for, so, yet, which, that, because, although, though, since, unless, until, when, while, where, how, however, moreover, furthermore, nevertheless, nonetheless, consequently, therefore, thus, hence, often, also`

#### How to Modify

**Add new conjunction:**
```python
# Line ~6
pattern = r'\s*,?\s*\b(and|but|or|...|newword)\b\s*'
```

**Change minimum fragment filter:**
```python
# Line ~92
if len(part.split()) < 3:  # Change this threshold
    continue
```

**Adjust hyphenation rules:**
```python
# Line ~50-60
# Rule 1: VC-CV pattern
pattern1 = r'([aeiouy][^aeiouy])([^aeiouy][aeiouy])'
# Rule 2: V-CV pattern
pattern2 = r'([aeiouy])([^aeiouy][aeiouy])'
```

---

### 1.5 adhd_mode.py

**Location:** `F:\chat_editor_mp\adhd_mode.py`
**Purpose:** ADHD-specific focus formatting

#### Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `_bold_first_noun` | `(sentence: str) -> str` | Bold first significant content word |
| `format_for_adhd` | `(text: str) -> str` | Main formatter with `[i/N]` markers |

#### Skip-Words List (27 items)
Articles, prepositions, be-verbs, auxiliaries, common adverbs

**Heuristic logic:**
1. Split sentence into words
2. Skip: articles, prepositions, auxiliaries, pronouns
3. Skip: words ending in `ing`, `ed`, `es`, `s` (verb indicators)
4. Bold first remaining word with length > 2
5. Wrap in `**word**`

#### How to Modify

**Add to skip list:**
```python
# Line ~13-26
skip_words = {
    ...
    "newword",
}
```

**Change verb-ending detection:**
```python
# Line ~40-41
if word.endswith(('ing', 'ed', 'es', 's')) and len(word) > 3:
    # Modify this logic
```

---

### 1.6 autism_mode.py

**Location:** `F:\chat_editor_mp\autism_mode.py`
**Purpose:** Autism-specific idiom and jargon replacement

#### Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `load_idiom_map` | `() -> dict` | Load from JSON or use fallback |
| `load_jargon_map` | `() -> dict` | Load from JSON or use fallback |
| `_replace_idioms` | `(text: str) -> str` | Case-insensitive replacement |
| `_replace_jargon` | `(text: str) -> str` | Case-sensitive for acronyms, case-insensitive for phrases |
| `format_for_autism` | `(text: str) -> str` | Main formatter |

#### Current Idiom Count: 20
#### Current Jargon Count: 20

#### How to Modify

**Add new idiom:**
Edit `idiom_map.json`:
```json
{
  ...
  "new idiom": "literal meaning"
}
```

**Add new jargon:**
Edit `jargon_map.json`:
```json
{
  ...
  "NEWACRONYM": "plain language expansion"
}
```

**Note:** Acronyms (uppercase) are matched case-sensitively. Phrases are case-insensitive.

---

## 4. Electron Main Process

### 4.1 main.js

**Location:** `F:\chat_editor_mp\electron-app\main.js`
**Purpose:** Electron main process - window creation, Python process management, IPC handling

#### Key Components

1. **Window creation** (`createWindow()`)
   - 1200x800 default size
   - Loads Vite dev server or built files

2. **Python process spawning**
   - Spawns `simplify_server.py` as child process
   - Handles stdout/stderr logging
   - Restarts on macOS activation
   - Kills on app quit

3. **IPC Handler** (`ipcMain.handle('simplify', ...)`)
   - Receives payload from renderer
   - Sends JSON + newline to Python stdin
   - Buffers stdout to accumulate complete JSON
   - 30-second timeout
   - Returns parsed response or error

#### How to Modify

**Change window size:**
```javascript
// Line ~20
const mainWindow = new BrowserWindow({
  width: 1200,  // Change here
  height: 800,  // Change here
  ...
});
```

**Adjust timeout:**
```javascript
// Line ~80
const timeout = setTimeout(() => {
  reject(new Error('Request timeout after 30s'));
}, 30000);  // Change milliseconds here
```

---

### 4.2 preload.js

**Location:** `F:\chat_editor_mp\electron-app\preload.js`
**Purpose:** Context bridge exposing safe IPC to renderer

#### Exposed API
```javascript
window.electronAPI.simplify(payload)
```

#### How to Modify

**Add new IPC channel:**
```javascript
// Add to contextBridge.exposeInMainWorld
newFunction: (arg) => ipcRenderer.invoke('new-channel', arg)
```

Then add handler in `main.js`:
```javascript
ipcMain.handle('new-channel', async (event, arg) => {
  // Handle new channel
});
```

---

## 5. React UI Layer

### 5.1 AppContext.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\context\AppContext.jsx`
**Purpose:** Global application state management

#### State Variables

| State | Type | Default | Description |
|-------|------|---------|-------------|
| `inputText` | string | `""` | User's input text |
| `outputText` | string | `""` | Simplified output |
| `isLoading` | boolean | `false` | Processing state |
| `mode` | string | `"dyslexia"` | Current mode |
| `metrics` | object | `{before: {}, after: {}, change: {}}` | Readability metrics |
| `focusMode` | boolean | `false` | (Unused placeholder) |
| `focusSentenceIndex` | number | `0` | ADHD mode active sentence |
| `sentences` | array | `[]` | Split sentences for navigation |
| `settingsOpen` | boolean | `false` | Settings panel visibility |
| `settings` | object | See below | User preferences |

#### Settings Object
```javascript
settings: {
  theme: "light",        // Handled by ThemeContext
  fontFamily: "lexend",  // "lexend" | "opendyslexic" | "merriweather" | "mono"
  fontSize: 18,          // 14-28 pixels
  lineSpacing: "standard", // "standard" | "relaxed" | "wide"
  cogFocusMode: true,    // (Unused)
  reduceMotion: false,   // Disable animations
  useHyphenation: false, // Enable dyslexia hyphenation
}
```

#### How to Modify

**Add new setting:**
1. Add to `settings` initial state
2. Add side effect in `useEffect` if needed
3. Add UI control in `SettingsPanel.jsx`
4. Apply in relevant component

---

### 5.2 ThemeContext.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\context\ThemeContext.jsx`
**Purpose:** Theme switching (light/dark/high-contrast)

#### Themes
- `light` - Default light theme
- `dark` - Dark mode
- `high-contrast` - Yellow on black (WCAG AAA)

#### How to Modify

**Add new theme:**
1. Add CSS variables in `index.css` under new class (e.g., `html.sepia`)
2. Add option in `SettingsPanel.jsx`
3. Add case in `ThemeContext.jsx` effect

---

### 5.3 Header.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\layout\Header.jsx`
**Purpose:** App header with logo, mode selector, simplify button, settings toggle

#### Used State
- `mode`, `setMode` - Mode dropdown
- `isLoading` - Button disabled state
- `handleSimplify` - Button action
- `setSettingsOpen` - Settings button

#### How to Modify

**Change mode options:**
Edit the dropdown options (~line 50-65)

**Change button text/style:**
Modify the "Simplify Text" button (~line 70)

---

### 5.4 SettingsPanel.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\layout\SettingsPanel.jsx`
**Purpose:** Accessibility settings modal

#### Sections
1. **Display & Theme** - Light/Dark/High-Contrast
2. **Typography** - Font family, size, hyphenation
3. **Reading Assistance** - Line spacing, reduce motion

#### How to Modify

**Add new setting:**
1. Add UI control in appropriate section
2. Use `updateSetting('newKey', value)` to save
3. Apply effect in `AppContext.jsx` if needed

---

### 5.5 InputPanel.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\editor\InputPanel.jsx`
**Purpose:** Text input area for source text

#### Used State
- `inputText`, `setInputText` - Text content
- `mode` - Conditional styling for dyslexia

#### Features
- Clear button (trash icon)
- Character/word count display
- Optional `dyslexia-text` CSS class

---

### 5.6 OutputPanel.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\editor\OutputPanel.jsx`
**Purpose:** Container for mode-specific output renderers

#### Used State
- `outputText` - Simplified content
- `isLoading` - Loading overlay
- `mode` - Component selection

#### Features
- Copy to clipboard
- Print button
- Loading overlay with message
- Privacy badge
- Mode-based component routing

---

### 5.7 DyslexiaOutput.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\modes\DyslexiaOutput.jsx`
**Purpose:** Dyslexia-friendly output with text-to-speech

#### Features
- Web Speech API integration
- Paragraph highlighting synced with speech
- Auto-scrolling (respects reduce-motion)
- Listen/Stop toggle

#### How to Modify

**Change speech rate:**
```javascript
// Add around line 30
utterance.rate = 0.9; // 0.5 to 2.0
```

**Change voice:**
```javascript
utterance.voice = speechSynthesis.getVoices().find(v => v.name === 'VoiceName');
```

---

### 5.8 ADHDFocusMode.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\modes\ADHDFocusMode.jsx`
**Purpose:** Cognitive focus navigator - one sentence at a time

#### Features
- `parseLine()` - Extract `[i/N]` markers and bold text
- Keyboard navigation (arrow keys)
- Click to select sentence
- Previous/Next buttons
- Dimmed context for non-active sentences
- Auto-scroll (respects reduce-motion)

#### How to Modify

**Change key bindings:**
```javascript
// Line ~35
if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { ... }
```

**Change dimming level:**
```css
/* index.css */
.dimmed-text {
  opacity: 0.3; /* Change this */
}
```

---

### 5.9 AutismOutput.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\modes\AutismOutput.jsx`
**Purpose:** Clean paragraph output with bolded replacements

#### Features
- `renderBold()` - Split on `**` markers
- Clean typography
- Centered layout

#### How to Modify

**Change replacement highlight color:**
```javascript
// Line ~10
<strong className="text-[var(--color-primary)] font-bold">
// Change to different CSS variable or class
```

---

### 5.10 MetricsBar.jsx

**Location:** `F:\chat_editor_mp\electron-app\src\components\layout\MetricsBar.jsx`
**Purpose:** Display readability metrics before/after

#### Metrics Shown
- Word count
- Average sentence length
- Flesch Reading Ease
- Change badge (green if improved)

---

### 5.11 index.css

**Location:** `F:\chat_editor_mp\electron-app\src\index.css`
**Purpose:** Global styles with CSS variables and Tailwind

#### Key CSS Variables
```css
:root {
  --color-bg: #f6f6f8;
  --color-surface: #ffffff;
  --color-primary: #3b82f6;
  --color-text: #1f2937;
  --color-muted: #6b7280;
  --font-size-body: 18px;
}
```

#### Theme Classes
- `html.light` (default)
- `html.dark`
- `html.high-contrast`

#### Utility Classes
- `.dyslexia-text` - Optimized spacing for dyslexia
- `.reduce-motion` - Disables animations
- `.fade-in`, `.slide-in-up`, `.pulse-subtle` - Animations
- `.lexend-font`, `.opendyslexic-font`, `.merriweather-font`, `.mono-font`

#### How to Modify

**Change theme colors:**
Edit the appropriate `html.dark` or `html.high-contrast` section

**Add new animation:**
```css
@keyframes new-animation {
  from { ... }
  to { ... }
}
.new-animation-class {
  animation: new-animation 0.3s ease-out;
}
```

---

## 6. Data Files

### 6.1 idiom_map.json

**Location:** `F:\chat_editor_mp\idiom_map.json`
**Purpose:** Idiom → literal meaning mappings for Autism mode
**Format:** `{"idiom phrase": "literal meaning", ...}`
**Current Count:** 20 entries

#### Sample Entries
```json
{
  "piece of cake": "easy",
  "break a leg": "good luck",
  "under the weather": "feeling sick"
}
```

---

### 6.2 jargon_map.json

**Location:** `F:\chat_editor_mp\jargon_map.json`
**Purpose:** Jargon → plain language mappings for Autism mode
**Format:** `{"term": "plain language", ...}`
**Current Count:** 20 entries

#### Sample Entries
```json
{
  "MRI": "magnetic resonance imaging",
  "hypertension": "high blood pressure",
  "efficacy": "how well it works"
}
```

---

## 7. Model Artifacts

### 7.1 t5-simplifier/

**Location:** `F:\chat_editor_mp\t5-simplifier\`
**Purpose:** Fine-tuned T5-small model for text simplification

#### Files
| File | Purpose |
|------|---------|
| `config.json` | Model architecture config (hidden_size: 768, layers: 12, heads: 12) |
| `generation_config.json` | Default generation params (overridden by code) |
| `model.safetensors` | Trained weights |
| `tokenizer.json` | SentencePiece tokenizer |
| `tokenizer_config.json` | Tokenizer settings |

#### Training Details
- Dataset: GEM/wiki_auto_asset_turk (filtered for meaningful simplification)
- Prefix: `"simplify: "`
- Checkpoints: 2500, 5000 steps available

---

## 8. Data Flow

### Complete Request Flow

```
1. USER TYPES TEXT
   │
   ▼
2. InputPanel.jsx → setInputText()
   │
   ▼
3. USER CLICKS "Simplify Text"
   │
   ▼
4. AppContext.handleSimplify()
   │
   ▼
5. window.electronAPI.simplify({text, mode, useHyphenation})
   │
   ▼
6. preload.js → ipcRenderer.invoke('simplify', payload)
   │
   ▼
7. main.js → ipcMain.handle('simplify')
   │
   ▼
8. Send JSON to Python stdin: {"text": "...", "mode": "...", ...}
   │
   ▼
9. simplify_server.py receives line
   │
   ▼
10. process_text() called
    │
    ├─► simplify_with_t5() → T5 inference per sentence
    │
    ├─► dyslexia_mode.format_for_dyslexia()
    │   OR adhd_mode.format_for_adhd()
    │   OR autism_mode.format_for_autism()
    │
    └─► compute_metrics(before, after)
    │
    ▼
11. JSON response: {"simplified": "...", "metrics": {...}}
    │
    ▼
12. main.js receives stdout, parses JSON
    │
    ▼
13. AppContext receives result
    │
    ├─► setOutputText(result.simplified)
    ├─► setMetrics(result.metrics)
    └─► setSentences(split result)
    │
    ▼
14. OutputPanel.jsx renders mode-specific component
    │
    ├─► DyslexiaOutput.jsx (with TTS)
    ├─► ADHDFocusMode.jsx (with navigation)
    └─► AutismOutput.jsx (clean paragraphs)
    │
    ▼
15. USER READS SIMPLIFIED OUTPUT
```

---

## 9. How To Guide

### Changing a Button Color

**Example: Change "Simplify Text" button to green**

File: `Header.jsx`
```jsx
// Find the button (~line 70)
<button
  onClick={handleSimplify}
  className="... bg-[var(--color-primary)] ..."  // Change this
>
```

Change to:
```jsx
className="... bg-green-600 hover:bg-green-700 ..."
```

---

### Adding a New Font

**Step 1:** Add font to `index.html`
```html
<link href="https://fonts.googleapis.com/css2?family=NewFont&display=swap" rel="stylesheet">
```

**Step 2:** Add CSS class in `index.css`
```css
.newfont-font {
  font-family: 'NewFont', sans-serif;
}
```

**Step 3:** Add to `SettingsPanel.jsx` dropdown (~line 115)
```jsx
<option value="newfont">NewFont (Custom)</option>
```

**Step 4:** Handle in `AppContext.jsx` useEffect if needed

---

### Adding a New Mode

**Step 1:** Create backend formatter
```python
# new_mode.py
def format_for_new_mode(text: str) -> str:
    # Your processing logic
    return processed_text
```

**Step 2:** Wire into `simplify.py`
```python
# In process_text()
elif mode == "new_mode":
    return format_for_new_mode(simplified)
```

**Step 3:** Wire into `simplify_server.py`
```python
from new_mode import format_for_new_mode
```

**Step 4:** Create React component
```jsx
// NewModeOutput.jsx
export default function NewModeOutput() {
  const { outputText } = useApp();
  return <div>{outputText}</div>;
}
```

**Step 5:** Route in `OutputPanel.jsx`
```jsx
import NewModeOutput from './modes/NewModeOutput';
// ...
{mode === 'new_mode' && <NewModeOutput />}
```

**Step 6:** Add to `Header.jsx` dropdown

---

### Adjusting T5 Model Parameters

**File:** `simplify.py` (~line 115)

```python
outputs = model.generate(
    inputs["input_ids"],
    max_length=128,        # Max output tokens
    num_beams=4,           # Beam search width
    length_penalty=0.8,    # < 1 = shorter outputs
    no_repeat_ngram_size=3,# Prevent repetition
    early_stopping=True,   # Stop when all beams finish
)
```

**To make outputs shorter:** Lower `max_length` or `length_penalty`
**To make outputs longer:** Increase `max_length` or raise `length_penalty` above 1.0
**To improve quality:** Increase `num_beams` (slower)

---

### Expanding the Idiom Dictionary

**File:** `idiom_map.json`

Add new entries following the pattern:
```json
{
  "raining cats and dogs": "raining heavily",
  "hit the sack": "go to sleep",
  "your new idiom": "its literal meaning"
}
```

**Note:** Use lowercase phrases; matching is case-insensitive.
**Note:** Avoid partial idioms that could match incorrectly.

---

## Summary

This codebase implements a complete offline text simplification pipeline with:

1. **Python Backend** - T5 neural simplification + rule-based mode-specific post-processing
2. **Electron Shell** - Desktop app with Python process management
3. **React UI** - Mode-specific output renderers with accessibility features
4. **Multi-modal Support** - Dyslexia, ADHD, and Autism modes
5. **Full Privacy** - Everything runs locally, no data leaves the device

For any modifications, identify the relevant layer (backend, Electron main, React UI) and follow the patterns established in the existing code.

---

*Document created: 2026-03-24*
*Last updated: 2026-03-24*
