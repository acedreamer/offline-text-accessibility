# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Install dependencies**
  ```bash
  npm install
  ```

- **Start the application (Electron + Vite dev server)**
  ```bash
  npm run start
  ```
  This runs `concurrently "npm run dev" "npm run electron:dev"`:
  - `npm run dev` – Vite dev server for the React UI (http://localhost:5173)
  - `npm run electron:dev` – Launches Electron pointing at the Vite server

- **Run only the UI (for faster iteration when backend is not changing)**
  ```bash
  npm run dev
  ```

- **Run only the Electron binary (uses the last built UI)**
  ```bash
  npm run electron
  ```
  (requires a prior `npm run build` or the Vite dev server running)

- **Build a production Electron app**
  ```bash
  npm run build
  ```
  (creates a distributable in `dist/`; see `package.json` scripts for details)

- **Run the Python backend manually (useful for debugging or CLI use)**
  ```bash
  python simplify.py --input sample.txt --mode dyslexia --metrics
  ```
  or start the server:
  ```bash
  python simplify_server.py
  ```
  then interact via stdin/stdout JSON as defined in the server.

- **Run unit tests (if any exist)**
  The repository does not currently contain a test suite; add tests under `__tests__` or `tests/` and run with `npm test` once configured.

## High‑Level Architecture

- **Entry Point**
  - `electron-app/main.js` – Electron main process. Spawns the Python backend (`simplify_server.py`) as a child process and loads the React UI via `index.html`.

- **UI Layer (React)**
  - Located in `electron-app/src/`.
  - State is managed with React Context:
    - `AppContext.jsx` – holds input/output text, mode, loading flag, metrics, focus handling, and settings (theme, font, line spacing, hyphenation, reduce motion).
    - `ThemeContext.jsx` – provides current theme (light/dark/high-contrast) and a setter.
  - UI components:
    - `Header.jsx` – mode selector, simplify button, settings toggle.
    - `SettingsPanel.jsx` – accessibility settings panel (font, theme, line spacing, hyphenation, reduce motion).
    - `OutputPanel.jsx` – shows simplified result and hosts mode‑specific views:
      - `DyslexiaOutput.jsx`
      - `ADHDFocusMode.jsx`
      - `AutismOutput.jsx`
    - `MetricsBar.jsx` – displays readability metrics before/after simplification.
    - `InputPanel.jsx` – raw text entry area.
  - Styling:
    - Uses TailwindCSS via `@import "tailwindcss";` in `index.css`.
    - Custom CSS variables (`--color-*`, `--font-size-body`) defined in `:root` and updated via `AppContext` when settings change.
    - Theme switching swaps CSS variables on the `html` element (`.dark`, `.high-contrast` classes).

- **Backend (Python)**
  - `simplify.py` – Command‑line interface and core processing logic:
    - Model selection (`_select_model`) based on complexity (`_select_by_task_complexity`) or device RAM (`_select_by_device`).
    - Model caching (`_load_model`) with LRU‑style limit (max 3 models) and error handling with fallback.
    - Sentence‑level T5 simplification (`simplify_with_t5`) using the fine‑tuned T5 model in `t5-simplifier/`.
    - Post‑processing dispatcher (`process_text`) calls the appropriate mode formatter.
  - `simplify_server.py` – Persistent server used by Electron:
    - Loads the model once at start.
    - Accepts JSON lines on stdin: `{ "text": "...", "mode": "...", "useHyphenation": false }`.
    - Returns JSON: `{ "simplified": "...", "metrics": {...} }`.
  - Utility functions (`utils.py`):
    - `read_input_file`, `split_sentences` (handles abbreviations and protects decimals/volume patterns),
    - `get_words` (expands contractions, extracts words and hyphenated terms),
    - `count_syllables` (improved heuristic with silent‑e and `le` handling),
    - `compute_metrics` (word count, average sentence length, Flesch Reading Ease),
    - `print_metrics` (CLI pretty‑print).
  - Mode‑specific formatters:
    - `dyslexia_mode.py` – splits sentences on conjunctions, ensures proper punctuation, optionally applies hyphenation (user‑controlled via `useHyphenation` flag, disabled by default per BDA guidelines).
    - `adhd_mode.py` – splits into sentences, bolds the first significant noun (skip‑word list, verb‑ending heuristic), adds progress markers `[i/N]`.
    - `autism_mode.py` – loads idiom and jargon maps from JSON (`idiom_map.json`, `jargon_map.json`) with fallbacks, replaces idioms (case‑insensitive) and jargon (case‑sensitive for acronyms, case‑insensitive for phrases), bolds replacements.

- **Data Flow**
  1. User types text in `InputPanel.jsx` → stored in `AppContext.inputText`.
  2. Clicking **Simplify Text** triggers `AppContext.handleSimplify`:
     - Calls Electron IPC `window.electronAPI.simplify` with payload `{ text, mode, useHyphenation }`.
     - Electron’s `ipcMain.handle('simplify')` forwards the payload to the Python backend’s stdin.
     - Backend runs `process_text`, returns simplified text + metrics.
     - Electron sends result back via stdout; UI updates `outputText`, `metrics`, `sentences` (for focus modes), and focus index.
  3. `OutputPanel.jsx` renders the appropriate mode component based on `mode`.
  4. `MetricsBar.jsx` reads `metrics` from context and displays before/after values.
  5. Focus‑mode components (`ADHDFocusMode`, `DyslexiaOutput`) use `useEffect` to scroll the active sentence/paragraph into view, respecting the `reduceMotion` setting (instant jump when enabled).

### Important Notes for Future Work

- Settings are persisted in React state only; they reset on reload. To persist across sessions, consider writing to `localStorage` or a config file.
- The Python backend loads the model from the relative path `t5-simplifier/`; ensure that directory contains the fine‑tuned model files (`config.json`, `generation_config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json`).
- When adding new accessibility modes, follow the pattern:
  1. Add a formatter in `*_mode.py` with signature `func(text, ...) -> str`.
  2. Import and wire it in `simplify.py:process_text` and `simplify_server.py:process_text`.
  3. Add a React component in `electron-app/src/components/modes/` and import it in `OutputPanel.jsx`.
  4. Update the mode selector in `Header.jsx` if needed.
- Keep animations and transitions respectful of the `reduceMotion` setting; any new animation should check `document.body.classList.contains('reduce-motion')` and either disable or substitute with a non‑animated alternative.

This should give a clear picture of how to build, run, and extend the codebase. Happy coding!