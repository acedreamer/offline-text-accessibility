# SimplyAI — Presentation Q&A Prep Guide
## Group 3 | COE Kottarakkara

---

## SECTION 1: General Questions (Anyone can answer)

**Q: What is SimplyAI in one sentence?**
**A:** SimplyAI is a privacy-first, fully offline desktop app that uses a fine-tuned AI to simplify complex English text for individuals with Dyslexia, ADHD, and Autism.

**Q: What problem are you solving?**
**A:** Cloud AI tools like ChatGPT require sending your documents to external servers — a privacy risk. We built a system that runs 100% on your device, so sensitive documents never leave your machine.

**Q: Who are your target users?**
**A:** Students and professionals with neurodivergent conditions — dyslexia (reading difficulty), ADHD (focus difficulty), autism (difficulty with idioms/non-literal language).

**Q: What makes this different from a summarizer?**
**A:** Summarization *removes* information. Simplification *retains all content* but restructures it to reduce cognitive load. For accessibility, you cannot afford to lose any content.

**Q: What are the three modes?**
**A:** Dyslexia (readable formatting, one sentence/line), ADHD (progress markers, focus navigator), Autism (idiom → literal replacement).

**Q: What's the innovation here?**
**A:** The pipeline approach — fine-tuned T5 neural simplification + mode-specific rule-based post-processing + a specialized UI that adapts to each cognitive need. No existing offline tool does this combination.

---

## SECTION 2: AI/ML Technical (Abishek / Alfred)

**Q: Why T5-small?**
**A:** 60M parameters — small enough for CPU-only inference on a consumer laptop, but powerful enough for meaningful simplification. No GPU required, which is critical for accessibility.

**Q: Why "simplify:" prefix and not "summarize:"?**
**A:** T5 was trained on summarization, which condenses and *loses* information. We use "simplify:" to condition it to preserve all content while reducing syntactic complexity. Information retention is non-negotiable for accessibility.

**Q: What dataset did you use for fine-tuning?**
**A:** GEM/wiki_auto_asset_turk — high-quality pairs of complex Wikipedia sentences with human-written simplified versions.

**Q: What data filtering did you apply?**
**A:** We filtered for pairs where word overlap was **<80%** (so the model actually learns to change the text) and the target was shorter than the source. Raw WikiLarge has many near-identical pairs that would teach the model to just copy.

**Q: Explain beam search.**
**A:** Instead of picking the single most likely next word (greedy), beam search explores 4 parallel paths simultaneously and selects the one with the highest overall probability. This produces more grammatically coherent output.

**Q: How do you measure simplification quantitatively?**
**A:** Three metrics — word count, average sentence length, and Flesch Reading Ease (FRE). Our test case showed sentence length drop from **29.0 → 7.0 words** and FRE improved by **+17.05 points**.

**Q: Why are FRE scores still negative after simplification?**
**A:** Because the input is highly technical text with multi-syllable words (artificial, intelligence, integrated). FRE penalizes syllables heavily. The absolute value isn't the point — the **+17.05 improvement delta** is what demonstrates the system is working.

**Q: What is auto-device model selection?**
**A:** We use `psutil` to check available system RAM. If RAM is sufficient, we can load t5-medium for better quality. On low-RAM devices, we default to t5-small to prevent crashes.

---

## SECTION 3: Software/Backend (Abishek / Alfred)

**Q: Walk us through the architecture.**
**A:** `User Input → simplify_server.py (JSON IPC listener) → simplify.py (T5 inference + mode dispatch) → dyslexia_mode.py / adhd_mode.py / autism_mode.py → utils.py (metrics)`

**Q: How does Electron talk to Python?**
**A:** The Electron UI calls `window.electronAPI.simplify(payload)` → `preload.js` (contextBridge) → `main.js` → `python-bridge.js` → spawns `simplify_server.py` as a child process → communicates via JSON over stdin/stdout.

**Q: Why JSON stdin/stdout for IPC?**
**A:** It's the simplest, language-agnostic way for Node.js to talk to Python without a web server. Both sides just read/write lines of JSON.

**Q: How is Autism mode implemented technically?**
**A:** A dictionary of 20 common idioms mapped to literal meanings, applied via regex with word-boundary constraints (`\b`) and case-insensitive matching to avoid false positives. E.g., "piece of cake" → "easy", "under the weather" → "feeling sick".

**Q: Why sentence-by-sentence processing?**
**A:** Keeps inputs within the model's context window, enables precise post-processing per sentence (like [i/N] markers), and gives natural boundaries for spacing heuristics.

---

## SECTION 4: Frontend/UI (Karthik)

**Q: Why Electron over a web app?**
**A:** Electron can spawn a Python subprocess directly — no web server needed. It also gives us access to native OS features and works fully offline.

**Q: How is ADHD Focus Navigator implemented?**
**A:** A sidebar shows the full dimmed text (context). The main panel shows only the active sentence, enlarged. Prev/Next buttons navigate sentences and a "Sentence N of Total" badge tracks progress.

**Q: How is TTS implemented?**
**A:** Via the **Web Speech API** — native to the browser/Electron runtime, works completely offline, no external API call.

