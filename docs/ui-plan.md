# UI/UX Implementation Plan — SimplifyAI Electron App

## What the Stitch Designs Tell Us

5 complete screen designs covering every major UI state:

| Screen | What it shows |
|---|---|
| Dashboard 1 | Light theme — main split-pane editor |
| Dashboard 2 | High-contrast theme — same layout, WCAG AAA |
| Dyslexia mode | Dyslexia-specific typography + active sentence highlight |
| ADHD focus mode | Cognitive focus reading (sentence-by-sentence navigation) |
| Settings overlay | Slide-over panel with theme/font/reading controls |

Stitch files are in: `stitch/` (5 folders, each with `screen.png` + `code.html`)

---

## Directory Structure

```
electron-app/
├── main.js                   # Electron main process
├── preload.js                # contextBridge (electronAPI)
├── python-bridge.js          # spawn simplify_server.py
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx              # React entry point
    ├── App.jsx               # Root: theme provider + layout
    ├── index.css             # Tailwind + CSS variables for themes
    │
    ├── context/
    │   ├── ThemeContext.jsx  # light | dark | high-contrast
    │   └── AppContext.jsx    # global state (mode, text, result, settings)
    │
    ├── components/
    │   ├── layout/
    │   │   ├── Header.jsx        # Toolbar: logo, mode selector, simplify btn
    │   │   ├── MetricsBar.jsx    # Bottom footer: word/sentence/readability stats
    │   │   └── SettingsPanel.jsx # Slide-over settings overlay
    │   │
    │   ├── editor/
    │   │   ├── InputPanel.jsx    # Left: textarea + formatting toolbar
    │   │   └── OutputPanel.jsx   # Right: result display, copy, PDF
    │   │
    │   ├── modes/
    │   │   ├── DyslexiaOutput.jsx   # Paragraph rendering with dyslexia CSS
    │   │   ├── ADHDFocusMode.jsx    # Sentence-by-sentence navigator
    │   │   └── AutismOutput.jsx     # Clean literal output rendering
    │   │
    │   └── ui/
    │       ├── ModeSelector.jsx    # Dropdown: ADHD / Dyslexia / Autism
    │       ├── ThemeSwitcher.jsx   # 3-option visual picker (in settings)
    │       ├── Toggle.jsx          # Reusable ARIA toggle switch
    │       ├── MetricBadge.jsx     # "450 → 320 -28%" display unit
    │       └── StatusDot.jsx       # Pulsing green "AI Ready" indicator
```

---

## Global State (AppContext)

```js
{
  // Input/Output
  inputText: "",
  outputText: "",
  isLoading: false,

  // Mode
  mode: "dyslexia",           // "dyslexia" | "adhd" | "autism"

  // Metrics (from Python response)
  metrics: {
    before: { word_count, avg_sentence_length, flesch_reading_ease },
    after:  { word_count, avg_sentence_length, flesch_reading_ease }
  },

  // Cognitive Focus (ADHD mode reading)
  focusMode: false,            // true when in sentence-nav mode
  focusSentenceIndex: 0,       // current highlighted sentence
  sentences: [],               // outputText split into sentences

  // Settings
  settings: {
    theme: "light",            // "light" | "dark" | "high-contrast"
    fontFamily: "lexend",      // "lexend" | "opendyslexic" | "merriweather" | "mono"
    fontSize: 18,              // 14–28px
    lineSpacing: "standard",   // "standard" | "relaxed" | "wide"
    cogFocusMode: true,
    reduceMotion: false,
  }
}
```

---

## Theme System

Use CSS custom properties per theme class on `<html>`. Tailwind reads these variables.

**`index.css`:**
```css
:root {
  --color-bg: #f6f6f8;
  --color-surface: #ffffff;
  --color-primary: #135bec;
  --color-text: #0f172a;
  --color-muted: #64748b;
  --color-border: #e2e8f0;
  --color-badge-good: #16a34a;
}

html.dark {
  --color-bg: #101622;
  --color-surface: #1e2635;
  --color-text: #f1f5f9;
  --color-border: #334155;
}

html.high-contrast {
  --color-bg: #000000;
  --color-surface: #000000;
  --color-primary: #ffff00;
  --color-text: #ffffff;
  --color-border: #ffffff;
  --color-badge-good: #ffff00;
  font-weight: 700;
}
```

`ThemeContext` sets the class on `document.documentElement` when theme changes.

---

## Component Details

### `Header.jsx`
Reference: `stitch/local_ai_text_simplifier_dashboard_1/` + `dashboard_2/`

