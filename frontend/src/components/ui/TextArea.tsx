type Props = React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export default function TextArea(props: Props) {
  return (
    <textarea
      {...props}
      style={{
        width: "100%",
        minHeight: 150,
        padding: 10,
        borderRadius: 8,
        border: "1px solid #444",
        background: "#1f2937",
        color: "#fff",
        resize: "vertical",
        ...props.style,
      }}
    />
  );
}