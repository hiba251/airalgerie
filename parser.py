# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 16:29:46 2026

feriel boukerma Hiba doumar
"""

from __future__ import annotations
import re
from typing import Optional, Dict

PRICE_RE = re.compile(
    r"""
    (?P<route>.*?)
    \s+From\s+
    (?P<price>[\d\s]+(?:[.,]\d{2})?)
    \s*(?P<currency>[A-Z]{3})
    """,
    re.IGNORECASE | re.VERBOSE
)

def normalize_price(price_raw: str) -> float:
    s = price_raw.replace(" ", "").replace("\u00a0", "")
    s = s.replace(",", ".")
    return float(s)

def parse_offer(text: str) -> Optional[Dict]:
    text = " ".join(text.split())
    m = PRICE_RE.search(text)
    if not m:
        return None

    route = m.group("route").strip(" -–—")
    price_raw = m.group("price").strip()
    currency = m.group("currency").upper()

    price_value = None
    try:
        price_value = normalize_price(price_raw)
    except Exception:
        pass

    return {
        "route": route,
        "price_raw": price_raw,
        "price_value": price_value,
        "currency": currency,
        "text_source": text
    }