import { useEffect, useState } from "react";
import { Calendar, GraduationCap, Plus } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Chip from "../../components/ui/Chip";
import EmptyState from "../../components/ui/EmptyState";
import DeleteButton from "../../components/ui/DeleteButton";

import { useToast } from "../../context/ToastContext";
import { formatRange } from "../../utils/format";

import {
  getEducation,
  addEducation,
  deleteEducation,
} from "../../services/education";

export default function EducationModule() {
  const toast = useToast();

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
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setEducation(await getEducation());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your education. Check that the backend is running.");
    }
  }

  async function add() {

    if (!form.degree.trim()) {
      toast.error("Degree is required.");
      return;
    }

    if (!form.specialization.trim()) {
      toast.error("Specialization is required.");
      return;
    }

    if (!form.college.trim()) {
      toast.error("College name is required.");
      return;
    }

    if (!form.start_date) {
      toast.error("Start date is required.");
      return;
    }

    if (!form.end_date) {
      toast.error("End date is required.");
      return;
    }

    if (form.cgpa) {

      const cgpa = Number(form.cgpa);

      if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
        toast.error("CGPA must be between 0 and 10.");
        return;
      }

    }

    setSaving(true);

    try {
      await addEducation(form);

      setForm(empty);

      load();

      toast.success("Education added.");
    } catch (error) {
      console.error(error);
      toast.error("Could not add this education. Please try again.");
    } finally {
      setSaving(false);
    }

  }

  async function remove(index: number) {
    try {
      await deleteEducation(index);
      load();
      toast.success("Education removed.");
    } catch (error) {
      console.error(error);
      toast.error("Could not remove this education. Please try again.");
    }
  }

  return (
    <Container>
      <SectionHeader
        title="Education"
        subtitle="Add your degrees, colleges and results."
      />

      <Card
        title="Add education"
        footer={
          <Button
            icon={<Plus size={16} />}
            loading={saving}
            onClick={add}
          >
            Add education
          </Button>
        }
      >
        <div className="form-grid">
          <Field label="Degree" required>
            <Input
              placeholder="Bachelor of Technology"
              value={form.degree}
              onChange={(e) =>
                setForm({
                  ...form,
                  degree: e.target.value,
                })
              }
            />
          </Field>

          <Field label="Specialization" required>
            <Input
              placeholder="Artificial Intelligence & Machine Learning"
              value={form.specialization}
              onChange={(e) =>
                setForm({
                  ...form,
                  specialization: e.target.value,
                })
              }
            />
          </Field>

          <Field label="College" required>
            <Input
              value={form.college}
              onChange={(e) =>
                setForm({
                  ...form,
                  college: e.target.value,
                })
              }
            />
          </Field>

          <Field label="University">
            <Input
              value={form.university}
              onChange={(e) =>
                setForm({
                  ...form,
                  university: e.target.value,
                })
              }
            />
          </Field>

          <Field label="CGPA" hint="Out of 10">
            <Input
              inputMode="decimal"
              value={form.cgpa}
              onChange={(e) =>
                setForm({
                  ...form,
                  cgpa: e.target.value,
                })
              }
            />
          </Field>

          <div className="form-grid">
            <Field label="Start date" required>
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

            <Field label="End date" required>
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
          </div>
        </div>
      </Card>

      <Card
        title="Your education"
        action={
          education.length > 0 ? (
            <Chip>{education.length}</Chip>
          ) : undefined
        }
      >
        {education.length === 0 ? (
          <EmptyState
            icon={<GraduationCap size={20} />}
            title="No education added yet"
            text="Add your degree above and it will appear on your resume."
          />
        ) : (
          <div className="item-grid">
            {education.map((item, index) => {
              const range = formatRange(item.start_date, item.end_date);

              return (
                <article className="item" key={index}>
                  <div className="item__top">
                    <div>
                      <h3 className="item__title">{item.degree}</h3>
                      <p className="item__sub">{item.specialization}</p>
                    </div>

                    <DeleteButton onConfirm={() => remove(index)} />
                  </div>

                  <div className="item__meta">
                    <span>
                      <GraduationCap size={14} />
                      {[item.college, item.university]
                        .filter(Boolean)
                        .join(", ")}
                    </span>

                    {range && (
                      <span>
                        <Calendar size={14} />
                        {range}
                      </span>
                    )}
                  </div>

                  {item.cgpa && <Chip tone="accent" small>CGPA {item.cgpa}</Chip>}
                </article>
              );
            })}
          </div>
        )}
      </Card>
    </Container>
  );
}
