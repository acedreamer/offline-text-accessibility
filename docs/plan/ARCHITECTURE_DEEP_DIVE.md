# Comprehensive Architectural Deep Dive: SimplifyAI Text Accessibility System

## Project Overview

This is an **Electron + React + Python** desktop application that simplifies text for neurodivergent users with three accessibility modes:

- **Dyslexia**: Short sentences, improved spacing, optional hyphenation, text-to-speech
- **ADHD Focus**: Bulleted list with progress markers [1/N], bolded key nouns
- **Autism/Literal Clarity**: Idiom replacement, jargon simplification, literal interpretations

The system uses a **fine-tuned T5 transformer model** for neural text simplification, combined with rule-based post-processing specific to each mode.

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Electron UI Layer (React)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│  │  Header     │  │  Input      │  │  Output Panel   │   │
│  │  - Mode Sel │  │  Panel       │  │  - Dyslexia     │   │
│  │  - Simplify │  │  - Textarea │  │  - ADHD Focus   │   │
│  │  - Settings │  │             │  │  - Autism       │   │
│  └─────────────┘  └─────────────┘  └─────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         Metrics Bar (Readability stats)             │  │
│  │  Word count, Sentence length, Flesch Reading Ease  │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           Settings Panel (Modal)                    │  │
│  │  - Theme (light/dark/high-contrast)                │  │
│  │  - Font family/size                                │  │
│  │  - Line spacing                                    │  │
│  │  - Hyphenation toggle                              │  │
│  │  - Reduce motion                                   │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                              │
                              │ IPC (invoke 'simplify')
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Electron Main Process (main.js)               │
│  - Spawns Python backend as child process                 │
│  - Handles IPC: ipcMain.handle('simplify', ...)          │
│  - Forwards JSON requests to Python stdin                 │
│  - Parses JSON responses from Python stdout               │
│  - 30-second timeout protection                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ stdin/stdout (JSON lines)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│          Python Backend (simplify_server.py)              │
│  - Preloads T5 model at startup                           │
│  - Listens for JSON: {text, mode, useHyphenation}        │
│  - Calls process_text()                                   │
│  - Returns JSON: {simplified, metrics}                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│          Core Processing (simplify.py)                    │
│  1. Model Selection:                                      │
│     - small: ./t5-simplifier (fine-tuned)                │
│     - medium: t5-medium (base model)                      │
│     - auto-task: based on text complexity                 │
│     - auto-device: based on available RAM                 │
│                                                           │
│  2. Model Caching (LRU, max 3 models):                   │
│     _models = {}                                          │
│     - Loads T5ForConditionalGeneration + tokenizer       │
│     - On cache overflow: removes oldest entry            │
│     - Fallback to smaller model on load failure          │
│                                                           │
│  3. Sentence-Level Simplification:                       │
│     - split_sentences(text) → list of sentences         │
│     - For each sentence:                                 │
│       * Mode-specific prompting:                        │
│         - dyslexia: "correct spelling and simplify: {s}"│
│         - adhd: "simplify keeping all details: {s}"     │
│         - autism: "make literal and clear: {s}"         │
│       * Tokenize with T5 tokenizer                       │
│       * Generate with mode-tuned parameters:             │
│         - length_penalty: dyslexia=1.5, adhd=2.5,       │
│                    autism=1.8                            │
│         - min_length: varies by mode (preserve detail)   │
│         - num_beams=4, no_repeat_ngram_size=3           │
│       * Decode result                                    │
│     - Join simplified sentences                         │
│                                                           │
│  4. Mode-Specific Post-Processing (process_text):        │
│     if mode == dyslexia:                                 │
│       return format_for_dyslexia(simplified, ...)       │
│     elif mode == adhd:                                   │
│       return format_for_adhd(simplified)                │
│     elif mode == autism:                                 │
│       return format_for_autism(simplified)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Component Breakdown

### A. Backend Processing Pipeline

#### 2.1 `simplify.py` - Core Simplification Engine

**Key Functions:**

