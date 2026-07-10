import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";

import StatCard from "./components/StatCard";
import QuickAction from "./components/QuickAction";
import RecentProjects from "./components/RecentProjects";
import ProfileCompletion from "./components/ProfileCompletion";

import { getDashboard } from "../../services/dashboard";

export default function DashboardModule() {
  const [stats, setStats] = useState({
    projects: 0,
    skills: 0,
    certifications: 0,
    achievements: 0,
  });

  useEffect(() => {
    load();
  }, []);

  async function load() {
    const data = await getDashboard();
    setStats(data);
  }

  return (
    <Container>
      <SectionHeader
        title="Dashboard"
        subtitle="Build an ATS-friendly resume with AI"
      />
      <p
        style={{
        color: "#9ca3af",
        marginBottom: 25,
        fontSize: 15,
       }}
       >
         Complete your profile, add your projects and skills, then generate an ATS-friendly resume tailored to your target job.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))",
          gap: 20,
        }}
      >
        <StatCard
          title="Projects"
          value={String(stats.projects)}
        />

        <StatCard
          title="Skills"
          value={String(stats.skills)}
        />

        <StatCard
          title="Certifications"
          value={String(stats.certifications)}
        />

        <StatCard
          title="Achievements"
          value={String(stats.achievements)}
        />
      </div>

      <br />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 20,
        }}
      >
        <ProfileCompletion />

        <div
          style={{
            background: "#111827",
            padding: 20,
            borderRadius: 12,
            border: "1px solid #333",
          }}
        >
          <h2
                style={{
                 marginBottom: 20,
                }}
              >
              Quick Actions
          </h2>

          <QuickAction
            title="Generate Resume"
            action="generate"
          />

          <QuickAction
            title="Preview Resume"
            action="preview"
          />

          <QuickAction
            title="Download PDF"
            action="download"
          />
        </div>
      </div>

      <br />

      <RecentProjects />
    </Container>
  );
}