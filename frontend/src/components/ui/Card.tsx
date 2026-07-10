type Props = {
  title: string;
  children: React.ReactNode;
};

export default function Card({ title, children }: Props) {
  return (
    <div
      style={{
        background: "#111827",
        border: "1px solid #2d3748",
        borderRadius: 12,
        padding: 25,
        marginBottom: 20,
      }}
    >
      <h2>{title}</h2>

      {children}
    </div>
  );
}