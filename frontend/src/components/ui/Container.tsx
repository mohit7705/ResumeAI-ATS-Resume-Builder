type Props = {
  children: React.ReactNode;
};

export default function Container({ children }: Props) {
  return (
    <div
      style={{
        maxWidth: 1100,
        margin: "0 auto",
        padding: 30,
      }}
    >
      {children}
    </div>
  );
}