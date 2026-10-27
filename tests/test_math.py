"""Tests for the quote math module."""

from project_quote_builder.math import (
    discount_amount,
    money,
    subtotal,
    tax_amount,
    total,
)


class FakeItem:
    def __init__(self, quantity, rate):
        self.quantity = quantity
        self.rate = rate


def test_subtotal_sums_line_items():
    items = [FakeItem(2, 100.00), FakeItem(1, 50.00)]
    assert subtotal(items) == 250.00


def test_subtotal_empty_is_zero():
    assert subtotal([]) == 0.0


def test_tax_amount():
    assert tax_amount(100.00, 10.0) == 10.00
    assert tax_amount(250.00, 8.25) == 20.63


def test_discount_amount():
    assert discount_amount(100.00, 20.00) == 20.00
    assert discount_amount(100.00, 0.00) == 0.0
    assert discount_amount(100.00, 150.00) == 100.0


def test_total():
    assert total(100.00, 10.00, 0.00) == 110.00
    assert total(250.00, 20.63, 25.00) == 245.63


def test_money_formats_two_decimals():
    assert money(100) == "100.00"
    assert money(1000.5) == "1,000.50"
    assert money(0.005) == "0.01"