- **`_select_model(choice, text)`**: Determines which T5 model to use
  - `"small"`: `./t5-simplifier` (local fine-tuned model)
  - `"medium"`: `"t5-medium"` (larger base model from HuggingFace)
  - `"auto-task"`: Analyzes text complexity (avg word length > 6 or >200 words → medium)
  - `"auto-device"`: Checks available RAM via `psutil` (>4GB → medium)
  - Default: `./t5-simplifier`

- **`_load_model(model_name)`**: Smart model caching
  - Checks `_models` dict cache
  - Loads `T5ForConditionalGeneration` and `T5Tokenizer`
  - Sets model to `eval()` mode
  - Cache limit: 3 models (FIFO eviction)
  - On failure: falls back to `./t5-simplifier`

- **`simplify_with_t5(text, model_name, mode)`**: Sentence-by-sentence neural simplification
  - Split text into sentences using `split_sentences()`
  - For each sentence:
    - Apply mode-specific prompt template
    - Tokenize with `max_length=512`
    - Generate with tuned parameters (see table above)
    - Decode with `skip_special_tokens=True`
  - Join results with spaces

- **`process_text(text, mode, model_name, use_hyphenation)`**: Dispatcher
  - Calls `simplify_with_t5()`
  - Then delegates to mode-specific formatter

#### 2.2 `utils.py` - Shared Utilities

**Core Functions:**

