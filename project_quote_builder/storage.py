"""Local-only JSON storage for quotes.

Quotes are stored as individual JSON files in a data directory. Nothing is
ever sent over the network. The directory can be overridden with the
PQB_DATA_DIR environment variable; it defaults to
~/.local/share/project-quote-builder/quotes.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Quote

DEFAULT_DIR = Path.home() / ".local" / "share" / "project-quote-builder" / "quotes"


class QuoteStore:
    """CRUD for quotes persisted as local JSON files."""

    def __init__(self, directory: str | Path | None = None) -> None:
        if directory is None:
            directory = os.environ.get("PQB_DATA_DIR", str(DEFAULT_DIR))
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, quote_id: str) -> Path:
        return self.directory / f"{quote_id}.json"

    def save(self, quote: Quote) -> None:
        with self._path(quote.quote_id).open("w", encoding="utf-8") as handle:
            json.dump(quote.to_dict(), handle, indent=2)

    def get(self, quote_id: str) -> Quote | None:
        path = self._path(quote_id)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return Quote.from_dict(data)

    def delete(self, quote_id: str) -> bool:
        path = self._path(quote_id)
        if not path.exists():
            return False
        path.unlink()
        return True

    def list(self) -> list[Quote]:
        quotes: list[Quote] = []
        for path in sorted(self.directory.glob("*.json")):
            try:
                with path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                quotes.append(Quote.from_dict(data))
            except (json.JSONDecodeError, OSError):
                continue
        return quotes
