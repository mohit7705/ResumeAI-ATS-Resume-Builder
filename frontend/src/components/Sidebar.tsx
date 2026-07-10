import { useApp } from "../context/AppContext";

const menus = [
  { title: "Dashboard", value: "dashboard" },
  { title: "Profile", value: "profile" },
  { title: "Contact", value: "contact" },
  { title: "Summary", value: "summary" },
  { title: "Education", value: "education" },
  { title: "Experience", value: "experience" },
  { title: "Skills", value: "skills" },
  { title: "Projects", value: "projects" },
  { title: "Certifications", value: "certifications" },
  { title: "Achievements", value: "achievements" },
  { title: "Resume", value: "resume" },
];

export default function Sidebar() {
  const { page, setPage } = useApp();

  return (
    <div
      style={{
        width: 250,
        borderRight: "1px solid #2f3542",
        padding: 24,
        background: "#16171d",
        minHeight: "100vh",
      }}
    >
      <h2
        style={{
          color: "#ffffff",
          textAlign: "center",
          marginBottom: 6,
          fontSize: 28,
          fontWeight: 700,
        }}
      >
        ResumeAI
      </h2>

      <p
        style={{
          textAlign: "center",
          color: "#9ca3af",
          marginBottom: 25,
          fontSize: 13,
        }}
      >
        ATS Resume Builder
      </p>

      {menus.map((menu) => (
        <button
          key={menu.value}
          onClick={() => setPage(menu.value as any)}
          style={{
            display: "block",
            width: "100%",
            marginBottom: 10,
            padding: "14px",
            borderRadius: 10,
            border: "1px solid #374151",
            cursor: "pointer",
            fontSize: 15,
            fontWeight: 600,
            transition: "all 0.2s ease",

            background:
              page === menu.value ? "#2563eb" : "#1f2937",

            color: "#ffffff",
          }}
        >
          {menu.title}
        </button>
      ))}
    </div>
  );
}