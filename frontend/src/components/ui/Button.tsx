type Props = React.ButtonHTMLAttributes<HTMLButtonElement>;

export default function Button(props: Props) {
  return (
    <button
      {...props}
      style={{
        padding: "10px 18px",
        border: "none",
        borderRadius: 8,
        cursor: "pointer",
        background: "#2563eb",
        color: "#fff",
        fontWeight: 600,
        ...props.style,
      }}
    >
      {props.children}
    </button>
  );
}