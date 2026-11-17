import { useEffect, useState } from "react";
import { Calendar, Plus, Trophy } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import Input from "../../components/ui/Input";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";
import Chip from "../../components/ui/Chip";
import EmptyState from "../../components/ui/EmptyState";
import DeleteButton from "../../components/ui/DeleteButton";

import { useToast } from "../../context/ToastContext";
import { formatDate } from "../../utils/format";

import {
  getAchievements,
  addAchievement,
  deleteAchievement,
} from "../../services/achievements";

export default function AchievementsModule() {
  const toast = useToast();

  const empty = {
    title: "",
    description: "",
    date: "",
  };

  const [form, setForm] = useState(empty);
  const [items, setItems] = useState<any[]>([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setItems(await getAchievements());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your achievements. Check that the backend is running.");
    }
  }

  async function add() {

    if (!form.title.trim()) {
      toast.error("Achievement title is required.");
      return;
    }

    if (!form.description.trim()) {
      toast.error("Achievement description is required.");
      return;
    }

    if (!form.date) {
      toast.error("Achievement date is required.");
      return;
    }

    setSaving(true);

    try {
      await addAchievement(form);

      setForm(empty);

      load();

      toast.success("Achievement added.");
    } catch (error) {
      console.error(error);
      toast.error("Could not add this achievement. Please try again.");
    } finally {
      setSaving(false);
    }

  }

  async function remove(index: number) {
    try {
      await deleteAchievement(index);
      load();
      toast.success("Achievement removed.");
    } catch (error) {
      console.error(error);
      toast.error("Could not remove this achievement. Please try again.");
    }
  }

  return (
    <Container>
      <SectionHeader
        title="Achievements"
        subtitle="Awards, rankings and milestones worth mentioning."
      />

      <Card
        title="Add achievement"
        footer={
          <Button
            icon={<Plus size={16} />}
            loading={saving}
            onClick={add}
          >
            Add achievement
          </Button>
        }
      >
        <div className="form-grid">
          <Field label="Title" required>
            <Input
              value={form.title}
              onChange={(e) =>
                setForm({ ...form, title: e.target.value })
              }
            />
          </Field>

          <Field label="Date" required>
            <Input
              type="date"
              value={form.date}
              onChange={(e) =>
                setForm({ ...form, date: e.target.value })
              }
            />
          </Field>

          <Field label="Description" required wide>
            <TextArea
              rows={4}
              value={form.description}
              onChange={(e) =>
                setForm({
                  ...form,
                  description: e.target.value,
                })
              }
            />
          </Field>
        </div>
      </Card>

      <Card
        title="Your achievements"
        action={items.length > 0 ? <Chip>{items.length}</Chip> : undefined}
      >
        {items.length === 0 ? (
          <EmptyState
            icon={<Trophy size={20} />}
            title="No achievements yet"
            text="Hackathon wins, scholarships and competition ranks all count."
          />
        ) : (
          <div className="item-grid">
            {items.map((item, index) => (
              <article className="item" key={index}>
                <div className="item__top">
                  <div>
                    <h3 className="item__title">{item.title}</h3>
                    {item.date && (
                      <div className="item__meta" style={{ marginTop: 4 }}>
                        <span>
                          <Calendar size={14} />
                          {formatDate(item.date)}
                        </span>
                      </div>
                    )}
                  </div>

                  <DeleteButton onConfirm={() => remove(index)} />
                </div>

                {item.description && (
                  <p className="item__sub" style={{ marginTop: 0 }}>
                    {item.description}
                  </p>
                )}
              </article>
            ))}
          </div>
        )}
      </Card>
    </Container>
  );
}
