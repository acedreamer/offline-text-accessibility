# Project Design Context

This project is an offline, privacy-preserving AI text simplification tool.

## Scope and Mode Support

The system supports three accessibility-oriented modes through a unified
architecture. All three modes are fully implemented. Dyslexia Mode is
quantitatively evaluated; ADHD and Autism modes are functionally complete
but not yet formally evaluated.

Implemented modes:
- Dyslexia (sentence simplification, hyphenation, one-sentence-per-line)
- ADHD (progress markers, bullet formatting, key term bolding)
- Autism (idiom replacement with literal meanings)

## ADHD Mode

ADHD mode formats simplified text to reduce cognitive load and help users
maintain attention. Features:

- Progress markers: Each sentence is prefixed with `[i/N]` where N is the
  total sentence count. This gives users a concrete sense of how far through
  the text they are.
- Bullet-style layout: One sentence per line, visually chunked.
- Key term bolding: The first significant content word in each sentence is
  wrapped in `**bold**` markers to anchor the reader's attention.

Implementation file: `adhd_mode.py`

## Autism Mode

Autism mode targets literal interpretation by replacing figurative and
idiomatic language with explicit, unambiguous alternatives. Features:

- Idiom replacement: A curated dictionary of 20 common English idioms is
  applied via regex, replacing each with its literal meaning.
  Example: "piece of cake" → "easy", "under the weather" → "feeling sick"
- Case-insensitive matching with word-boundary constraints to avoid
  false positives.
- No pronoun resolution (deferred - requires coreference NLP).

Implementation file: `autism_mode.py`

## Core Constraints

- Must run fully offline
- CPU-only inference
- T5-based text simplification
- CLI-first, UI later
- Sentence-by-sentence output in Dyslexia mode

## Architecture

- Shared AI simplification core
- Mode-specific post-processing
- No cloud calls
- No Electron or heavy UI frameworks initially

## T5 Task Conditioning Strategy

Text simplification is implemented using a T5-based sequence-to-sequence model.
Inputs are task-conditioned using the `summarize:` prefix, which T5-small
responds to reliably due to its pretraining on CNN/DailyMail summarization.
While a `simplify:` prefix would be semantically cleaner, T5-small was not
pretrained on a simplification corpus and produces better outputs with the
`summarize:` prompt. This is a deliberate trade-off documented here for
transparency.

## Dyslexia-Oriented Linguistic Heuristics

Following neural simplification, rule-based post-processing is applied to
optimize readability for dyslexic users. These heuristics include:

- Splitting compound sentences into single-idea statements
- One sentence per line with additional spacing
- Conservative punctuation and capitalization

These heuristics are intentionally simple and transparent, aligning with
accessibility writing guidelines and avoiding opaque transformations.
