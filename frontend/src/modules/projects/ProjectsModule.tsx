import { useEffect, useState } from "react";
import { ExternalLink, Folder, Link as LinkIcon, Plus } from "lucide-react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Field from "../../components/ui/Field";
import Input from "../../components/ui/Input";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";
import Chip from "../../components/ui/Chip";
import Toggle from "../../components/ui/Toggle";
import EmptyState from "../../components/ui/EmptyState";
import DeleteButton from "../../components/ui/DeleteButton";

import { useToast } from "../../context/ToastContext";
import { toList } from "../../utils/format";

import {
  getProjects,
  addProject,
  deleteProject,
} from "../../services/projects";

export default function ProjectsModule() {
  const toast = useToast();

  const empty = {
    title: "",
    github: "",
    live_demo: "",
    technologies: "",
    highlights: "",
    keywords: "",
    featured: false,
  };

  const [form, setForm] = useState(empty);
  const [projects, setProjects] = useState<any[]>([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setProjects(await getProjects());
    } catch (error) {
      console.error(error);
      toast.error("Could not load your projects. Check that the backend is running.");
    }
  }

  async function save() {

    if (!form.title.trim()) {
      toast.error("Project title is required.");
      return;
    }

    if (!form.github.trim()) {
      toast.error("GitHub URL is required.");
      return;
    }

    if (
      !form.github.startsWith("https://github.com/")
    ) {
      toast.error("Enter a valid GitHub URL.");
      return;
    }

    if (
      form.live_demo &&
      !/^https?:\/\/.+/.test(form.live_demo)
    ) {
      toast.error("Enter a valid Live Demo URL.");
      return;
    }

    if (!form.technologies.trim()) {
      toast.error("Technologies are required.");
      return;
    }

    if (!form.highlights.trim()) {
      toast.error("Project highlights are required.");
      return;
    }

    if (!form.keywords.trim()) {
      toast.error("Project keywords are required.");
      return;
    }

    setSaving(true);

    try {
      await addProject({
        title: form.title,
        github: form.github,
        live_demo: form.live_demo,

        technologies: form.technologies
          .split(",")
          .map(item => item.trim())
          .filter(Boolean),

        highlights: form.highlights
          .split("\n")
          .map(item => item.trim())
          .filter(Boolean),

        keywords: form.keywords
          .split(",")
          .map(item => item.trim())
          .filter(Boolean),

        featured: form.featured,
      });

      setForm(empty);

      load();

      toast.success("Project added.");
    } catch (error) {
      console.error(error);
      toast.error("Could not add this project. Please try again.");
    } finally {
      setSaving(false);
    }

  }

  async function remove(index: number) {
    try {
      await deleteProject(index);
      load();
      toast.success("Project removed.");
    } catch (error) {
      console.error(error);
      toast.error("Could not remove this project. Please try again.");
    }
  }

  return (
    <Container>
      <SectionHeader
        title="Projects"
        subtitle="The generator ranks your projects against each job and picks the best matches."
      />

      <Card
        title="Add project"
        footer={
          <>
            <Toggle
              checked={form.featured}
              onChange={(e)=>
                setForm({
                  ...form,
                  featured:e.target.checked
                })
              }
            >
              Featured project
            </Toggle>

            <span style={{ flex: 1 }} />

            <Button
              icon={<Plus size={16} />}
              loading={saving}
              onClick={save}
            >
              Add project
            </Button>
          </>
        }
      >
        <div className="form-grid">
          <Field label="Title" required wide>
            <Input
              value={form.title}
              onChange={(e)=>
                setForm({...form,title:e.target.value})
              }
            />
          </Field>

          <Field label="GitHub" required hint="Starts with https://github.com/">
            <Input
              type="url"
              value={form.github}
              onChange={(e)=>
                setForm({...form,github:e.target.value})
              }
            />
          </Field>

          <Field label="Live demo" hint="Optional">
            <Input
              type="url"
              value={form.live_demo}
              onChange={(e)=>
                setForm({...form,live_demo:e.target.value})
              }
            />
          </Field>

          <Field
            label="Technologies"
            required
            wide
            hint="Separate with commas"
          >
            <Input
              value={form.technologies}
              onChange={(e)=>
                setForm({...form,technologies:e.target.value})
              }
            />
          </Field>

          <Field label="Highlights" required wide hint="One highlight per line">
            <TextArea
              rows={5}
              placeholder="One highlight per line"
              value={form.highlights}
              onChange={(e)=>
                setForm({
                  ...form,
                  highlights:e.target.value
                })
              }
            />
          </Field>

          <Field
            label="Keywords"
            required
            wide
            hint="Used to match this project to job descriptions"
          >
            <Input
              placeholder="Python, FastAPI, AI"
              value={form.keywords}
              onChange={(e)=>
                setForm({
                  ...form,
                  keywords:e.target.value
                })
              }
            />
          </Field>
        </div>
      </Card>

      <Card
        title="Your projects"
        action={projects.length > 0 ? <Chip>{projects.length}</Chip> : undefined}
      >
        {projects.length === 0 ? (
          <EmptyState
            icon={<Folder size={20} />}
            title="No projects added yet"
            text="Add your first project above. Two or three strong projects is a good start."
          />
        ) : (
          <div className="item-grid">
            {projects.map((project,index)=>{
              const tech = toList(project.technologies);
              const highlights = toList(project.highlights, /\n+/);

              return (
                <article className="item" key={index}>
                  <div className="item__top">
                    <div>
                      <h3 className="item__title">{project.title}</h3>

                      {project.featured && (
                        <div style={{ marginTop: 6 }}>
                          <span className="badge badge--accent">Featured</span>
                        </div>
                      )}

                      {project.description && (
                        <p className="item__sub">{project.description}</p>
                      )}
                    </div>

                    <DeleteButton onConfirm={()=>remove(index)} />
                  </div>

                  {highlights.length > 0 && (
                    <ul className="item__list">
                      {highlights.slice(0, 2).map((line, i) => (
                        <li key={i}>{line}</li>
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

                  {(project.github || project.live_demo) && (
                    <div className="item__links">
                      {project.github && (
                        <a href={project.github} target="_blank" rel="noreferrer">
                          <LinkIcon size={14} />
                          Source code
                        </a>
                      )}

                      {project.live_demo && (
                        <a href={project.live_demo} target="_blank" rel="noreferrer">
                          <ExternalLink size={14} />
                          Live demo
                        </a>
                      )}
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
