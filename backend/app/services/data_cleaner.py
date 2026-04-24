from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any


def parse_evds_date(value: str) -> date | None:
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except (TypeError, ValueError):
            continue
    return None


def parse_numeric(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))

    cleaned = str(value).strip()
    if not cleaned or cleaned.upper() in {"ND", "NA", "NULL", "-"}:
        return None

    cleaned = cleaned.replace(" ", "").replace(",", ".")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def clean_observations(rows: list[dict[str, Any]], evds_code: str) -> list[tuple[date, Decimal]]:
    value_keys = [
        evds_code,
        evds_code.replace(".", "_"),
        evds_code.replace(".", "_").replace("-", "_"),
    ]
    cleaned: dict[date, Decimal] = {}

    for row in rows:
        observed_at = parse_evds_date(str(row.get("Tarih") or row.get("DATE") or ""))
        if observed_at is None:
            continue

        raw_value = None
        for key in value_keys:
            if key in row:
                raw_value = row.get(key)
                break

        value = parse_numeric(raw_value)
        if value is not None:
            cleaned[observed_at] = value

    return sorted(cleaned.items(), key=lambda item: item[0])


def normalize_points(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    first_value = next(
        (float(point["value"]) for point in points if float(point["value"]) != 0),
        None,
    )
    if first_value is None:
        return points

    return [
        {
            **point,
            "value": round((float(point["value"]) / first_value) * 100, 4),
        }
        for point in points
    ]

