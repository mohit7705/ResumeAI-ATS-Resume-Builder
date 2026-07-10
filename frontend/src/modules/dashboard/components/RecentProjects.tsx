import { useEffect, useState } from "react";

import { getProjects } from "../../../services/projects";

export default function RecentProjects() {

  const [projects, setProjects] = useState<any[]>([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    const data = await getProjects();
    setProjects(data.slice(0, 3));
  }

  return (
    <div
      style={{
        background: "#111827",
        padding: 20,
        borderRadius: 12,
        border: "1px solid #333",
      }}
    >
      <h2>Recent Projects</h2>

      {projects.length === 0 ? (
        <p>No projects added.</p>
      ) : (
        <ul
          style={{
            paddingLeft: 20,
            marginTop: 15,
          }}
        >
          {projects.map((project, index) => (
            <li
              key={index}
              style={{
                marginBottom: 10,
              }}
            >
              <strong>{project.title}</strong>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}