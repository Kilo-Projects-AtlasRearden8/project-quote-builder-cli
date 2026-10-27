"""Data models for project quotes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .math import discount_amount, money, subtotal, tax_amount, total


@dataclass
class LineItem:
    """A single line item on a quote."""

    description: str
    quantity: float
    rate: float
    item_id: str = field(default_factory=lambda: uuid4().hex[:8])

    @property
    def amount(self) -> float:
        return round(self.quantity * self.rate, 2)


@dataclass
class Quote:
    """A project quote with line items, tax, discount, and totals."""

    client_name: str
    project_name: str
    items: list[LineItem] = field(default_factory=list)
    tax_rate: float = 0.0
    discount: float = 0.0
    quote_id: str = field(default_factory=lambda: uuid4().hex[:8])
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def subtotal(self) -> float:
        return subtotal(self.items)

    @property
    def tax(self) -> float:
        return tax_amount(self.subtotal, self.tax_rate)

    @property
    def discount_amount(self) -> float:
        return discount_amount(self.subtotal, self.discount)

    @property
    def total(self) -> float:
        return total(self.subtotal, self.tax, self.discount_amount)

    def add_item(self, item: LineItem) -> None:
        self.items.append(item)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_item(self, item_id: str) -> bool:
        before = len(self.items)
        self.items = [item for item in self.items if item.item_id != item_id]
        if len(self.items) < before:
            self.updated_at = datetime.now(timezone.utc).isoformat()
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "quote_id": self.quote_id,
            "client_name": self.client_name,
            "project_name": self.project_name,
            "tax_rate": self.tax_rate,
            "discount": self.discount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "items": [
                {
                    "item_id": item.item_id,
                    "description": item.description,
                    "quantity": item.quantity,
                    "rate": item.rate,
                }
                for item in self.items
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        quote = cls(
            client_name=data["client_name"],
            project_name=data["project_name"],
            tax_rate=float(data.get("tax_rate", 0.0)),
            discount=float(data.get("discount", 0.0)),
            quote_id=data.get("quote_id", uuid4().hex[:8]),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
        )
        for item in data.get("items", []):
            quote.add_item(
                LineItem(
                    description=item["description"],
                    quantity=float(item["quantity"]),
                    rate=float(item["rate"]),
                    item_id=item.get("item_id", uuid4().hex[:8]),
                )
            )
        return quote

    def money_subtotal(self) -> str:
        return money(self.subtotal)

    def money_tax(self) -> str:
        return money(self.tax)

    def money_discount(self) -> str:
        return money(self.discount_amount)

    def money_total(self) -> str:
        return money(self.total)
