type Props = {
  html?: string;
};

export default function ResumePreview({ html }: Props) {
  if (!html) return null;

  const path = html.replace(/\\/g, "/");

  return (
    <div
      style={{
        marginTop: 30,
      }}
    >
      <h2>Live Resume Preview</h2>

      <iframe
        title="Resume Preview"
        src={`http://127.0.0.1:8000/generated/html/resume.html?${Date.now()}&path=${encodeURIComponent(path)}`}
        width="100%"
        height="900"
        style={{
          border: "1px solid #444",
          borderRadius: 10,
          background: "#fff",
        }}
      />
    </div>
  );
}