**Q: What is contextBridge?**
**A:** An Electron security feature. It exposes only specific whitelisted functions (like `simplify`) to the React frontend, instead of giving it full Node.js access — prevents XSS and injection attacks.

**Q: How do themes work?**
**A:** `ThemeContext.jsx` provides a React context with light/dark/high-contrast themes (WCAG AAA compliant). Every component reads from this context, so switching themes re-renders the entire UI instantly.

**Q: Why Vite over Create React App?**
**A:** Vite offers near-instant Hot Module Replacement and significantly faster builds — critical when iterating quickly on complex accessibility UI states.

---

## SECTION 5: Evaluation & Research (Ashish)

**Q: How did you evaluate the project?**
**A:** Quantitatively: Flesch Reading Ease, average sentence length, word count before/after. Qualitatively: checking information retention and grammar correctness manually.

**Q: Did you do user studies?**
**A:** Honestly, no — due to time and ethical constraints. We followed established **WCAG 2.1** accessibility guidelines and the **British Dyslexia Association's Style Guide** as our design validation framework. User studies are our top future work priority.

**Q: What are the limitations?**
**A:** (1) English only. (2) No user studies. (3) T5-small occasionally loses nuance. (4) Autism idiom dictionary limited to 20 entries. (5) FRE still negative on very technical text — though the delta is positive.

**Q: What research supports your design decisions?**
**A:** Rello & Baeza-Yates (2013) on dyslexia-friendly fonts. Siddharthan (2014) survey on text simplification. BDA Style Guide on sentence length and spacing. Raffel et al. (2020) for T5 architecture.

**Q: What's your future work?**
**A:** User studies with actual participants, expanding the idiom dictionary, ONNX export for faster CPU inference, multilingual support.

---

## SECTION 6: Tricky Questions (Whole Team)

**Q: Why not just use ChatGPT?**
**A:** ChatGPT requires internet and sends your data to OpenAI. For someone simplifying a medical document, legal letter, or school assignment, that's a real privacy concern. We solve that.

**Q: Isn't 60M parameters too small?**
**A:** A small model *fine-tuned specifically for one task* often outperforms a large general model on that task. Specialization beats raw size here.

**Q: What if the AI makes a grammar mistake?**
**A:** Beam search (4 beams) minimizes this by choosing the most likely coherent output. We also show the original text side-by-side so users can cross-check. Acknowledged as a known limitation.

**Q: 20 idioms seems too few for Autism mode?**
**A:** This is a proof of concept demonstrating the mechanism. The dictionary is a simple data structure that can be expanded to thousands of entries without changing any code.

**Q: Electron is memory-heavy — why use it?**
**A:** The memory overhead is the cost of getting: cross-platform compatibility, Python subprocess management, TTS via Web Speech API, and a React UI — all in one framework. Worth the trade-off.

**Q: How did you divide work?**
**A:** Abishek — AI fine-tuning, T5 integration, backend core. Alfred — backend modules, idiom research, dataset filtering. Karthik — Electron/React UI, accessibility themes, focus navigator. Ashish — evaluation metrics, paper, documentation, testing.

---

## SECTION 7: Quick-Fire Definitions Cheat Sheet

| Term | Definition |
|------|-----------|
| **T5** | Text-to-Text Transfer Transformer; encoder-decoder model treating all NLP tasks as text-to-text |
| **Beam Search** | Decoding strategy exploring 4 parallel word-sequence paths, picks highest probability |
| **FRE** | Flesch Reading Ease: 206.835 − 1.015×(words/sentences) − 84.6×(syllables/words) |
| **WCAG** | Web Content Accessibility Guidelines — international web accessibility standard |
| **IPC** | Inter-Process Communication — how Electron and Python talk via stdin/stdout |
| **Electron** | Framework for cross-platform desktop apps using Chromium + Node.js |
| **contextBridge** | Electron security API that safely exposes whitelisted functions to the renderer |
| **Task Conditioning** | Using a prefix like "simplify:" to tell T5 which task to perform |
| **psutil** | Python library for reading system RAM/CPU usage |
| **textstat** | Python library for computing readability statistics |
| **GEM** | Benchmark suite for Natural Language Generation |
| **wiki_auto_asset_turk** | High-quality human-verified text simplification dataset |
| **TTS** | Text-to-Speech — converts written text to audio |
| **Fine-tuning** | Further training a pre-trained model on a specific dataset/task |
| **Tokenizer** | Converts raw text to numerical token IDs the model understands |
| **Seq2Seq** | Sequence-to-Sequence — model that maps one word sequence to another |
| **Lexend/OpenDyslexic** | Fonts designed to reduce visual stress for dyslexic readers |
| **Vite** | Fast modern build tool with near-instant Hot Module Replacement |
| **Tailwind CSS** | Utility-first CSS framework for rapid styling |
| **Transformer** | Neural network architecture using self-attention; backbone of T5, GPT, BERT |

---

## Tips for the Day

- If you don't know an answer, say *"That's a great point — in our current prototype we haven't addressed that, but here's how we'd approach it..."* Never bluff.
- Always bring it back to the **core value: privacy + offline + accessibility.**
- Know your numbers: **29.0 → 7.0 words/sentence, +17.05 FRE improvement.**
- The honest limitation answer ("no user studies, but here's our plan") is stronger than dodging it.
