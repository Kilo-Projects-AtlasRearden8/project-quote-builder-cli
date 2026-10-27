"""Export quotes to Markdown and PDF."""

from __future__ import annotations

from .models import Quote


def _discount_line(quote: Quote) -> str:
    if quote.discount_amount > 0:
        return f"-{quote.money_discount()}"
    return quote.money_discount()


def export_markdown(quote: Quote, output) -> None:
    """Write a quote as Markdown to a file path or file-like object."""
    lines = [
        f"# Quote {quote.quote_id}",
        "",
        f"**Client:** {quote.client_name}",
        f"**Project:** {quote.project_name}",
        f"**Created:** {quote.created_at}",
        f"**Updated:** {quote.updated_at}",
        "",
        "## Line items",
        "",
        "| Item | Description | Quantity | Rate | Amount |",
        "|------|-------------|----------|------|--------|",
    ]
    for item in quote.items:
        lines.append(
            f"| {item.item_id} | {item.description} | {item.quantity:g} | "
            f"${item.rate:,.2f} | ${item.amount:,.2f} |"
        )
    if not quote.items:
        lines.append("| -- | -- | -- | -- | -- |")
    lines += [
        "",
        "## Totals",
        "",
        f"- Subtotal: {quote.money_subtotal()}",
        f"- Tax ({quote.tax_rate:g}%): {quote.money_tax()}",
        f"- Discount: {_discount_line(quote)}",
        f"- **Total: {quote.money_total()}**",
        "",
    ]
    content = "\n".join(lines)
    if hasattr(output, "write"):
        output.write(content)
    else:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(content)


def export_pdf(quote: Quote, output) -> None:
    """Write a quote as PDF to a file path.

    Requires the optional ``reportlab`` package. Raises ``ImportError`` with a
    helpful message when it is not installed.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "PDF export requires the 'reportlab' package. "
            "Install it with: pip install reportlab"
        ) from exc

    c = canvas.Canvas(output, pagesize=letter)
    width, height = letter
    y = height - 0.75 * inch

    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.75 * inch, y, f"Quote {quote.quote_id}")
    y -= 0.4 * inch

    c.setFont("Helvetica", 11)
    c.drawString(0.75 * inch, y, f"Client: {quote.client_name}")
    y -= 0.22 * inch
    c.drawString(0.75 * inch, y, f"Project: {quote.project_name}")
    y -= 0.22 * inch
    c.drawString(0.75 * inch, y, f"Created: {quote.created_at}")
    y -= 0.22 * inch
    c.drawString(0.75 * inch, y, f"Updated: {quote.updated_at}")
    y -= 0.4 * inch

    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, y, "Line items")
    y -= 0.22 * inch
    c.setFont("Helvetica", 10)
    headers = ["Description", "Qty", "Rate", "Amount"]
    x_positions = [0.75 * inch, 3.4 * inch, 4.1 * inch, 4.8 * inch]
    for header, x in zip(headers, x_positions):
        c.drawString(x, y, header)
    y -= 0.22 * inch
    c.setStrokeGray(0.7)
    c.line(0.75 * inch, y, width - 0.75 * inch, y)
    y -= 0.18 * inch

    for item in quote.items:
        c.drawString(x_positions[0], y, item.description[:60])
        c.drawString(x_positions[1], y, f"{item.quantity:g}")
        c.drawString(x_positions[2], y, f"${item.rate:,.2f}")
        c.drawString(x_positions[3], y, f"${item.amount:,.2f}")
        y -= 0.22 * inch

    if not quote.items:
        c.drawString(x_positions[0], y, "No line items.")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.line(0.75 * inch, y, width - 0.75 * inch, y)
    y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 11)
    totals = [
        (f"Subtotal: {quote.money_subtotal()}", quote.money_subtotal()),
        (f"Tax ({quote.tax_rate:g}%): {quote.money_tax()}", quote.money_tax()),
        (f"Discount: -{quote.money_discount()}", quote.money_discount()),
        (f"Total: {quote.money_total()}", quote.money_total()),
    ]
    for label, value in totals:
        c.drawString(x_positions[2], y, label)
        c.drawRightString(width - 0.75 * inch, y, value)
        y -= 0.22 * inch

    c.showPage()
    c.save()
