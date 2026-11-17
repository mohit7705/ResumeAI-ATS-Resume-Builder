type Check = { name: string; ok: boolean; detail?: string };

type Props = {
  data?: { passed: number; total: number; checks: Check[] } | null;
};

export default function RecruiterCheck({ data }: Props) {
  if (!data || !data.checks?.length) return null;

  return (
    <div style={{ marginTop: 24 }}>
      <p className="label" style={{ marginBottom: 8 }}>
        Recruiter check: {data.passed}/{data.total} passed
      </p>
      <ul style={{ margin: 0, paddingLeft: 18, lineHeight: 1.6 }}>
        {data.checks.map((check) => (
          <li key={check.name}>
            {check.ok ? "✓" : "✗"} {check.name}
            {check.detail ? ` — ${check.detail}` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}
