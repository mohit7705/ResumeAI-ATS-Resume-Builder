import { useEffect, useState } from "react";
import { ChevronDown, Plus, Save, Wrench, X } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Chip from "../../components/ui/Chip";
import Toggle from "../../components/ui/Toggle";
import EmptyState from "../../components/ui/EmptyState";

import { useToast } from "../../context/ToastContext";

import {
  getSkills,
  saveSkills,
} from "../../services/skills";

type Skill = {
  name: string;
  enabled: boolean;
};

type SkillCategory = {
  enabled: boolean;
  skills: Skill[];
};

type SkillsData = Record<string, SkillCategory>;

const CATEGORY_TITLES: Record<string, string> = {
  languages: "Programming Languages",
  ai_ml: "AI / Machine Learning",
  databases: "Databases",
  cs_fundamentals: "CS Fundamentals",
  tools: "Tools & Technologies",
  cloud: "Cloud",
  soft_skills: "Soft Skills",
};

const DEFAULT_SKILLS: SkillsData = {
  languages: { enabled: true, skills: [] },
  ai_ml: { enabled: true, skills: [] },
  databases: { enabled: true, skills: [] },
  cs_fundamentals: { enabled: true, skills: [] },
  tools: { enabled: true, skills: [] },
  cloud: { enabled: true, skills: [] },
  soft_skills: { enabled: true, skills: [] },
};

function normalizeSkills(data: any): SkillsData {
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    return { ...DEFAULT_SKILLS };
  }

  const result: SkillsData = {};

  for (const [category, value] of Object.entries(data)) {
    // Support the old format: languages: ["Python", "Java"]
    if (Array.isArray(value)) {
      result[category] = {
        enabled: true,
        skills: value
          .filter((item) => typeof item === "string")
          .map((name) => ({ name, enabled: true })),
      };
      continue;
    }

    if (!value || typeof value !== "object") {
      continue;
    }

    const categoryData = value as any;

    result[category] = {
      enabled: categoryData.enabled !== false,
      skills: Array.isArray(categoryData.skills)
        ? categoryData.skills
            .map((item: any) => {
              if (typeof item === "string") {
                return { name: item, enabled: true };
              }

              if (
                item &&
                typeof item.name === "string"
              ) {
                return {
                  name: item.name,
                  enabled: item.enabled !== false,
                };
              }

              return null;
            })
            .filter(
              (item: Skill | null): item is Skill =>
                item !== null
            )
        : [],
    };
  }

  // Include expected categories missing from the response.
  for (const [category, value] of Object.entries(DEFAULT_SKILLS)) {
    if (!result[category]) {
      result[category] = {
        enabled: value.enabled,
        skills: [],
      };
    }
  }

  return result;
}

