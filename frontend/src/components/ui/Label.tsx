type Props = {
  children: React.ReactNode;
};

export default function Label({
  children,
}: Props) {
  return (
    <label
      style={{
        display: "block",
        marginBottom: 8,
        fontWeight: 600,
      }}
    >
      {children}
    </label>
  );
}