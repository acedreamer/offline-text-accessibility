# Offline Text Simplification for Dyslexia Support

A privacy-preserving, offline text simplification tool designed to support readers with dyslexia. Runs entirely on local CPU hardware without cloud dependencies.

## Features

- **100% Offline** - No internet required, no data sent anywhere
- **CPU-Only** - Works on any laptop, no GPU needed
- **Privacy-First** - Documents never leave your device
- **Dyslexia-Optimized** - Short sentences, one idea per line, extra spacing

## Installation

```bash
pip install transformers torch
```

## Usage

```bash
# Basic usage
python simplify.py --input your_file.txt --mode dyslexia

# With readability metrics
python simplify.py --input your_file.txt --mode dyslexia --metrics
```

## Example

**Input:**
```
Artificial intelligence systems are increasingly being integrated into
educational environments and often introduce complex sentence structures.
```

**Output:**
```
Artificial intelligence systems are used in education.

They often use complex language.

This can be hard to process.
```

## Modes

| Mode | Status | Description |
|------|--------|-------------|
| `dyslexia` | Implemented | Short sentences, visual spacing |
| `adhd` | Future | Chunking, focus-friendly output |
| `autism` | Future | Literal phrasing, reduced ambiguity |

## How It Works

1. **T5-small model** simplifies text (60M parameters, runs on CPU)
2. **Rule-based post-processing** formats output for dyslexia:
   - Splits compound sentences
   - One sentence per line
   - Extra spacing between ideas

## Metrics

The tool computes readability improvements:
- Word count change
- Average sentence length
- Flesch Reading Ease score

## Limitations

- English only
- No user studies conducted
- Technical proof-of-concept, not a clinical tool

## License

MIT