export default function SkillsModule() {
  const toast = useToast();

  const [skills, setSkills] = useState<SkillsData>(
    DEFAULT_SKILLS
  );

  const [values, setValues] = useState<Record<string, string>>(
    {}
  );

  const [open, setOpen] = useState<Record<string, boolean>>({
    languages: true,
  });

  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const data = await getSkills();
      setSkills(normalizeSkills(data));
      setDirty(false);
    } catch (error) {
      console.error("Failed to load skills:", error);
      toast.error("Could not load skills. Please try again.");
    }
  }

  function updateCategory(
    category: string,
    update: (current: SkillCategory) => SkillCategory
  ) {
    setDirty(true);

    setSkills((current) => ({
      ...current,
      [category]: update(
        current[category] ?? { enabled: true, skills: [] }
      ),
    }));
  }

  function toggleCategory(category: string, enabled: boolean) {
    updateCategory(category, (current) => ({
      ...current,
      enabled,
    }));
  }

  function toggleSkill(
    category: string,
    index: number,
    enabled: boolean
  ) {
    updateCategory(category, (current) => ({
      ...current,
      skills: current.skills.map((skill, i) =>
        i === index ? { ...skill, enabled } : skill
      ),
    }));
  }

  function add(category: string) {
    const value = (values[category] ?? "").trim();

    if (!value) return;

    const newNames = value
      .split(/[\n,]+/)
      .map((name) => name.trim())
      .filter(Boolean);

    updateCategory(category, (current) => {
      const existing = new Set(
        current.skills.map((skill) =>
          skill.name.trim().toLowerCase()
        )
      );

      const additions = newNames
        .filter((name) => {
          const key = name.toLowerCase();

          if (existing.has(key)) return false;

          existing.add(key);
          return true;
        })
        .map((name) => ({
          name,
          enabled: true,
        }));

      return {
        ...current,
        skills: [...current.skills, ...additions],
      };
    });

    setValues((current) => ({
      ...current,
      [category]: "",
    }));
  }

  function remove(category: string, index: number) {
    updateCategory(category, (current) => ({
      ...current,
      skills: current.skills.filter((_, i) => i !== index),
    }));
  }

  async function save() {
    setSaving(true);

    try {
      await saveSkills(skills);
      setDirty(false);
      toast.success("Skills saved.");
    } catch (error) {
      console.error("Failed to save skills:", error);
      toast.error("Could not save skills. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  const categories = Object.keys(skills);
  const allOpen = categories.every((category) => open[category]);

  function toggleAll() {
    const next: Record<string, boolean> = {};
    categories.forEach((category) => {
      next[category] = !allOpen;
    });
    setOpen(next);
  }

  function render(category: string, title: string) {
    const categoryData = skills[category];

    if (!categoryData) return null;

    const isOpen = Boolean(open[category]);
    const selected = categoryData.skills.filter((s) => s.enabled).length;

    return (
      <section className="card accordion" key={category}>
        <div className="accordion__head">
          <button
            type="button"
            className="accordion__trigger"
            aria-expanded={isOpen}
            aria-controls={`skills-${category}`}
            onClick={() =>
              setOpen((current) => ({
                ...current,
                [category]: !current[category],
              }))
            }
          >
            <span className="accordion__name">{title}</span>

            <Chip small tone={categoryData.enabled ? "accent" : "neutral"}>
              {categoryData.skills.length === 0
                ? "Empty"
                : `${selected} of ${categoryData.skills.length} selected`}
            </Chip>

            <span style={{ flex: 1 }} />

            <ChevronDown size={18} aria-hidden="true" />
          </button>

          <Toggle
            checked={categoryData.enabled}
            onChange={(event) =>
              toggleCategory(category, event.target.checked)
            }
            aria-label={`Show ${title} on resume`}
          >
            <span className="hide-xs">On resume</span>
          </Toggle>
        </div>

        {isOpen && (
          <div className="accordion__body" id={`skills-${category}`}>
            <div className="add-row">
              <Input
                placeholder="Add skills, separated by commas"
                aria-label={`Add skills to ${title}`}
                value={values[category] ?? ""}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    event.preventDefault();
                    add(category);
                  }
                }}
                onChange={(event) =>
                  setValues((current) => ({
                    ...current,
                    [category]: event.target.value,
                  }))
                }
              />

              <Button
                variant="secondary"
                icon={<Plus size={16} />}
                onClick={() => add(category)}
              >
                Add skills
              </Button>
            </div>

            {categoryData.skills.length === 0 ? (
              <EmptyState
                icon={<Wrench size={20} />}
                title="No skills added yet"
                text="Type a skill above and press Enter."
              />
            ) : (
              <ul className="skill-chips">
                {categoryData.skills.map((skill, index) => (
                  <li
                    key={`${skill.name}-${index}`}
                    className="skill-chip"
                    data-disabled={!categoryData.enabled}
                  >
                    <label>
                      <input
                        type="checkbox"
                        checked={skill.enabled}
                        disabled={!categoryData.enabled}
                        onChange={(event) =>
                          toggleSkill(
                            category,
                            index,
                            event.target.checked
                          )
                        }
                      />
                      <span>{skill.name}</span>
                    </label>

                    <button
                      type="button"
                      aria-label={`Remove ${skill.name}`}
                      onClick={() => remove(category, index)}
                    >
                      <X size={14} />
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </section>
    );
  }

  return (
    <Container>
      <SectionHeader
        title="Technical skills"
        subtitle="Tick the skills you want on your resume. Unticked skills stay saved but are left out."
        action={
          <Button variant="secondary" size="sm" onClick={toggleAll}>
            {allOpen ? "Collapse all" : "Expand all"}
          </Button>
        }
      />

      {categories.map((category) =>
        render(
          category,
          CATEGORY_TITLES[category] ?? category
        )
      )}

      <div className="savebar">
        <span className="savebar__text">
          <span className="dot" data-tone={dirty ? "warn" : "ok"} />
          {dirty ? "You have unsaved changes" : "All changes saved"}
        </span>

        <Button
          icon={<Save size={16} />}
          loading={saving}
          disabled={!dirty}
          onClick={save}
        >
          Save all skills
        </Button>
      </div>
    </Container>
  );
}
