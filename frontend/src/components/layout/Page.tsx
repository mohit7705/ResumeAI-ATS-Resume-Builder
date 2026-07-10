type Props = {
  title: string;
  children: React.ReactNode;
};

export default function Page({ title, children }: Props) {
  return (
    <div
      style={{
        maxWidth: 900,
        margin: "0 auto",
      }}
    >
      <h1
        style={{
          marginBottom: 30,
        }}
      >
        {title}
      </h1>

      {children}
    </div>
  );
}