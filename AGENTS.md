# Repository Guidance

This repository builds fictional DOCX/XLSX compatibility fixtures and imports them into ODT/ODS with Grind.

## Build and Validation

- Use `docker build -t grind-sample-corpus .` to build the complete generator and Grind CLI image.
- Use `docker run --rm -v "$PWD/samples:/workspace/samples" grind-sample-corpus` to generate fixtures and conversion reports.
- The Dockerfile pins Craft release versions and verifies the published SHA-256 checksums before installation.
- Keep `scripts/create_samples.py` using `wordcraft-cli` and `gridcraft-cli`; do not replace Craft generation with Python document libraries.
- Preserve the explicitly fictional names, `.test` email addresses, and `FICTIONAL TEST DATA` labels in fixtures.
- Keep output directories and report generation consistent with `scripts/create_samples.py` and `README.md`.

## Changes

- Prefer focused edits to the generator and its documented container workflow.
- Verify generated DOCX/XLSX files and Grind imports when changing fixture content or generation behavior.
- Do not commit generated files under `samples/` unless the task specifically requests them.