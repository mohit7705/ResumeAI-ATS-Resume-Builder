import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

import {
  getEducation,
  addEducation,
  deleteEducation,
} from "../../services/education";

export default function EducationModule() {
  const empty = {
    degree: "",
    specialization: "",
    college: "",
    university: "",
    cgpa: "",
    start_date: "",
    end_date: "",
  };

  const [education, setEducation] = useState<any[]>([]);
  const [form, setForm] = useState(empty);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setEducation(await getEducation());
  }

  async function add() {

  if (!form.degree.trim()) {
    alert("Degree is required.");
    return;
  }

  if (!form.specialization.trim()) {
    alert("Specialization is required.");
    return;
  }

  if (!form.college.trim()) {
    alert("College name is required.");
    return;
  }

  if (!form.start_date) {
    alert("Start date is required.");
    return;
  }

  if (!form.end_date) {
    alert("End date is required.");
    return;
  }

  if (form.cgpa) {

    const cgpa = Number(form.cgpa);

    if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
      alert("CGPA must be between 0 and 10.");
      return;
    }

  }

  await addEducation(form);

  setForm(empty);

  load();

  alert("Education Added Successfully.");

}

  async function remove(index: number) {
    await deleteEducation(index);
    load();
  }

  return (
    <Container>
      <SectionHeader
        title="Education"
        subtitle="Manage Education"
      />

      <Card title="Add Education">

        <Label>Degree</Label>
        <Input
          value={form.degree}
          onChange={(e) =>
            setForm({
              ...form,
              degree: e.target.value,
            })
          }
        />

        <Label>Specialization</Label>
        <Input
          value={form.specialization}
          onChange={(e) =>
            setForm({
              ...form,
              specialization: e.target.value,
            })
          }
        />

        <Label>College</Label>
        <Input
          value={form.college}
          onChange={(e) =>
            setForm({
              ...form,
              college: e.target.value,
            })
          }
        />

        <Label>University</Label>
        <Input
          value={form.university}
          onChange={(e) =>
            setForm({
              ...form,
              university: e.target.value,
            })
          }
        />

        <Label>CGPA</Label>
        <Input
          value={form.cgpa}
          onChange={(e) =>
            setForm({
              ...form,
              cgpa: e.target.value,
            })
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

        <Button onClick={add}>
          Add Education
        </Button>

      </Card>

      <Card title="Education List">

        {education.map((item, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #333",
              borderRadius: 8,
              padding: 15,
              marginBottom: 15,
            }}
          >
            <h3>{item.degree}</h3>

            <p>{item.specialization}</p>

            <p>{item.college}</p>

            <Button
              style={{
                background: "#dc2626",
              }}
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