```
[Logo + Icon] [MODE: dropdown▾]          [✦ Simplify Text] [⚙] [JD]
```

- Mode selector dropdown: 4 options, shows mode name + icon
- "Simplify Text" calls `handleSimplify()` from AppContext
- Gear icon opens `SettingsPanel` (sets `settingsOpen: true`)
- High-contrast theme: all-caps text, yellow button, square borders

### `InputPanel.jsx`
Reference: `stitch/local_ai_text_simplifier_dashboard_1/` (left panel) + `stitch/dyslexia-friendly_ai_editor_mode/` (left panel)

- `<textarea>` with dynamic class based on mode:
  - Dyslexia: `dyslexia-text` (line-height 1.8, letter-spacing 0.07em, word-spacing 0.15em)
  - Others: standard Lexend text
- Toolbar below: B / I / ≡ buttons + character counter
- "Clear All" button top-right

### `OutputPanel.jsx`
Reference: `stitch/local_ai_text_simplifier_dashboard_1/` (right panel)

- When `isLoading`: show spinner + "Neuro-Adjustments Active" dashed card
- When result exists: render mode-specific output component:
  - Dyslexia → `<DyslexiaOutput />`
  - ADHD → `<ADHDFocusMode />`
  - Autism → `<AutismOutput />`
- Copy button: `navigator.clipboard.writeText(outputText)`
- PDF button: placeholder (`window.print()`)
- Footer: "PROCESSED LOCALLY ON YOUR DEVICE" with shield icon

### `DyslexiaOutput.jsx`
Reference: `stitch/dyslexia-friendly_ai_editor_mode/` (right panel)

- Splits output into paragraphs
- Each paragraph: `<p className="dyslexia-text">`
- Active sentence highlighted with `.active-sentence`:
  ```css
  background: rgba(74,143,227,0.12);
  border-left: 4px solid #4a8fe3;
  padding: 4px 8px;
  border-radius: 4px;
  ```
- "Listen" button → `speechSynthesis.speak()`
- "Copy" button
- Focus Mode progress bar at the bottom (Sentence N of Total)

### `ADHDFocusMode.jsx`
Reference: `stitch/adhd_cognitive_focus_mode/`

Reading navigator — left sidebar (1/3) = dimmed source, right (2/3) = active sentence large.

```
[Source Document sidebar]  |  [Cognitive Focus Active]
Dimmed original text       |  ← Previous   Next →
                           |
                           |  "Focus Layer: Sentence 3 of 5" (floating badge)
```

Logic:
- `sentences = outputText.split(/(?<=[.!?])\s+/)`
- `focusSentenceIndex` tracks current sentence
- Current sentence: `active-sentence` class (opacity 1 + blue highlight)
- All others: `dimmed-text` class (opacity 0.3)
- Previous/Next buttons increment/decrement index
- Badge: green pulse dot + "Sentence {n} of {total}"

### `SettingsPanel.jsx`
Reference: `stitch/accessibility_settings_panel_overlay/`

- Fixed right slide-over, 400px wide
- Closed: `translateX(100%)` → Open: `translateX(0)` (CSS transition)
- Backdrop: `fixed inset-0 bg-black/40 backdrop-blur-sm`, click to close
- ESC key listener to close

Sections:
1. **Display & Theme** — 3 visual mini-buttons (Light / Dark / High Contrast) as aspect-video previews
2. **Typography** — Font Family `<select>` (Lexend / OpenDyslexic / Merriweather / Mono), Font Size `<input type="range">` 14–28px
3. **Reading Assistance** — Cognitive Focus toggle, Reduce Motion toggle, Line Spacing (Standard / Relaxed / Wide)

Footer: "Save and Apply Settings" primary button

### `MetricsBar.jsx`
Reference: `stitch/local_ai_text_simplifier_dashboard_1/` + `dashboard_2/` footers

```
WORD COUNT        SENTENCE COUNT       READABILITY          AI STATUS
450 → 320 -28%   25 → 18  -7          Grade 12 → Grade 7   ● T5-Simplifier Ready
```

- Shows zeros/dashes before first run
- `MetricBadge`: renders `before → after ±delta`
- `StatusDot`: pulsing green dot + "T5-Simplifier Ready"
- High-contrast: yellow bordered box for AI status

---

## IPC Wiring

**`preload.js`:**
```js
contextBridge.exposeInMainWorld('electronAPI', {
  simplify: (payload) => ipcRenderer.invoke('simplify', payload)
})
```

