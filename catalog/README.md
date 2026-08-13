# Card catalogue

This directory contains version-controlled, non-user card knowledge.

- `cards/` contains supported cards loaded by the application.
- `examples/` documents the schema and is used by tests only.

Each supported card has stable metadata in `card.yaml` and immutable,
effective-dated rule files under `rules/`. Correct factual mistakes in place;
represent bank changes by adding a new rule version.
