# project-quote-builder

A local-first Python CLI for freelancers and small businesses to build project
quotes: line items, rates, totals, and Markdown/PDF export. Built and
maintained by [Asdale Dynamics, LLC](https://dylanasdale.github.io).

## Who it's for

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC (Indiana, formed October 2026). His book *The Massive AI Manual*
and hub site dylanasdale.github.io explain AI "like a friend would": plain
English, step by step, never condescending.

Asdale Dynamics focuses on beginner-friendly AI education, books and guides,
and practical tools the LLC can publish or sell — including small-business and
author tools like this quote builder.

## What it does

`pqb` helps you create quotes, add line items with quantities and rates, and
compute subtotals, tax, and discounts. Export your finished quote to Markdown
or PDF. Everything is stored locally as JSON files — nothing is ever sent over
the network. A dry-run mode lets you preview a quote before you save it.

## Install

Copy this folder onto your machine, then install:

```bash
cd project-quote-builder-cli
pip install .
```

If your system blocks `pip install` (externally managed Python), use a virtual
environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

PDF export requires the optional `reportlab` package:

```bash
pip install reportlab
```

## Quick start

Create a quote:

```bash
pqb new --client "Acme Corp" --project "Website redesign"
```

Add line items:

```bash
pqb add-item <QUOTE_ID> --description "UI design" --quantity 2 --rate 150.00
pqb add-item <QUOTE_ID> --description "Development" --quantity 20 --rate 120.00
```

Preview without saving (dry-run):

```bash
pqb new --client "Acme Corp" --project "Website redesign" --dry-run
pqb add-item <QUOTE_ID> --description "UI design" --quantity 2 --rate 150.00 --dry-run
```

List, view, and totals:

```bash
pqb list
pqb show <QUOTE_ID>
pqb total <QUOTE_ID>
```

Export:

```bash
pqb export <QUOTE_ID> --format md --out quote.md
pqb export <QUOTE_ID> --format pdf --out quote.pdf
```

## Tests

```bash
pip install pytest
pytest
```

## Storage

Quotes are saved as local JSON files under
`~/.local/share/project-quote-builder/quotes`. Override the location with the
`PQB_DATA_DIR` environment variable. No network access is used.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: Asdale Dynamics, LLC — beginner-friendly AI education, books, guides,
and practical tools for freelancers, authors, and small businesses.