1. **`split_sentences(text)`**: Robust sentence boundary detection
   - **Protection mechanisms** (temporary placeholders):
     - Decimals: `(\d)\.(\d)` → `\1<DECIMAL>\2`
     - Ellipsis: `\.{3,}` → `<ELLIPSIS>`
     - Titles (Mr., Mrs., Dr., etc.): appends `<TITLEDOT>`
     - Mid-sentence abbreviations (vs., etc., Jan., St., etc.): `<ABBREVDOT>`
     - a.m./p.m. abbreviations
     - Numbered lists (e.g., "1. First item" → don't split)
   - Split pattern: `([.!?]["\']?\s+)(?=[A-Z])` OR `<ELLIPSIS>\s+`
   - Reconstruct sentences, restoring placeholders
   - Extra pass: `_split_numbered_lists()` to handle consecutive list items

2. **`get_words(text)`**: Word extraction with expansion
   - Expands contractions using dictionary (ain't → am not, etc.)
   - Regex: `\b[a-zA-Z]+(?:[-'][a-zA-Z]+)*\b`
   - Captures hyphenated words and apostrophes

3. **`count_syllables(word)`**: Heuristic algorithm
   - Exception dictionary (queue=1, hour=1, business=2, etc.)
   - Counts vowel groups (non-consecutive vowels count as one)
   - Special handling for:
     - Silent 'e' at end (drops it)
     - 'le' ending (adds 1 syllable)
   - Minimum 1 syllable

4. **`compute_metrics(before, after)`**: Readability metrics
   ```python
   {
     'before': {
       'word_count': int,
       'avg_sentence_length': float,
       'flesch_reading_ease': float
     },
     'after': {...},
     'change': {...}
   }
   ```
   - **Flesch Reading Ease**: `206.835 - (1.015 * avg_sent_len) - (84.6 * avg_syllables_per_word)`
   - Higher score = more readable (range 0-100)

5. **`correct_spelling(text)`**: Context-aware homophone correction
   - Uses `_HOMOPHONE_RULES` dictionary: `(wrong_word, nearby_context) → correct_word`
   - Examples:
     - (`'hole'`, `'world'`) → `'whole'` (context indicates "whole world" not "hole world")
     - (`'knot'`, `'is'`) → `'not'` (detects "knot is" vs "knot of")
     - (`'sea'`, `'from'`) → `'see'` ("from you" → "see you")
   - For each word, checks nearby context (±3 words)
   - Preserves original punctuation and capitalization
   - This is a **rule-based** correction system

#### 2.3 `dyslexia_mode.py` - Sentence Splitting & Hyphenation

**Purpose**: Make text digestible by breaking complex sentences

**Algorithm:**
1. `format_for_dyslexia(simplified_text, split_sentences_func, use_hyphenation)`
2. Call `correct_spelling()` first
3. Split text into sentences using provided splitter
4. For each sentence:
   - `_split_on_conjunctions()`: Split at conjunctions (and, but, or, because, although, etc.)
     - Regex: `\b(and|but|or|...)\b`
     - Removes the conjunction from output
     - Special handling for "often" and "also" as sentence starters
   - Checks compound patterns (black/white, up/down, day/night, etc.):
     - If split parts can be re-merged as compounds, merge with "and"
   - Filters out very short fragments (<2 words)
   - `_capitalize_first()` and `_ensure_sentence_end()` (adds period if missing)
   - If `use_hyphenation=True`: `_hyphenate_text()`
     - Words >6 chars: `_hyphenate_word()`
     - Regex patterns:
       - VC-CV: `([aeiouy][^aeiouy])([^aeiouy][aeiouy])` → `\1-\2` (better → bet-ter)
       - (V-CV pattern commented out to avoid over-hyphenation)
5. Join with double newlines (`\n\n`) - one sentence per paragraph

**Hyphenation rationale**: Per BDA guidelines, hyphenation disrupts word-shape recognition, so **disabled by default**

#### 2.4 `adhd_mode.py` - Focus Mode with Noun Highlighting

**Purpose**: Help users with ADHD maintain focus through visual guidance and progress markers

**Algorithm:**
1. `format_for_adhd(text)`
2. Call `correct_spelling()` first
3. Split into sentences (standard `split_sentences()`)
4. For each sentence `[i/N]`:
   - `_bold_first_noun(sentence)`: Bolds the first significant content noun
     - **Primary**: Uses spaCy POS tagging via `nlp_utils.get_first_noun_position()`
       - Loads `en_core_web_sm` model lazily
       - Returns first NOUN or PROPN token with character positions
       - Wraps noun in `**...**` markdown
     - **Fallback**: If spaCy unavailable, uses heuristic:
       - Skip words in `_SKIP_WORDS` list (articles, pronouns, conjunctions, prepositions, auxiliaries, etc.)
       - Find first word >2 chars that's not in skip list
       - Bold it
   - Format: `[{i}/{total}] - {bolded_sentence}`
5. Join with newlines (one bullet per line)

**ADHD-specific behavior**: T5 generation uses **`length_penalty=2.5`** (highest) to preserve all details, avoid summarization

#### 2.5 `autism_mode.py` - Literal Interpretation & Jargon Simplification

**Purpose**: Replace idioms and academic/medical jargon with plain, literal language

**Data Files:**
- `idiom_map.json`: `{"break a leg": "good luck", "kick the bucket": "die", ...}`
- `jargon_map.json`: `{"ADHD": "Attention Deficit Hyperactivity Disorder", "PTSD": "Post-Traumatic Stress Disorder", ...}`

**Algorithm:**
1. `format_for_autism(text)`
2. `_replace_idioms()` with **per-match context awareness**:
   - Loads idiom map lazily (`_load_idiom_map()`)
   - For each idiom: `pattern = r'\b' + re.escape(idiom) + r'\b'`
   - `re.finditer()` with `re.IGNORECASE`
   - For each match: call `_is_idiom_in_context()`
     - Check if context suggests **literal usage** (not idiomatic)
     - Example: "break a leg" with nearby words like "fell", "injury", "hurt", "doctor" → literal (broken leg), don't replace
     - If literal context detected → skip replacement
     - Otherwise → replace with `**literal_meaning**`
3. `_replace_jargon()`:
   - Loads jargon map lazily
   - For each term:
     - If term is ALL CAPS or contains capitals (acronym detection):
       - Pattern: `(?<!\w){term}(?!\w)` (exact standalone match)
     - Else (regular phrase):
       - Pattern: `\b{term}\b` with `re.IGNORECASE`
   - Replace with `**plain_language**`
4. Return final text

**Context awareness**: Prevents over-replacement. Example: "He broke his leg" → doesn't replace "broke his leg" to "good luck" because "leg" and injury context detected.

---

### B. Electron Bridge Layer

#### `electron-app/main.js`

**Responsibilities:**
1. Create Electron `BrowserWindow` (1200×800)
2. **Spawn Python backend** as child process:
   ```javascript
   pythonProcess = spawn('python' or 'python3', ['simplify_server.py'])
   ```
3. **IPC Handler** `ipcMain.handle('simplify', async (event, payload))`:
   - Validates Python process is running
   - Sets up response buffer and `stdout` listener
   - Writes JSON request to Python stdin: `JSON.stringify(payload) + '\n'`
   - **JSON streaming protocol**:
     - Accumulates stdout data
     - Splits on newlines → complete JSON objects
     - Parses each JSON response
     - Removes listener after one response
   - 30-second timeout protection
   - Error handling: rejects promise on error
4. **Lifecycle**:
   - On window close (non-mac): `pythonProcess.kill()`
   - On app quit: ensure Python killed
5. Load UI: either Vite dev server or production `dist/index.html`

**Communication Protocol:**
- Request from React: `window.electronAPI.simplify({text, mode, useHyphenation})`
- Response from Python: `{simplified: "...", metrics: {...}}` or `{error: "..."}`

#### `electron-app/preload.js`

Exposes secure IPC API to renderer:
```javascript
contextBridge.exposeInMainWorld('electronAPI', {
  simplify: (payload) => ipcRenderer.invoke('simplify', payload)
})
```

---

### C. React Frontend

#### State Management: `AppContext.jsx`

**Central state:**
```javascript
{
  inputText, setInputText,
  outputText, setOutputText,
  isLoading, setIsLoading,
  mode, setMode,              // 'dyslexia' | 'adhd' | 'autism'
  metrics, setMetrics,        // before/after metrics
  focusMode, setFocusMode,
  focusSentenceIndex, setFocusSentenceIndex,
  sentences, setSentences,    // array of sentences/paragraphs
  settingsOpen, setSettingsOpen,
  settings: {
    theme,                    // handled mostly by ThemeContext
    fontFamily: 'lexend',
    fontSize: 18,
    lineSpacing: 'standard',
    cogFocusMode: true,
    reduceMotion: false,
    useHyphenation: false
  }
}
```

**`handleSimplify()`:**
1. Validate input exists
2. Set `isLoading = true`
3. Call `window.electronAPI.simplify({ text: inputText, mode, useHyphenation })`
4. On response:
   - Set `outputText`, `metrics`
   - Split into sentences:
     - ADHD mode: `result.simplified.split('\n')` (already formatted with [1/N] markers)
     - Other modes: `result.simplified.split(/(?<=[.!?])\s+/)` (regex sentence split)
   - Set `sentences` array (filtered non-empty)
   - Reset `focusSentenceIndex = 0`
5. On error: display error message
6. Set `isLoading = false`

---

#### Components

**1. Header.jsx**
- Mode selector dropdown (dyslexia, adhd, autism)
- "Simplify Text" button (calls `handleSimplify()`)
- Settings gear icon (opens modal)
- User avatar placeholder

**2. InputPanel.jsx**
- Textarea for input
- Word/char count at bottom
- Clear button (trash icon)
- Dyslexia-specific CSS class when in dyslexia mode

**3. OutputPanel.jsx**
- Conditionally renders mode-specific component:
  - `mode === 'dyslexia'` → `<DyslexiaOutput />`
  - `mode === 'adhd'` → `<ADHDFocusMode />`
  - `mode === 'autism'` → `<AutismOutput />`
- Loading state: spinner with "Processing with local T5 model..."
- Empty state: "Click 'Simplify Text' to see results"
- Copy to clipboard button
- Print/PDF button (`window.print()`)

**4. DyslexiaOutput.jsx**
- Renders paragraphs from `outputText.split('\n')`
- **Text-to-speech feature**:
  - Uses Web Speech API (`SpeechSynthesisUtterance`)
  - Join paragraphs with `\n\n`
  - `onboundary` event → tracks current word/sentence → highlights active paragraph
  - Scrolls active paragraph into view (respecting `reduce-motion`)
  - "Listen"/"Stop" toggle button
- Active paragraph highlighting: background color + left border + pulse animation
- `useEffect` cleanup: cancels speech on unmount/text change

**5. ADHDFocusMode.jsx**
- Displays sentences as numbered bullets: `[1/15] - **Bolded** sentence`
- **Focus navigation**:
  - Arrow keys (Up/Down, Left/Right) → change `focusSentenceIndex`
  - Prev/Next buttons
- **Active sentence** styling: larger, shadow, `active-sentence` class
- **Inactive sentences**: dimmed opacity, hover effect
- Auto-scroll: `useEffect` on `focusSentenceIndex` → `scrollIntoView({behavior: smooth/auto})`
- Keyboard focus handling: `tabIndex={0}` + `onKeyDown`

**6. AutismOutput.jsx**
- Simple paragraph rendering
- Bolded idioms/jargon (markdown `**text**`) parsed via `renderBold()`
- Icon per paragraph (LayoutList)
- Clean, accessible layout

**7. MetricsBar.jsx**
- Displays three metrics side-by-side:
  - **Word Count**: before → after + diff%
  - **Avg Sentence Length**: before → after + diff%
  - **Flesch Reading Ease**: before → after + diff%
- Color coding: green arrows for improvement (higher Flesch score = better; shorter sentences = better), red for regression
- "T5-Simplifier Ready" indicator (green pulsing dot)

**8. SettingsPanel.jsx** (Modal)
- Backdrop with blur
- Three sections:
  1. **Display & Theme**: Light/Dark/High-Contrast buttons (updates `<html>` class via `ThemeContext`)
  2. **Typography**:
     - Font family: Lexend (default), OpenDyslexic, Merriweather, Monospace
       - Applies via `document.body.className = `${fontFamily}-font``
     - Font size slider: 14-28px → sets CSS var `--font-size-body`
     - Hyphenation toggle (dyslexia mode only)
  3. **Reading Assistance**:
     - Line spacing: Standard (1.5), Relaxed (1.8), Wide (2.0)
     - Reduce motion checkbox → adds/removes `reduce-motion` and `no-transition` classes on body
- "Save and Apply Settings" button (closes modal)

**9. ThemeContext.jsx**
- Simple theme provider
- `<html>` class manipulation: removes all, adds `theme` if not 'light'
- `useTheme()` hook exposes `{theme, setTheme}`

---

### D. Model & Data

#### T5 Simplifier Model

Location: `./t5-simplifier/` (local directory, fine-tuned model)

Expected structure:
```
t5-simplifier/
├── config.json
├── generation_config.json
├── model.safetensors (or .bin)
├── tokenizer.json
└── tokenizer_config.json
```

**Fine-tuning for accessibility modes:**
- The prompt templates (`_MODE_PROMPTS`) suggest a single multi-task model fine-tuned on different directives
- Training objective: conditional text simplification with task-specific prompts
- Expected training data: parallel corpora (complex → simple) with mode-specific transformations

**Fine-tuned model behavior:**
- Dyslexia: spelling correction + sentence splitting indication
- ADHD: preserves details, doesn't summarize
- Autism: literal interpretations, explains figurative language

If model missing → errors caught and fallback attempted.

#### Mapping Data (`idiom_map.json`, `jargon_map.json`)

- **Morphologically expanded** (recent work): 5,207 idiom entries (from 220), 2,054 jargon entries (from 100)
- Expansion used:
  - `expand_maps.py`: generates morphological variants (different verb tenses/forms)
  - Uses spaCy + lemminflect for verb conjugation
- Structure:
```json
{
  "idiom": "literal meaning",
  "break a leg": "good luck",
  "__metadata__": {...}
}
```
- `_load_*_map()`: filters out keys starting with `__` (metadata)

---

### E. NLP Utilities (`nlp_utils.py`)

**Lazy spaCy integration:**
- `_get_nlp()`: loads `en_core_web_sm` on first use
- `is_spacy_available()`: checks without loading
- `get_pos_tags(text)`: returns list of `(token, pos_tag)`
- `extract_nouns(text)`: returns all nouns and proper nouns
- `get_first_noun(text)`: returns first noun string
- `get_first_noun_position(text)`: returns `(noun, start_char, end_char)` tuple ← used by `adhd_mode.py`

---

## 3. Data Flow End-to-End

### Complete Request Processing

```
1. User types in InputPanel → setInputText(e.target.value)
   → stored in AppContext.inputText

2. User clicks "Simplify Text" → handleSimplify():
   - set isLoading(true)
   - await window.electronAPI.simplify({text, mode, useHyphenation})

3. Electron main.js IPC handler:
   - Writes JSON to Python stdin
   - Waits for JSON response on stdout
   - Returns to renderer

4. Python simplify_server.py:
   - Reads JSON line
   - process_text() →
     a. simplify_with_t5() (neural)
        - split_sentences()
        - For each sentence: T5 generation with mode prompt
        - join results
     b. mode formatter:
        - dyslexia: split conjunctions, hyphenate, spelling correction
        - adhd: bold first noun, add [1/N] markers
        - autism: idiom/jargon replacement with context awareness
   - compute_metrics(before, after)
   - Print JSON response

5. React receives response:
   - setOutputText(result.simplified)
   - setMetrics(result.metrics)
   - Split into sentences array (different logic for ADHD)
   - setSentences(...)
   - setFocusSentenceIndex(0)
   - set isLoading(false)

6. OutputPanel renders appropriate component:
   - DyslexiaOutput: paragraph rendering with speech synthesis ready
   - ADHDFocusMode: focus mode with navigation
   - AutismOutput: literal interpretation display

7. MetricsBar updates with before/after comparison
```

---

## 4. Key Technical Features

### Model Caching & Memory Management
- LRU cache with size limit 3
- Stored as `(model, tokenizer)` tuple
- On cache overflow: `del _models[oldest_key]` (FIFO)
- Each model ~hundreds of MBs (T5-medium ~2GB RAM required)

### Sentence Splitting Edge Cases
`split_sentences()` handles:
- Titles: "Mr. Smith" → not split after "Mr."
- Abbreviations: "e.g.", "i.e.", "etc.", "vs.", "Jan.", dates
- Ellipsis: "..." → preserve as single unit
- Decimals: "3.14" → protected from splitting
- Numbered lists: "1. First item 2. Second item" → split properly between items
- Sentence continuation: "Dr. Smith said, 'Hello.' Then he left." → splits on period after "Hello"

### Mode-Specific T5 Generation Parameters

| Mode      | length_penalty | min_length                     | repetition_penalty |
|-----------|----------------|--------------------------------|--------------------|
| dyslexia  | 1.5            | max(5, len(sentence)//2)      | 1.1                |
| adhd      | 2.5            | max(20, len(sentence) - 10)   | 1.0                |
| autism    | 1.8            | max(8, len(sentence)//2)      | 1.1                |
| default   | 1.2            | (no explicit min)             | (no penalty)       |

- Higher `length_penalty` → favors longer outputs
- `min_length` ensures certain verbosity preservation

### Context-Aware Idiom Replacement

`_is_idiom_in_context()` uses predefined literal contexts:
```python
_LITERAL_CONTEXTS = {
    'break a leg': ['fell', 'injury', 'hurt', 'broken', 'doctor', ...],
    'kick the bucket': ['water', 'yard', 'bucket', 'spilled', ...],
    ...
}
```
- If any literal context word appears in surrounding 50-char window → skip replacement
- Prevents false positives: "She broke her leg" → doesn't replace with "good luck"

### Accessibility Features

1. **Reduce motion**: `document.body.classList.contains('reduce-motion')` → instant scroll, no animations
2. **High contrast theme**: CSS variables for colors
3. **Font scaling**: `--font-size-body` CSS variable
4. **Line spacing**: dynamic `line-height` styles
5. **Keyboard navigation**: Arrow keys for ADHD focus mode
6. **Speech synthesis**: `SpeechSynthesisUtterance` for dyslexia audio support
7. **Focus visibility**: Active sentence/paragraph highlighting

---

## 5. File Structure Summary

```
chat_editor_mp/
├── simplify.py              # CLI + core simplification logic
├── simplify_server.py       # Persistent daemon for Electron
├── utils.py                 # Utilities: split_sentences, metrics, homophone correction
├── dyslexia_mode.py         # Dyslexia formatter (conjunction splitting, hyphenation)
├── adhd_mode.py             # ADHD formatter (noun bolding, progress markers)
├── autism_mode.py           # Autism formatter (idiom/jargon replacement)
├── nlp_utils.py             # spaCy POS tagging, noun extraction
├── idiom_map.json           # Idiom → literal meaning mappings (5k+ entries)
├── jargon_map.json          # Jargon → plain language mappings (2k+ entries)
├── electron-app/
│   ├── main.js              # Electron main process
│   ├── preload.js           # Context bridge
│   └── src/
│       ├── App.jsx          # Root component
│       ├── index.css        # Tailwind + CSS variables
│       ├── context/
│       │   ├── AppContext.jsx   # Global state
│       │   └── ThemeContext.jsx # Theme state
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
├── t5-simplifier/           # Fine-tuned T5 model (local)
├── __tests__/               # Unit tests
└── docs/                    # Documentation
```

---

## 6. Configuration & Persistence

**Non-persistent settings**: Currently stored only in React state (`AppContext.settings`), reset on app reload. To persist:
- Could use `localStorage` in `SettingsPanel` → on save, write to `localStorage`
- On app init (`AppProvider`), read from `localStorage` and hydrate state

**Theme persistence**: `ThemeContext` could also read/write from `localStorage`

---

## 7. Error Handling & Fallbacks

- **Model load failure**: Falls back to `./t5-simplifier` from `t5-medium`
- **spaCy unavailable** (`adhd_mode.py`): Uses word heuristic (skip-words list)
- **JSON parse errors** (main.js): Buffer cleared, logs error, rejects promise
- **File not found** (utils.py): Exits with error code 1
- **Python process missing**: IPC rejects with "Python process is not running"
- **Timeouts**: 30-second timeout on simplification requests
- **Empty text**: Returns early in multiple places

---

## 8. Performance Considerations

1. **Model loading**: T5 models are large (300MB-2GB). `simplify.py` caches up to 3 models; `simplify_server.py` preloads one model at startup
2. **Sentence-level processing**: Splits text into sentences → processes each separately → avoids OOM on long texts
3. **Transformer max_length**: 512 tokens (standard T5 context)
4. **Generation**: Beam search with 4 beams → 4× compute but better quality
5. **Memory**: Python process holds model in GPU/CPU memory; Electron UI separate
6. **UI responsiveness**: Async IPC → UI doesn't freeze, shows loading spinner

---

## 9. Testing & Metrics

- `compute_metrics()` returns three metrics:
  - Word count (simple count via `get_words()`)
  - Avg sentence length (words / sentences)
  - Flesch Reading Ease (higher = easier to read)

- **Improvement indicators**:
  - Word count ↓ (conciseness) → good
  - Sentence length ↓ (shorter sentences) → good
  - Flesch score ↑ (more readable) → good

Metrics displayed in green for improvements, red for regressions.

---

## 10. Recent Enhancements (from git history)

- **Morphological expansion** of idiom/jargon maps (5-20× growth)
- **Spelling correction** with context-aware homophones
- **Hyphenation toggle** with BDA compliance note
- **Compound pattern detection** in dyslexia mode (preserves pairs like "black and white")
- **spaCy integration** for accurate noun detection in ADHD mode
- **Metrics computation** for quantitative evaluation

---

This system represents a thoughtful integration of **neural text simplification** (T5) with **rule-based accessibility post-processing**, wrapped in a polished **Electron desktop application** with comprehensive **accessibility settings**. The architecture cleanly separates concerns: model inference, mode-specific formatting, UI rendering, and inter-process communication.
