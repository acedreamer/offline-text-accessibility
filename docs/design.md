# Project Design Context

This project is an offline, privacy-preserving AI text simplification tool.

## Scope and Mode Support

The system supports multiple accessibility-oriented modes through a unified
architecture. In the current prototype, Dyslexia Mode is fully implemented
and quantitatively evaluated.

ADHD and Autism modes are included at the interface and architectural level
to demonstrate extensibility of the system design. These modes are not
evaluated in the present work and are considered part of future development.

Primary evaluated mode:
- Dyslexia support (sentence simplification, readability improvement)

Other modes (design extensions, not evaluated):
- ADHD (chunking, focus-friendly output)
- Autism (literal phrasing, reduced ambiguity)

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
Inputs are task-conditioned using the `simplify:` prefix to encourage semantic
preservation while reducing syntactic complexity. This approach was chosen
over summarization prompts to avoid information loss, which is critical for
assistive accessibility tools.

## Dyslexia-Oriented Linguistic Heuristics

Following neural simplification, rule-based post-processing is applied to
optimize readability for dyslexic users. These heuristics include:

- Splitting compound sentences into single-idea statements
- One sentence per line with additional spacing
- Conservative punctuation and capitalization

These heuristics are intentionally simple and transparent, aligning with
accessibility writing guidelines and avoiding opaque transformations.
