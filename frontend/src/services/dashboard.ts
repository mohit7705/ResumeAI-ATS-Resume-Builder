import axios from "axios";

const API = "http://127.0.0.1:8000";

export async function getDashboard() {
  const [projects, skills, certifications, achievements] =
    await Promise.all([
      axios.get(`${API}/projects/`),
      axios.get(`${API}/skills/`),
      axios.get(`${API}/certifications/`),
      axios.get(`${API}/achievements/`),
    ]);

  const skillCount = Object.values(skills.data).reduce(
    (total: number, list: any) => total + list.length,
    0
  );

  return {
    projects: projects.data.length,
    skills: skillCount,
    certifications: certifications.data.length,
    achievements: achievements.data.length,
  };
}