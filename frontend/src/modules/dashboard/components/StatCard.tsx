type Props = {
  title: string;
  value: string | number;
};

export default function StatCard({
  title,
  value,
}: Props) {
  return (
    <div
      style={{
        background: "#111827",
        padding: 20,
        borderRadius: 12,
        border: "1px solid #333",
      }}
    >
      <h3>{title}</h3>

      <h1>{value}</h1>
    </div>
  );
}