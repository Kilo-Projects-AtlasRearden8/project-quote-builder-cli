# STATUS

## What was built

`project-quote-builder-cli` — a local-first Python CLI for freelancers and
small businesses to build project quotes.

Components:
- `project_quote_builder/models.py` — `Quote` and `LineItem` data models with
  subtotal/tax/discount/total properties and JSON (de)serialization.
- `project_quote_builder/math.py` — exact Decimal-based money math
  (`subtotal`, `tax_amount`, `discount_amount`, `total`, `money` formatting).
- `project_quote_builder/storage.py` — `QuoteStore`: local-only JSON file CRUD
  under `~/.local/share/project-quote-builder/quotes` (overridable via
  `PQB_DATA_DIR`). No network access.
- `project_quote_builder/exporter.py` — Markdown and PDF (`reportlab`) export.
- `project_quote_builder/cli.py` — `pqb` CLI: `new`, `add-item`, `list`,
  `show`, `total`, `export` (md/pdf), with `--dry-run` on `new` and `add-item`.

Files:
- `pyproject.toml` — project metadata + `pqb` console script entry point.
- `README.md` — install, quick start, tests, storage, license, credit.
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC.
- `tests/test_math.py` — math tests.
- `.gitignore` — standard Python ignores.

## How to run it

```bash
cd project-quote-builder-cli
pip install .            # or use a venv if pip is externally managed
pip install reportlab    # only needed for PDF export

pqb new --client "Acme Corp" --project "Website redesign" --dry-run
pqb new --client "Acme Corp" --project "Website redesign"
pqb add-item <QUOTE_ID> --description "UI design" --quantity 2 --rate 150.00
pqb add-item <QUOTE_ID> --description "Development" --quantity 20 --rate 120.00
pqb show <QUOTE_ID>
pqb total <QUOTE_ID>
pqb export <QUOTE_ID> --format md --out quote.md
pqb export <QUOTE_ID> --format pdf --out quote.pdf

pip install pytest
pytest
```

## Verification results

- `pytest`: 6 passed.
- CLI end-to-end (save, add items, show, total, list): works; totals correct
  (subtotal 2,700.00, tax 0.00, discount 0.00, total 2,700.00).
- Dry-run mode: previews without saving.
- Markdown export: produces valid Markdown with line items and totals.
- PDF export: produces a PDF via `reportlab`.
- Package builds: `pyproject.toml` is valid; `pip install .` is blocked only by
  the system's externally-managed Python (PEP 668), not by the package itself
  — use a venv.

Known gap: the package was not installed into site-packages in this
environment because the system Python is externally managed (PEP 668). Run in a
virtual environment or with `pip install --user`/`pipx` to install the `pqb`
command on PATH.

## Credit

Built by Asdale Dynamics, LLC. MIT License, Copyright (c) 2026 Asdale Dynamics,
LLC.
