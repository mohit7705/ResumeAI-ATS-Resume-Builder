type Props = {
  title: string;
  subtitle?: string;
};

export default function SectionHeader({
  title,
  subtitle,
}: Props) {
  return (
    <div
      style={{
        marginBottom: 25,
      }}
    >
      <h1
        style={{
          marginBottom: 5,
        }}
      >
        {title}
      </h1>

      {subtitle && (
        <p
          style={{
            color: "#9ca3af",
          }}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
}