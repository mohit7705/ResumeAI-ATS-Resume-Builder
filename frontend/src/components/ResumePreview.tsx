import { useEffect, useRef, useState } from "react";

type Props = {
  html?: string;
  version?: number;
};

const API_BASE_URL = "";

export default function ResumePreview({ html, version = 0 }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const container = containerRef.current;

    if (!container) return;

    const updateScale = () => {
      const availableWidth = container.clientWidth;
      const a4Width = 794;

      setScale(Math.min(availableWidth / a4Width, 1));
    };

    updateScale();

    const observer = new ResizeObserver(updateScale);
    observer.observe(container);
    window.addEventListener("resize", updateScale);

    return () => {
      observer.disconnect();
      window.removeEventListener("resize", updateScale);
    };
  }, []);

  if (!html) return null;

  const normalizedPath = html.replace(/\\/g, "/");
  const filename = normalizedPath.split("/").pop();

  if (
    filename !== "resume.html" &&
    filename !== "resume_photo.html"
  ) {
    return <p className="muted">Invalid resume preview path.</p>;
  }

  const previewUrl =
    `${API_BASE_URL}/generated/html/${filename}?t=${encodeURIComponent(
      normalizedPath
    )}&v=${version}`;

  return (
    <div className="paper">
      <div
        ref={containerRef}
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: 794,
            height: 1123,
            transform: `scale(${scale})`,
            transformOrigin: "top center",
            flexShrink: 0,
            marginBottom:
              scale < 1 ? -(1123 * (1 - scale)) : 0,
          }}
        >
          <iframe
            title={`Resume Preview - ${filename}`}
            src={previewUrl}
            width={794}
            height={1123}
            style={{
              display: "block",
              width: 794,
              height: 1123,
              border: "1px solid var(--line-strong)",
              borderRadius: 6,
              background: "#fff",
              boxShadow: "var(--shadow-md)",
            }}
          />
        </div>
      </div>
    </div>
  );
}
