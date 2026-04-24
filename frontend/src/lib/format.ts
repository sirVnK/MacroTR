export function formatNumber(value: number | null | undefined, unit?: string) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "-";
  }

  const digits = Math.abs(value) >= 1000 ? 0 : 2;
  const formatted = new Intl.NumberFormat("tr-TR", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  }).format(value);
  return unit ? `${formatted} ${unit}` : formatted;
}

export function formatDate(value: string | null | undefined) {
  if (!value) {
    return "-";
  }
  return new Intl.DateTimeFormat("tr-TR", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  }).format(new Date(value));
}

export function formatPercent(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "-";
  }
  return `${value > 0 ? "+" : ""}${value.toFixed(2)}%`;
}

export function toCsv(rows: Array<Record<string, string | number | null>>) {
  if (!rows.length) {
    return "";
  }
  const headers = Object.keys(rows[0]);
  const body = rows.map((row) =>
    headers
      .map((header) => {
        const value = row[header] ?? "";
        return `"${String(value).split('"').join('""')}"`;
      })
      .join(",")
  );
  return [headers.join(","), ...body].join("\n");
}
