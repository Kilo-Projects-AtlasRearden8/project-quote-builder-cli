"""project-quote-builder: local-first CLI for building project quotes."""

from .models import LineItem, Quote
from .math import money, subtotal, tax_amount, discount_amount, total
from .storage import QuoteStore

__all__ = [
    "LineItem",
    "Quote",
    "money",
    "subtotal",
    "tax_amount",
    "discount_amount",
    "total",
    "QuoteStore",
]
__version__ = "0.1.0"
