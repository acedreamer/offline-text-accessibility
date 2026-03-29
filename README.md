# SimplifyAI - Offline Text Accessibility Tool

**Privacy-preserving, AI-powered text simplification for neurodivergent readers**

A desktop application that uses fine-tuned T5 transformer models to simplify text for dyslexia, ADHD, and autism accessibility needs. Runs completely offline on your local CPU—no cloud, no data sharing, no internet required.

---

## 🚀 Quick Start

### Desktop App (Recommended)

```bash
# Install dependencies
npm install

# Start the application
npm run start
```

This launches the Electron app with Vite dev server. For production build, use `npm run build`.

### Command Line

```bash
# Install Python dependencies
pip install transformers torch spacy
python -m spacy download en_core_web_sm

# Run simplification
python simplify.py --input sample.txt --mode dyslexia --metrics
```

---

## ✨ Features

### Three Accessibility Modes

| Mode | Best For | Key Features |
|------|----------|--------------|
| **Dyslexia** | Readers with dyslexia | Short sentences, visual spacing, optional hyphenation, text-to-speech |
| **ADHD Focus** | Attention maintenance | Progress markers [1/N], bolded key nouns, focus navigation |
| **Literal Clarity** | Autism spectrum | Idiom replacement, jargon simplification, literal interpretations |

### Privacy & Performance

- 🛡️ **100% Offline** – All processing happens locally on your CPU
- ⚡ **Fast** – T5-small model runs efficiently on modern CPUs (~1-2 sec per paragraph)
- 🔒 **No Data Leaves Your Device** – Perfect for sensitive documents
- 📦 **Self-contained** – No external API keys or cloud dependencies

### Accessibility Settings

- **Themes**: Light, Dark, High Contrast (WCAG AAA)
- **Typography**: Choose from Lexend, OpenDyslexic, Merriweather, or Monospace
- **Layout**: Adjustable font size (14-28px), line spacing (1.5-2.0)
- **Motion**: Reduce motion toggle for animations
- **Hyphenation**: Optional for dyslexia (per BDA guidelines)

---

## 🏗️ How It Works

```
Input Text → Preprocessing → Neural Simplification → Mode Formatting → Output
     ↓              (Cleanup)           (T5 + ACCESS)      (Rules-based)      ↓
  Raw text   (Idioms/Jargon/Homophone) Sentence-by-sentence   Dyslexia/ADHD/Autism  Ready-to-read
```

1. **Neural Simplification** (T5 Transformer with ACCESS Control Tokens)
   - Fine-tuned model (`t5/`) on accessibility-focused parallel corpora
   - Preprocessing: Idiom/jargon replacement and homophone correction
   - Sentence-level processing with ACCESS control tokens for mode-specific guidance
   - Dynamic length constraints prevent over-summarization
   - Handles spelling, grammar, and vocabulary simplification

2. **Rule-Based Post-Processing**
   - **Dyslexia**: Split on conjunctions, ensure punctuation, optional hyphenation
   - **ADHD**: Bold first noun per sentence, add [1/N] markers
   - **Autism**: Replace idioms with literal meanings, simplify jargon

3. **Readability Metrics**
   - Word count, sentence length, Flesch Reading Ease
   - Before/after comparison for measurable improvements

---

## 🎯 Mode Details

### Dyslexia Mode

- Breaks complex sentences into short, single-idea statements
- One sentence per line with extra spacing
- Optional hyphenation for long words (disabled by default per BDA guidelines)
- Built-in text-to-speech with word boundary tracking
- Highlights paragraph as it reads aloud

### ADHD Focus Mode

- Converts paragraphs into a numbered bullet list: `[1/15] - Sentence...`
- **Visual emphasis**: First significant noun in each sentence is **bolded**
- Uses spaCy POS tagging for accurate noun detection (with fallback heuristics)
- Keyboard navigation: arrow keys to cycle through sentences
- Active sentence highlighting in the center of the viewport

### Autism/Literal Clarity Mode

- **Idiom replacement**: "break a leg" → "good luck"
- **Jargon simplification**: "PTSD" → "Post-Traumatic Stress Disorder"
- **Context awareness**: Prevents over-replacement
  - Example: "He broke his leg" (literal injury) is NOT replaced with "good luck"
- 5,200+ idioms and 2,000+ jargon terms (morphologically expanded)
- Bolded replacements for easy identification

---

## 📦 What's Included

