import axios from "axios";
import { countSkills } from "../utils/skills";

const API = "";

export async function getDashboard() {
  const [projects, skills, certifications, achievements] =
    await Promise.all([
      axios.get(`${API}/projects/`),
      axios.get(`${API}/skills/`),
      axios.get(`${API}/certifications/`),
      axios.get(`${API}/achievements/`),
    ]);

  return {
    projects: projects.data.length,
    // Fixed: skills now arrive as { category: { enabled, skills: [] } },
    // so the old `list.length` produced NaN.
    skills: countSkills(skills.data),
    certifications: certifications.data.length,
    achievements: achievements.data.length,
  };
}
