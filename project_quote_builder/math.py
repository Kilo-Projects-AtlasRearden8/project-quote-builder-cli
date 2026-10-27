"""Money math for quotes.

All calculations use Decimal internally so totals are exact to the cent.
Public functions accept and return plain floats for convenience, rounded to
two decimal places.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def _dec(value) -> Decimal:
    return Decimal(str(value))


def money(value) -> str:
    """Format a numeric value as a two-decimal currency string."""
    result = _dec(value).quantize(CENT, rounding=ROUND_HALF_UP)
    if result == 0:
        result = Decimal("0")
    return f"{result:,.2f}"


def subtotal(items) -> float:
    """Sum of quantity * rate across line items."""
    result = Decimal("0")
    for item in items:
        result += _dec(item.quantity) * _dec(item.rate)
    return float(result.quantize(CENT, rounding=ROUND_HALF_UP))


def tax_amount(subtotal_value, tax_rate) -> float:
    """Tax = subtotal * tax_rate / 100."""
    result = _dec(subtotal_value) * _dec(tax_rate) / Decimal("100")
    return float(result.quantize(CENT, rounding=ROUND_HALF_UP))


def discount_amount(subtotal_value, discount) -> float:
    """Fixed dollar discount off the subtotal (capped so it never exceeds the subtotal)."""
    result = _dec(discount)
    if result < 0:
        result = Decimal("0")
    if result > _dec(subtotal_value):
        result = _dec(subtotal_value)
    return float(result.quantize(CENT, rounding=ROUND_HALF_UP))


def total(subtotal_value, tax, discount_amount_value) -> float:
    """Grand total = subtotal + tax - discount."""
    result = _dec(subtotal_value) + _dec(tax) - _dec(discount_amount_value)
    if result < 0:
        result = Decimal("0")
    return float(result.quantize(CENT, rounding=ROUND_HALF_UP))
