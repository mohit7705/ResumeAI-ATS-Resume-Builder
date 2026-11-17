import { useEffect, useState } from "react";
import { Check } from "lucide-react";

import Card from "../../../components/ui/Card";
import Ring from "../../../components/ui/Ring";
import { useApp } from "../../../context/AppContext";
import type { Page } from "../../../context/AppContext";

import { getProfile } from "../../../services/personal";
import { getSkills } from "../../../services/skills";
import { getProjects } from "../../../services/projects";
import { getEducation } from "../../../services/education";
import { getCertifications } from "../../../services/certifications";
import { getAchievements } from "../../../services/achievements";
import { hasSkills } from "../../../utils/skills";

type Step = {
  label: string;
  page: Page;
  done: boolean;
};

export default function ProfileCompletion() {
  const { setPage } = useApp();

  const [percentage, setPercentage] = useState(0);
  const [steps, setSteps] = useState<Step[]>([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    calculate();
  }, []);

  async function calculate() {
    try {
      const profile = await getProfile();
      const skills = await getSkills();
      const projects = await getProjects();
      const education = await getEducation();
      const certifications = await getCertifications();
      const achievements = await getAchievements();

      const result: Step[] = [
        {
          label: "Profile details",
          page: "profile",
          done: Boolean(
            profile.first_name &&
              profile.last_name &&
              profile.professional_title
          ),
        },
        {
          label: "Technical skills",
          page: "skills",
          // Skills now arrive as { category: { enabled, skills: [] } }.
          done: hasSkills(skills),
        },
        {
          label: "Projects",
          page: "projects",
          done: projects.length > 0,
        },
        {
          label: "Education",
          page: "education",
          done: education.length > 0,
        },
        {
          label: "Certifications",
          page: "certifications",
          done: certifications.length > 0,
        },
        {
          label: "Achievements",
          page: "achievements",
          done: achievements.length > 0,
        },
      ];

      const completed = result.filter((step) => step.done).length;

      setSteps(result);
      setPercentage(Math.round((completed / result.length) * 100));
    } catch (error) {
      console.error(error);
    } finally {
      setLoaded(true);
    }
  }

  return (
    <Card
      title="Profile completion"
      description="Complete sections give the generator more to work with."
    >
      <div className="completion">
        <Ring
          value={percentage}
          tone={percentage === 100 ? "ok" : "accent"}
        />

        {loaded && steps.length === 0 ? (
          <p className="muted">
            Could not load your profile. Check that the backend is running.
          </p>
        ) : (
          <ul className="checklist">
            {steps.map((step) => (
              <li key={step.label} data-done={step.done}>
                <span className="checklist__mark" aria-hidden="true">
                  <Check size={12} strokeWidth={3} />
                </span>

                <span className="checklist__label">{step.label}</span>

                {!step.done && (
                  <button type="button" onClick={() => setPage(step.page)}>
                    Add
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </Card>
  );
}
