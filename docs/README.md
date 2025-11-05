# Documentron Doc Synthesis

This module synthesizes human-readable documentation from machine-generated artifacts.

## Features

- Deterministic doc generation from artifacts
- Citation and provenance tracking
- Hallucination detection and flagging
- API coverage reporting

## Usage

See quickstart.md for detailed usage instructions.

## Architecture

- `cli.py`: Command-line interface
- `artifact_loader.py`: Loads and validates artifacts
- `doc_writer.py`: Writes markdown docs with citations
- `provenance.py`: Manages provenance and confidence signals
- `hallucination_detector.py`: Flags potential hallucinations
- `api_coverage.py`: Measures API documentation coverage