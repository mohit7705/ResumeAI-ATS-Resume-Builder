import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import {
  getSkills,
  saveSkills,
} from "../../services/skills";

export default function SkillsModule() {
  const [skills, setSkills] = useState<any>({
    languages: [],
    frameworks: [],
    databases: [],
    tools: [],
    cloud: [],
    soft_skills: [],
  });

  const [values, setValues] = useState({
    languages: "",
    frameworks: "",
    databases: "",
    tools: "",
    cloud: "",
    soft_skills: "",
  });

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setSkills(await getSkills());
  }

  function add(category: string) {
    const value = values[category as keyof typeof values];

    if (!value.trim()) return;

    // Split by comma or newline
    const newSkills = value
      .split(/[\n,]+/)
      .map((skill) => skill.trim())
      .filter((skill) => skill.length > 0);

    // Remove duplicates (case-insensitive)
    const existing = skills[category].map((item: string) =>
      item.toLowerCase()
    );

    const merged = [...skills[category]];
    newSkills.forEach((skill) => {
      if (!existing.includes(skill.toLowerCase())) {
        merged.push(skill);
      }
    });

    setSkills({
      ...skills,
      [category]: merged,
    });

    setValues({
      ...values,
      [category]: "",
    });
  }

  async function save() {
    await saveSkills(skills);
    alert("Saved");
  }

  function remove(category: string, index: number) {
    const updated = [...skills[category]];
    updated.splice(index, 1);

    setSkills({
      ...skills,
      [category]: updated,
    });
  }

  function render(category: string, title: string) {
    return (
      <Card title={title}>
        <Input
          value={values[category as keyof typeof values]}
          onChange={(e) =>
            setValues({
              ...values,
              [category]: e.target.value,
            })
          }
        />

        <Button onClick={() => add(category)}>
          Add
        </Button>

        <br />
        <br />

        {skills[category]?.map((item: string, index: number) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: 10,
            }}
          >
            {item}

            <Button
              style={{ background: "#dc2626" }}
              onClick={() => remove(category, index)}
            >
              Delete
            </Button>
          </div>
        ))}
      </Card>
    );
  }

  return (
    <Container>
      <SectionHeader
        title="Skills"
        subtitle="Manage Skills"
      />

      {render("languages", "Programming Languages")}
      {render("frameworks", "Frameworks")}
      {render("databases", "Databases")}
      {render("tools", "Tools")}
      {render("cloud", "Cloud")}
      {render("soft_skills", "Soft Skills")}

      <Button onClick={save}>
        Save All Skills
      </Button>
    </Container>
  );
}