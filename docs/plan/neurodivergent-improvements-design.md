# Neurodivergent Improvements Design Document

**Date:** 2026-03-24
**Status:** Draft - Awaiting User Approval
**Chosen Approach:** Cognitive-Load Adaptive System (Approach 1)

---

## Executive Summary

This document outlines a strategic plan to deepen the accessibility features of SimplifyAI for neurodivergent users. After exploring three potential approaches, we recommend implementing a **Cognitive-Load Adaptive System** that provides intensity levels within each mode, respecting that neurodivergence exists on a spectrum.

---

## Current State Analysis

### What's Already Built

| Mode | Backend Features | Frontend Features | Gaps Identified |
|------|------------------|-------------------|-----------------|
| **Dyslexia** | Sentence splitting on conjunctions, optional hyphenation (BDA-compliant default off), double-newline formatting | Web Speech API TTS with paragraph syncing, active highlighting, auto-scroll, dyslexia typography class | Fixed intensity, no letter-spacing options, no reading guide |
| **ADHD** | `[i/N]` progress markers, key-term bolding via skip-word heuristic, sentence-level chunking | Cognitive focus navigator with prev/next buttons, keyboard navigation, dimmed context, active sentence highlight | Simple noun detection heuristic, no pacing options, no working memory aids |
| **Autism** | 20 idiom replacements, 20 jargon replacements, case-sensitive/acronym handling, bolded replacements | Clean paragraph rendering, bold highlighting of changed terms | Small dictionary, no pronoun resolution, no detection of sarcasm/figurative language beyond idioms |

### Key Insight
The foundation is solid, but each mode operates at a single "intensity level." Real neurodivergent users have varying needs day-to-day and task-to-task.

---

## Proposed Approach: Cognitive-Load Adaptive System

### Philosophy
> "Neurodivergence is not binary. Support shouldn't be either."

Instead of one-size-fits-all modes, each mode will offer **multiple intensity levels** that the user can adjust based on:
- Their current cognitive state (tired, focused, overwhelmed)
- The text complexity (casual reading vs. dense academic)
- Their personal preference and learning style

---

## Detailed Mode Enhancements

### 1. Dyslexia Mode Enhancements

#### Three Intensity Levels

| Level | Name | Features |
|-------|------|----------|
| **Light** | Supportive | Basic sentence simplification from T5, standard line spacing, optional TTS |
| **Standard** | Enhanced | Current implementation: conjunction splitting, double newlines, TTS with highlighting |
| **Intensive** | Maximum Support | Aggressive splitting, increased letter-spacing (0.15em), word-spacing (0.25em), bionic reading (bold first letters), reading ruler overlay |

#### Additional Features
- **Reading Ruler:** Horizontal overlay that follows the active line, reducing visual noise above/below
- **Bionic Reading Option:** Bold the first 2-3 letters of each word to guide eye movement (research shows this helps some dyslexic readers)
- **Word Difficulty Tooltip:** On hover over polysyllabic words >7 characters, show definition/pronunciation hint
- **Adjustable TTS Speed:** Slider from 0.5x to 1.5x with voice selection

#### Technical Considerations
- Bionic reading can be implemented client-side with regex: `word.slice(0, Math.ceil(word.length * 0.4))`
- Reading ruler: CSS overlay with `pointer-events: none` that tracks active paragraph
- Letter/word spacing: CSS variables controlled by intensity level

---

### 2. ADHD Mode Enhancements

#### Three Intensity Levels

| Level | Name | Features |
|-------|------|----------|
| **Light** | Guided | Progress markers, standard navigation, minimal dimming |
| **Standard** | Focused | Current implementation: key-term bolding, dimmed context, keyboard nav |
| **Intensive** | Deep Focus | Single-sentence isolation (everything else hidden), optional timer/pacing, ambient progress indicator |

#### Additional Features
- **Working Memory Aid:** Small "context badge" above current sentence showing: "Previous: [summary of last sentence]"
- **Optional Pacing Timer:** Gentle countdown between sentences (user-adjustable, default 0 = off)
- **Chunk Grouping:** Option to view 2-3 sentences together instead of one at a time
- **Completion Celebration:** Subtle visual acknowledgment when finishing a text (confetti animation or progress completion sound)
- **Improved Noun Detection:** Replace heuristic with POS-tagging for more reliable key-term identification

#### Technical Considerations
- POS tagging: Could use `compromise.js` (~200KB) for client-side NLP, or move to backend with spaCy
- Timer: Simple `setTimeout` with visual progress ring
- Memory aid: Requires storing sentence summaries - could be first 30 chars or LLM-generated keyword

---

### 3. Autism Mode Enhancements

#### Three Intensity Levels

| Level | Name | Features |
|-------|------|----------|
| **Light** | Clear | Basic idiom/jargon replacement, standard formatting |
| **Standard** | Explicit | Current: 20 idioms + 20 jargon, bolded replacements |
| **Intensive** | Comprehensive | Expanded dictionary (100+ idioms, 100+ jargon), pronoun resolution, ambiguity flagging, explanation tooltips |