**`handleSimplify()` in AppContext:**
```js
async function handleSimplify() {
  setIsLoading(true)
  const result = await window.electronAPI.simplify({
    text: inputText,
    mode: mode,
    model: "./t5-simplifier"
  })
  setOutputText(result.simplified)
  setMetrics(result.metrics)
  setSentences(result.simplified.split(/(?<=[.!?])\s+/))
  setIsLoading(false)
}
```

**Expected Python JSON response:**
```json
{
  "simplified": "...",
  "metrics": {
    "before": { "word_count": 450, "avg_sentence_length": 18, "flesch_reading_ease": 32 },
    "after":  { "word_count": 320, "avg_sentence_length": 12, "flesch_reading_ease": 61 }
  }
}
```

---

## Key CSS Classes (`index.css`)

```css
.dyslexia-text {
  line-height: 1.8;
  letter-spacing: 0.07em;
  word-spacing: 0.15em;
}

.active-sentence {
  background: rgba(74, 143, 227, 0.12);
  border-left: 4px solid #4a8fe3;
  padding: 4px 8px;
  border-radius: 4px;
}

.dimmed-text {
  opacity: 0.3;
  transition: opacity 0.2s ease;
}

html.high-contrast .active-sentence {
  background: rgba(255, 255, 0, 0.15);
  border-left-color: #ffff00;
}
```

---

## Build Order (Fastest Path to Working Demo)

### Day 1 — Python bridge + Electron scaffold
1. Create `simplify_server.py` — JSON stdin/stdout loop, calls existing `simplify.py`
2. Create `electron-app/` with `package.json`, `vite.config.js`, `main.js`, `preload.js`
3. Install dependencies: `electron`, `react`, `react-dom`, `vite`, `@vitejs/plugin-react`, `tailwindcss`
4. Verify blank React window launches inside Electron

### Day 2 — Core layout, wired to Python
5. `App.jsx` with `AppContext` + `ThemeContext`
6. `Header.jsx` — logo, mode selector, Simplify Text button
7. `InputPanel.jsx` — textarea + character count
8. `OutputPanel.jsx` — split pane, loading state, privacy badge
9. Wire `handleSimplify()` → IPC → Python → display raw output text

### Day 3 — Mode-specific output components
10. `DyslexiaOutput.jsx` — typography classes + active sentence highlight
11. `ADHDFocusMode.jsx` — cognitive focus navigator (prev/next + dimming)
12. `AutismOutput.jsx` — clean paragraph output
13. `MetricsBar.jsx` — wire real Python metrics to display

### Day 4 — Settings panel + theme switching
14. `SettingsPanel.jsx` — slide-over with all 3 sections
15. `ThemeContext` — apply `light/dark/high-contrast` class to `<html>`
16. Font family switching (CSS variable + class on body)
17. Font size slider → `--font-size-body` CSS variable

### Day 5 — Polish + screenshots
18. Loading spinner in OutputPanel
19. Transitions (skip if `reduceMotion` is on)
20. Take screenshots: light theme, high-contrast, ADHD focus mode → for results slide

---

## Notes on Using Stitch HTML

The Stitch HTML uses CDN Tailwind — cannot be pasted directly into Vite+React. Extract:
- Tailwind class strings (all valid in Vite Tailwind)
- Custom CSS classes (`.dyslexia-text`, `.active-sentence`, `.dimmed-text`)
- Color values (`#135bec`, `#f6f6f8`, `#ffff00`, `#000000`)
- Layout structure (header / `grid-cols-2` main / footer) → convert to JSX

Icon set: **Material Symbols Outlined** — add Google Font link in `index.html` template.

---

## Stitch Reference Map

| Component | Stitch file to open |
|---|---|
| Header (light) | `stitch/local_ai_text_simplifier_dashboard_1/code.html` |
| Header (high-contrast) | `stitch/local_ai_text_simplifier_dashboard_2/code.html` |
| InputPanel + OutputPanel | `stitch/local_ai_text_simplifier_dashboard_1/code.html` |
| DyslexiaOutput | `stitch/dyslexia-friendly_ai_editor_mode/code.html` |
| ADHDFocusMode | `stitch/adhd_cognitive_focus_mode/code.html` |
| SettingsPanel | `stitch/accessibility_settings_panel_overlay/code.html` |
| MetricsBar (light) | `stitch/local_ai_text_simplifier_dashboard_1/code.html` (footer) |
| MetricsBar (high-contrast) | `stitch/local_ai_text_simplifier_dashboard_2/code.html` (footer) |
