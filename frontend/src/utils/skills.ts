/**
 * The skills API returns { category: { enabled, skills: [{ name, enabled }] } }
 * (older data used { category: ["Python", ...] }). These helpers understand both.
 */
function listOf(value: unknown): unknown[] {
  if (Array.isArray(value)) return value;
  if (value && typeof value === "object" && Array.isArray((value as any).skills)) {
    return (value as any).skills;
  }
  return [];
}

export function countSkills(data: unknown): number {
  if (!data || typeof data !== "object") return 0;
  return Object.values(data as Record<string, unknown>).reduce<number>(
    (total, category) => total + listOf(category).length,
    0
  );
}

export function hasSkills(data: unknown): boolean {
  return countSkills(data) > 0;
}