#### Additional Features
- **Expanded Dictionary:** Grow from 20 to 100+ idioms (can crowdsource or use existing idiom datasets)
- **Pronoun Resolution:** Replace ambiguous pronouns with their antecedents where possible
  - Example: "The researchers conducted a study. They found..." → "The researchers conducted a study. **The researchers** found..."
- **Ambiguity Flagging:** Highlight potentially confusing phrases that couldn't be auto-resolved, with a `?` indicator
- **Explanation Tooltips:** Click on a bolded replacement to see what the original was and why it was changed
- **Tone Indicators:** Flag sections that might be sarcastic, metaphorical, or emotionally loaded (harder to implement, research needed)

#### Technical Considerations
- Pronoun resolution: Requires coreference resolution - could use `neuralcoref` or simpler rule-based approach
- Expanded dictionary: JSON files already externalized, just need expansion
- Tooltips: React component with hover state showing original text

---

## Architecture Impact

### Files That Would Change

| File | Changes |
|------|---------|
| `AppContext.jsx` | Add `intensityLevel` state per mode (or global), add `bionicReading`, `readingRuler`, `pacingTimer` settings |
| `SettingsPanel.jsx` | Add intensity level selector (dropdown or slider), checkboxes for new optional features |
| `index.css` | CSS variables for letter-spacing levels, reading ruler styles, bionic reading classes |
| `DyslexiaOutput.jsx` | Add intensity-based rendering, reading ruler component, bionic reading transformation |
| `ADHDFocusMode.jsx` | Add intensity-based isolation, memory aid component, timer feature |
| `AutismOutput.jsx` | Add tooltip system, pronoun highlighting, ambiguity indicators |
| `autism_mode.py` | Add optional pronoun resolution function, expand dictionaries |
| `adhd_mode.py` | Optional: add POS-tagging based noun detection |
| `idiom_map.json` | Expand from 20 to 100+ entries |
| `jargon_map.json` | Expand from 20 to 100+ entries |

### New Files

| File | Purpose |
|------|---------|
| `plan/neurodivergent-improvements-design.md` | This document |
| `plan/codebase-analysis.md` | Comprehensive code documentation |
| `electron-app/src/components/ui/ReadingRuler.jsx` | Reusable reading overlay component |
| `electron-app/src/components/ui/IntensitySelector.jsx` | Intensity level UI control |
| `electron-app/src/hooks/useBionicReading.js` | Text transformation hook |

---

## Implementation Phases (Not Starting Yet)

### Phase 1: Dyslexia Intensity Levels
- Add intensity state and UI controls
- Implement bionic reading toggle
- Add reading ruler
- Adjust CSS variables for spacing

### Phase 2: ADHD Enhancements
- Add intensity levels
- Implement working memory aid
- Add optional pacing timer
- Improve noun detection (backend)

### Phase 3: Autism Intelligence
- Expand idiom/jargon dictionaries
- Add explanation tooltips
- Research pronoun resolution approach
- Add ambiguity flagging

---

## Research References

### Supporting Evidence

1. **Bionic Reading**: A study by Kaufmann (2022) found that bolding initial letters can improve reading speed for some dyslexic readers by providing natural fixation points.

2. **ADHD Working Memory**: Barkley's research on ADHD highlights working memory deficits, supporting our "context badge" feature showing previous sentence summary.

3. **Autism and Literal Language**: Studies by Paul et al. show that autistic individuals often prefer explicit, unambiguous language and benefit from having idioms explained.

4. **Universal Design for Learning (UDL)**: CAST's framework emphasizes multiple means of representation and engagement, supporting our intensity-level approach.

---

## Open Questions

1. **Should intensity level be global or per-mode?**
   - Global: Simpler UX, consistent experience
   - Per-mode: More flexible, respects that someone might want intensive dyslexia support but light autism support

2. **Pronoun resolution quality vs. transparency?**
   - High-quality resolution requires ML models (larger size)
   - Rule-based resolution would be transparent but less accurate
   - Recommendation: Start with rule-based, flag uncertainties

3. **How to source expanded idiom/jargon dictionaries?**
   - Option A: Manual curation from idiom dictionaries
   - Option B: Existing datasets (e.g., SemEval idiom detection datasets)
   - Option C: Community contribution (needs moderation)

---

## Success Metrics

If these improvements are implemented, success could be measured by:

1. **Usage patterns**: Do users adjust intensity levels? What do they gravitate toward?
2. **Comprehension tests**: Before/after comprehension questions could show retention improvement
3. **Subjective feedback**: "Did this help you read better?" surveys
4. **Task completion**: Can users get through longer texts without abandoning?

---

## Conclusion

The Cognitive-Load Adaptive System approach respects neurodivergent users as individuals with varying needs. By providing intensity levels within each mode, we move from "one-size-fits-most" to truly personalized accessibility.

**Next step:** User approval of this design before proceeding to implementation planning.

---

*Document created: 2026-03-24*
*Author: Claude (AI assistant)*
*Project: SimplifyAI - F:\chat_editor_mp*
