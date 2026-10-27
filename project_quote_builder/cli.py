"""Command-line interface for project-quote-builder."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .exporter import export_markdown, export_pdf
from .math import money
from .models import LineItem, Quote
from .storage import QuoteStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pqb",
        description="Build project quotes locally: line items, rates, totals, "
        "Markdown/PDF export.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new quote")
    new_parser.add_argument("--client", required=True, help="Client name")
    new_parser.add_argument("--project", required=True, help="Project name")
    new_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the quote without saving it",
    )
    new_parser.set_defaults(func=cmd_new)

    add_item = subparsers.add_parser("add-item", help="Add a line item to a quote")
    add_item.add_argument("quote_id", help="Quote id")
    add_item.add_argument("--description", required=True)
    add_item.add_argument("--quantity", type=float, required=True)
    add_item.add_argument("--rate", type=float, required=True)
    add_item.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the updated quote without saving it",
    )
    add_item.set_defaults(func=cmd_add_item)

    list_parser = subparsers.add_parser("list", help="List saved quotes")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="Show a quote")
    show_parser.add_argument("quote_id")
    show_parser.set_defaults(func=cmd_show)

    total_parser = subparsers.add_parser("total", help="Show quote totals")
    total_parser.add_argument("quote_id")
    total_parser.set_defaults(func=cmd_total)

    export_parser = subparsers.add_parser("export", help="Export a quote")
    export_parser.add_argument("quote_id")
    export_parser.add_argument(
        "--format",
        choices=["md", "pdf"],
        default="md",
        help="Export format (default: md)",
    )
    export_parser.add_argument("--out", required=True, help="Output file path")
    export_parser.set_defaults(func=cmd_export)

    return parser


def _store() -> QuoteStore:
    return QuoteStore()


def cmd_new(args: argparse.Namespace) -> int:
    quote = Quote(client_name=args.client, project_name=args.project)
    if args.dry_run:
        print(quote_summary(quote))
        print("(dry-run: not saved)")
        return 0
    _store().save(quote)
    print(f"Created quote {quote.quote_id} for {args.client} / {args.project}")
    return 0


def cmd_add_item(args: argparse.Namespace) -> int:
    store = _store()
    quote = store.get(args.quote_id)
    if quote is None:
        print(f"Quote {args.quote_id} not found", file=sys.stderr)
        return 1
    item = LineItem(
        description=args.description,
        quantity=args.quantity,
        rate=args.rate,
    )
    quote.add_item(item)
    if args.dry_run:
        print(quote_summary(quote))
        print(f"Added item {item.item_id} (dry-run: not saved)")
        return 0
    store.save(quote)
    print(f"Added item {item.item_id} to quote {args.quote_id}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    quotes = _store().list()
    if not quotes:
        print("No quotes found.")
        return 0
    for quote in quotes:
        print(
            f"{quote.quote_id}  {quote.client_name} | {quote.project_name} | "
            f"total {quote.money_total()} | {quote.updated_at}"
        )
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    quote = _store().get(args.quote_id)
    if quote is None:
        print(f"Quote {args.quote_id} not found", file=sys.stderr)
        return 1
    print(quote_summary(quote))
    return 0


def cmd_total(args: argparse.Namespace) -> int:
    quote = _store().get(args.quote_id)
    if quote is None:
        print(f"Quote {args.quote_id} not found", file=sys.stderr)
        return 1
    print(f"Subtotal: {quote.money_subtotal()}")
    print(f"Tax ({quote.tax_rate:g}%): {quote.money_tax()}")
    print(f"Discount: {_discount_line(quote)}")
    print(f"Total: {quote.money_total()}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    quote = _store().get(args.quote_id)
    if quote is None:
        print(f"Quote {args.quote_id} not found", file=sys.stderr)
        return 1
    if args.format == "md":
        export_markdown(quote, args.out)
    else:
        try:
            export_pdf(quote, args.out)
        except ImportError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    print(f"Exported quote {args.quote_id} to {args.out} ({args.format})")
    return 0


def quote_summary(quote: Quote) -> str:
    lines = [
        f"Quote {quote.quote_id}",
        f"Client: {quote.client_name}",
        f"Project: {quote.project_name}",
        f"Created: {quote.created_at}",
        f"Updated: {quote.updated_at}",
        "",
        "Line items:",
    ]
    if not quote.items:
        lines.append("  (none)")
    for item in quote.items:
        lines.append(
            f"  {item.item_id}  {item.description}  qty={item.quantity:g}  "
            f"rate=${item.rate:,.2f}  amount=${item.amount:,.2f}"
        )
    lines += [
        "",
        "Totals:",
        f"  Subtotal: {quote.money_subtotal()}",
        f"  Tax ({quote.tax_rate:g}%): {quote.money_tax()}",
        f"  Discount: {_discount_line(quote)}",
        f"  Total: {quote.money_total()}",
    ]
    return "\n".join(lines)


def _discount_line(quote: Quote) -> str:
    if quote.discount_amount > 0:
        return f"-{quote.money_discount()}"
    return quote.money_discount()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
