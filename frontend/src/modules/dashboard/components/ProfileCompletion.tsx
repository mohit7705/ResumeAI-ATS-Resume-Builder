import { useEffect, useState } from "react";

import { getProfile } from "../../../services/personal";
import { getSkills } from "../../../services/skills";
import { getProjects } from "../../../services/projects";
import { getEducation } from "../../../services/education";
import { getCertifications } from "../../../services/certifications";
import { getAchievements } from "../../../services/achievements";


export default function ProfileCompletion() {

  const [percentage, setPercentage] = useState(0);


  useEffect(() => {
    calculate();
  }, []);


  async function calculate() {

    let completed = 0;
    const total = 6;


    const profile = await getProfile();

    if (
      profile.first_name &&
      profile.last_name &&
      profile.professional_title
    ) {
      completed++;
    }


    const skills = await getSkills();

    if (
      Object.values(skills)
        .some((item:any) => item.length > 0)
    ) {
      completed++;
    }


    const projects = await getProjects();

    if (projects.length > 0) {
      completed++;
    }


    const education = await getEducation();

    if (education.length > 0) {
      completed++;
    }


    const certifications = await getCertifications();

    if (certifications.length > 0) {
      completed++;
    }


    const achievements = await getAchievements();

    if (achievements.length > 0) {
      completed++;
    }


    setPercentage(
      Math.round((completed / total) * 100)
    );
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

      <h2>
        Profile Completion
      </h2>


      <h1>
        {percentage}%
      </h1>


      <div
        style={{
          height: 10,
          background: "#374151",
          borderRadius: 10,
        }}
      >

        <div
          style={{
            width: `${percentage}%`,
            height: "100%",
            borderRadius: 10,
            background: "#2563eb",
          }}
        />

      </div>


    </div>
  );
}