```
offline-text-accessibility/
├── simplify.py           # Core simplification engine (CLI)
├── simplify_server.py    # Persistent server for Electron
├── dyslexia_mode.py      # Dyslexia formatter
├── adhd_mode.py          # ADHD focus formatter
├── autism_mode.py        # Literal clarity formatter
├── utils.py              # Utilities: sentence splitting, metrics, homophones
├── nlp_utils.py          # spaCy integration (POS tagging, noun extraction)
├── idiom_map.json        # 5,207 idiom → literal mappings
├── jargon_map.json       # 2,054 jargon → plain language mappings
├── electron-app/         # Desktop UI (React + Electron)
│   ├── main.js
│   ├── preload.js
│   └── src/
│       ├── App.jsx
│       ├── context/
│       └── components/
├── t5/        # Fine-tuned T5 model (local)
├── expand_maps.py        # Utility: expand maps with morphological variants
├── __tests__/            # Unit tests
└── docs/                 # Additional documentation
```

---

## 🔧 Installation

### Desktop App (Electron)

```bash
# Clone the repository
git clone https://github.com/yourusername/offline-text-accessibility.git
cd offline-text-accessibility

# Install Node.js dependencies
npm install

# (Optional) Install Python dependencies for backend
pip install transformers torch spacy
python -m spacy download en_core_web_sm

# Run the app
npm run start
```

### Python CLI Only

```bash
pip install transformers torch spacy
python -m spacy download en_core_web_sm
```

---

## 🖥️ Using the Desktop App

1. **Paste or type** your text in the left panel
2. **Select a mode**: Dyslexia, ADHD Focus, or Literal Clarity
3. **Click "Simplify Text"**
4. **View results** in the right panel, customized for the selected mode
5. **Adjust settings** (gear icon):
   - Change theme (light/dark/high-contrast)
   - Select font (Lexend, OpenDyslexic, etc.)
   - Adjust font size and line spacing
   - Enable/disable hyphenation (dyslexia)
   - Reduce motion (accessibility)

---

## 📊 Readability Metrics

The tool calculates and displays:

- **Word count** – before and after simplification
- **Average sentence length** – target: shorter is better
- **Flesch Reading Ease** – 0-100 score (higher = easier to read)

All changes are color-coded: green for improvement, red for regression.

---

## 🛠️ For Developers

### Architecture

The application consists of three layers:

1. **Frontend** – React UI with Electron shell
   - State managed via React Context (AppContext, ThemeContext)
   - IPC communication with Python backend
   - TailwindCSS for styling with CSS custom properties

2. **Backend** – Python simplification server
   - T5 transformer model (HuggingFace) with ACCESS control token guidance
   - Preprocessing pipeline: Idiom/jargon replacement and homophone correction
   - Sentence-level processing with dynamic length constraints to prevent over-summarization
   - LRU model cache (up to 3 models)
   - JSON-over-stdin/stdout protocol

3. **Models** – Fine-tuned T5 on accessibility data
   - Location: `t5/` (local directory)
   - ACCESS control token profiles for mode-specific guidance
   - Dynamic length constraints and penalties for optimal output
   - Tuned generation parameters (beam search, repetition penalty)
   - Preprocessing-ready design for clean input
### Model Selection

```python
# In simplify.py
model_choice = "small"      # ./t5 (default, fastest)
# or
model_choice = "medium"     # t5-medium (higher quality, more RAM)
# or
model_choice = "auto-task"  # Auto-select based on text complexity
# or
model_choice = "auto-device" # Auto-select based on available RAM
```

---

## 📝 Recent Updates

- **Expanded lexical resources**: Idiom map grown from 220→5,207 entries; jargon map from 100→2,054 entries via morphological expansion
- **Full mode implementation**: All three accessibility modes now fully functional
- **spaCy integration**: Accurate part-of-speech tagging for ADHD noun bolding
- **Improved sentence splitting**: Better handling of abbreviations, decimals, and titles
- **Context-aware homophone correction**: "hole" vs "whole", "knot" vs "not", etc.
- **Comprehensive test suite**: Unit tests for mode formatters and map integrity
- **Detailed documentation**: Architecture deep dive and developer guide

---

## ⚠️ Limitations

- English text only (models trained on English)
- Requires ~2GB RAM for T5-medium (smaller model uses less)
- Not a clinical tool – designed for general accessibility support
- No user studies yet – feedback welcome

---

## 📄 License

MIT

---

## 🙏 Acknowledgments

- T5 model and HuggingFace transformers library
- spaCy for natural language processing
- TailwindCSS for utility-first styling
- The neurodiversity community for feedback and inspiration

---

## 📚 Documentation

- **[Architecture Deep Dive](plan/ARCHITECTURE_DEEP_DIVE.md)** – Comprehensive technical overview
- **CLAUDE.md** – Development guide and project instructions
- **docs/** – Additional evaluation and planning documents

---

*Made with ❤️ for neurodivergent readers. All processing happens on your device. Your text, your privacy.*
