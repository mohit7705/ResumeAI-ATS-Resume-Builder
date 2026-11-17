const MONTHS = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/** "2024-08" -> "Aug 2024" (anything else is returned untouched) */
export function formatMonth(value?: string): string {
  if (!value) return "";
  const match = /^(\d{4})-(\d{2})/.exec(value);
  if (!match) return value;
  return `${MONTHS[Number(match[2]) - 1] ?? ""} ${match[1]}`.trim();
}

/** "2024-08-15" -> "15 Aug 2024" */
export function formatDate(value?: string): string {
  if (!value) return "";
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);
  if (!match) return value;
  return `${Number(match[3])} ${MONTHS[Number(match[2]) - 1] ?? ""} ${match[1]}`;
}

/** "2022-08", "2026-06" -> "Aug 2022 – Jun 2026" (empty end date = Present) */
export function formatRange(start?: string, end?: string): string {
  const from = formatMonth(start);
  if (!from && !end) return "";
  const to = end ? formatMonth(end) : "Present";
  return from ? `${from} – ${to}` : to;
}

/** Accepts an array or a delimited string and returns clean items. */
export function toList(value: unknown, separator: RegExp = /,/): string[] {
  if (Array.isArray(value)) {
    return value.map((item) => String(item).trim()).filter(Boolean);
  }
  if (typeof value === "string") {
    return value.split(separator).map((item) => item.trim()).filter(Boolean);
  }
  return [];
}

export function initials(first?: string, last?: string): string {
  const letters = `${first?.trim()?.[0] ?? ""}${last?.trim()?.[0] ?? ""}`;
  return letters.toUpperCase() || "R";
}
