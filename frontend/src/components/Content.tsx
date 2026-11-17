import { useApp } from "../context/AppContext";

import DashboardModule from "../modules/dashboard/DashboardModule";
import PersonalModule from "../modules/personal/PersonalModule";
import ContactModule from "../modules/contact/ContactModule";
import SummaryModule from "../modules/summary/SummaryModule";
import EducationModule from "../modules/education/EducationModule";
import ExperienceModule from "../modules/experience/ExperienceModule";
import SkillsModule from "../modules/skills/SkillsModule";
import ProjectsModule from "../modules/projects/ProjectsModule";
import CertificationsModule from "../modules/certifications/CertificationsModule";
import AchievementsModule from "../modules/achievements/AchievementsModule";
import ResumeModule from "../modules/resume/ResumeModule";

export default function Content() {
  const { page } = useApp();

  return (
    <>
      {page === "dashboard" && <DashboardModule />}
      {page === "profile" && <PersonalModule />}
      {page === "contact" && <ContactModule />}
      {page === "summary" && <SummaryModule />}
      {page === "education" && <EducationModule />}
      {page === "experience" && <ExperienceModule />}
      {page === "skills" && <SkillsModule />}
      {page === "projects" && <ProjectsModule />}
      {page === "certifications" && <CertificationsModule />}
      {page === "achievements" && <AchievementsModule />}
      {page === "resume" && <ResumeModule />}
    </>
  );
}
