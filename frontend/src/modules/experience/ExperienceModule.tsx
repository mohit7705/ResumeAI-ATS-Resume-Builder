import { useEffect, useState } from "react";
import { Briefcase, Calendar, MapPin, Plus } from "lucide-react";

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
import { formatRange, toList } from "../../utils/format";

import {
  getExperience,
  addExperience,
  deleteExperience,
} from "../../services/experience";

export default function ExperienceModule() {
  const toast = useToast();

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
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setExperience(await getExperience());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your experience. Check that the backend is running.");
    }
  }

  async function add() {
    // Added so empty entries (the blank card in the old list) can't be saved.
    if (!form.company.trim()) {
      toast.error("Company is required.");
      return;
    }

    if (!form.position.trim()) {
      toast.error("Position is required.");
      return;
    }

    setSaving(true);

    try {
      await addExperience(form);
      setForm(empty);
      load();
      toast.success("Experience added.");
    } catch (error) {
      console.error(error);
      toast.error("Could not add this experience. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  async function remove(index: number) {
    try {
      await deleteExperience(index);
      load();
      toast.success("Experience removed.");
    } catch (error) {
      console.error(error);
      toast.error("Could not remove this experience. Please try again.");
    }
  }

  return (
    <Container>
      <SectionHeader
        title="Experience"
        subtitle="Internships, jobs and freelance work. Leave the end date empty if you still work there."
      />

      <Card
        title="Add experience"
        footer={
          <Button
            icon={<Plus size={16} />}
            loading={saving}
            onClick={add}
          >
            Add experience
          </Button>
        }
      >
        <div className="form-grid">
          <Field label="Company" required>
            <Input
              value={form.company}
              onChange={(e) =>
                setForm({ ...form, company: e.target.value })
              }
            />
          </Field>

          <Field label="Position" required>
            <Input
              value={form.position}
              onChange={(e) =>
                setForm({ ...form, position: e.target.value })
              }
            />
          </Field>

          <Field label="Employment type" hint="Internship, Full-time, Freelance…">
            <Input
              value={form.employment_type}
              onChange={(e) =>
                setForm({
                  ...form,
                  employment_type: e.target.value,
                })
              }
            />
          </Field>

          <Field label="Location">
            <Input
              value={form.location}
              onChange={(e) =>
                setForm({ ...form, location: e.target.value })
              }
            />
          </Field>

          <Field label="Start date">
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
          </Field>

          <Field label="End date">
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
          </Field>

          <Field
            label="Technologies"
            wide
            hint="Separate with commas, for example Python, FastAPI, React"
          >
            <Input
              value={form.technologies}
              onChange={(e) =>
                setForm({
                  ...form,
                  technologies: e.target.value,
                })
              }
            />
          </Field>

          <Field label="Responsibilities" wide hint="One responsibility per line">
            <TextArea
              rows={5}
              value={form.responsibilities}
              onChange={(e) =>
                setForm({
                  ...form,
                  responsibilities: e.target.value,
                })
              }
            />
          </Field>
        </div>
      </Card>

      <Card
        title="Your experience"
        action={
          experience.length > 0 ? (
            <Chip>{experience.length}</Chip>
          ) : undefined
        }
      >
        {experience.length === 0 ? (
          <EmptyState
            icon={<Briefcase size={20} />}
            title="No experience added yet"
            text="Freshers can add internships, freelance work or open-source contributions."
          />
        ) : (
          <div className="item-grid">
            {experience.map((item, index) => {
              const range = formatRange(item.start_date, item.end_date);
              const tech = toList(item.technologies);
              const duties = toList(item.responsibilities, /\n+/);
              const hasContent = item.position || item.company;

              return (
                <article className="item" key={index}>
                  <div className="item__top">
                    <div>
                      <h3 className="item__title">
                        {item.position || "Untitled role"}
                      </h3>
                      <p className="item__sub">
                        {[item.company, item.employment_type]
                          .filter(Boolean)
                          .join(" · ") ||
                          (hasContent ? "" : "No company or position saved")}
                      </p>
                    </div>

                    <DeleteButton onConfirm={() => remove(index)} />
                  </div>

                  {(item.location || range) && (
                    <div className="item__meta">
                      {item.location && (
                        <span>
                          <MapPin size={14} />
                          {item.location}
                        </span>
                      )}

                      {range && (
                        <span>
                          <Calendar size={14} />
                          {range}
                        </span>
                      )}
                    </div>
                  )}

                  {duties.length > 0 && (
                    <ul className="item__list">
                      {duties.slice(0, 3).map((duty, i) => (
                        <li key={i}>{duty}</li>
                      ))}
                    </ul>
                  )}

                  {tech.length > 0 && (
                    <div className="chips">
                      {tech.map((t) => (
                        <Chip key={t} small>
                          {t}
                        </Chip>
                      ))}
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        )}
      </Card>
    </Container>
  );
}
