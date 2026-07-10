import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";

import {
  getAchievements,
  addAchievement,
  deleteAchievement,
} from "../../services/achievements";

export default function AchievementsModule() {
  const empty = {
    title: "",
    description: "",
    date: "",
  };

  const [form, setForm] = useState(empty);
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setItems(await getAchievements());
  }

  async function add() {

  if (!form.title.trim()) {
    alert("Achievement title is required.");
    return;
  }

  if (!form.description.trim()) {
    alert("Achievement description is required.");
    return;
  }

  if (!form.date) {
    alert("Achievement date is required.");
    return;
  }

  await addAchievement(form);

  setForm(empty);

  load();

  alert("Achievement Added Successfully.");

  }

  async function remove(index: number) {
    await deleteAchievement(index);
    load();
  }

  return (
    <Container>
      <SectionHeader
        title="Achievements"
        subtitle="Manage Achievements"
      />

      <Card title="Add Achievement">
        <Label>Title</Label>
        <Input
          value={form.title}
          onChange={(e) =>
            setForm({ ...form, title: e.target.value })
          }
        />

        <Label>Description</Label>
        <TextArea
          value={form.description}
          onChange={(e) =>
            setForm({
              ...form,
              description: e.target.value,
            })
          }
        />

        <Label>Date</Label>
        <Input
          type="date"
          value={form.date}
          onChange={(e) =>
            setForm({ ...form, date: e.target.value })
          }
        />

        <Button onClick={add}>
          Add Achievement
        </Button>
      </Card>

      <Card title="Achievement List">
        {items.map((item, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #333",
              padding: 15,
              borderRadius: 8,
              marginBottom: 15,
            }}
          >
            <h3>{item.title}</h3>

            <p>{item.description}</p>

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