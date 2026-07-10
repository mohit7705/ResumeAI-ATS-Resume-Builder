import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";

import {
  getExperience,
  addExperience,
  deleteExperience,
} from "../../services/experience";

export default function ExperienceModule() {
  const empty = {
    company: "",
    position: "",
    employment_type: "",
    location: "",
    start_date: "",
    end_date: "",
    technologies: "",
    responsibilities: "",
  };

  const [form, setForm] = useState(empty);
  const [experience, setExperience] = useState<any[]>([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setExperience(await getExperience());
  }

  async function add() {
    await addExperience(form);
    setForm(empty);
    load();
  }

  async function remove(index: number) {
    await deleteExperience(index);
    load();
  }

  return (
    <Container>
      <SectionHeader
        title="Experience"
        subtitle="Manage Experience"
      />

      <Card title="Add Experience">
        <Label>Company</Label>
        <Input
          value={form.company}
          onChange={(e) =>
            setForm({ ...form, company: e.target.value })
          }
        />

        <Label>Position</Label>
        <Input
          value={form.position}
          onChange={(e) =>
            setForm({ ...form, position: e.target.value })
          }
        />

        <Label>Employment Type</Label>
        <Input
          value={form.employment_type}
          onChange={(e) =>
            setForm({
              ...form,
              employment_type: e.target.value,
            })
          }
        />

        <Label>Location</Label>
        <Input
          value={form.location}
          onChange={(e) =>
            setForm({ ...form, location: e.target.value })
          }
        />

        <Label>Start Date</Label>
        <Input
          type="month"
          value={form.start_date}
          onChange={(e) =>
            setForm({
              ...form,
              start_date: e.target.value,
            })
          }
        />

        <Label>End Date</Label>
        <Input
          type="month"
          value={form.end_date}
          onChange={(e) =>
            setForm({
              ...form,
              end_date: e.target.value,
            })
          }
        />

        <Label>Technologies</Label>
        <Input
          value={form.technologies}
          onChange={(e) =>
            setForm({
              ...form,
              technologies: e.target.value,
            })
          }
        />

        <Label>Responsibilities</Label>
        <TextArea
          value={form.responsibilities}
          onChange={(e) =>
            setForm({
              ...form,
              responsibilities: e.target.value,
            })
          }
        />

        <Button onClick={add}>
          Add Experience
        </Button>
      </Card>

      <Card title="Experience List">
        {experience.map((item, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #333",
              borderRadius: 8,
              padding: 15,
              marginBottom: 15,
            }}
          >
            <h3>{item.position}</h3>

            <p>{item.company}</p>

            <p>{item.location}</p>

            <Button
              style={{ background: "#dc2626" }}
              onClick={() => remove(index)}
            >
              Delete
            </Button>
          </div>
        ))}
      </Card>
    </Container>
  );
}