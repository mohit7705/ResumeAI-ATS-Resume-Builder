import { useEffect, useState } from "react";
import {
  Award,
  Folder,
  Sparkles,
  Trophy,
  Wrench,
} from "lucide-react";

import Container from "../../components/ui/Container";
import Button from "../../components/ui/Button";

import StatCard from "./components/StatCard";
import QuickAction from "./components/QuickAction";
import RecentProjects from "./components/RecentProjects";
import ProfileCompletion from "./components/ProfileCompletion";

import { useApp } from "../../context/AppContext";
import { useToast } from "../../context/ToastContext";
import { getDashboard } from "../../services/dashboard";
import { getProfile } from "../../services/personal";

function greeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

export default function DashboardModule() {
  const { setPage } = useApp();
  const toast = useToast();

  const [stats, setStats] = useState({
    projects: 0,
    skills: 0,
    certifications: 0,
    achievements: 0,
  });

  const [firstName, setFirstName] = useState("");

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const data = await getDashboard();
      setStats(data);
    } catch (error) {
      console.error(error);
      toast.error(
        "Could not load your dashboard. Check that the backend is running."
      );
    }

    try {
      const profile = await getProfile();
      setFirstName(profile?.first_name ?? "");
    } catch {
      /* the greeting works without a name */
    }
  }

  return (
    <Container>
      <section className="hero">
        <h1 className="hero__title">
          {greeting()}
          {firstName ? `, ${firstName}.` : "."}
        </h1>

        <p className="hero__text">
          Keep your details in one place, then paste a job description and get
          an ATS-friendly resume tailored to that role.
        </p>

        <div className="hero__actions">
          <Button
            size="lg"
            icon={<Sparkles size={18} />}
            onClick={() => setPage("resume")}
          >
            Generate resume
          </Button>
        </div>
      </section>

      <div className="stat-grid">
        <StatCard
          title="Projects"
          value={String(stats.projects)}
          icon={Folder}
          onClick={() => setPage("projects")}
        />

        <StatCard
          title="Skills"
          value={String(stats.skills)}
          icon={Wrench}
          onClick={() => setPage("skills")}
        />

        <StatCard
          title="Certifications"
          value={String(stats.certifications)}
          icon={Award}
          onClick={() => setPage("certifications")}
        />

        <StatCard
          title="Achievements"
          value={String(stats.achievements)}
          icon={Trophy}
          onClick={() => setPage("achievements")}
        />
      </div>

      <div className="dash-grid">
        <ProfileCompletion />

        <section className="card">
          <header className="card__head">
            <div>
              <h2 className="card__title">Quick actions</h2>
              <p className="card__desc">Jump straight to your resume.</p>
            </div>
          </header>

          <div className="card__body">
            <div className="action-list">
              <QuickAction
                title="Generate resume"
                description="Tailor a new resume to a job"
                action="generate"
              />

              <QuickAction
                title="Preview resume"
                description="Open your latest HTML resume"
                action="preview"
              />

              <QuickAction
                title="Download PDF"
                description="Save your latest resume as a PDF"
                action="download"
              />
            </div>
          </div>
        </section>

        <div className="dash-span">
          <RecentProjects />
        </div>
      </div>
    </Container>
  );
}
