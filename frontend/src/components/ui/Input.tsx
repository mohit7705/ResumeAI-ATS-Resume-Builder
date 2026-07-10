type Props = React.InputHTMLAttributes<HTMLInputElement>;

export default function Input(props: Props) {
  return (
    <input
      {...props}
      style={{
        width: "100%",
        padding: "10px",
        border: "1px solid #444",
        borderRadius: 8,
        marginTop: 5,
        marginBottom: 15,
        background: "#1f2937",
        color: "#fff",
        ...props.style,
      }}
    />
  );
}