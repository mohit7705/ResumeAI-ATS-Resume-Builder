import { useEffect, useState } from "react";

import Container from "../../components/ui/Container";
import SectionHeader from "../../components/ui/SectionHeader";
import Card from "../../components/ui/Card";
import Label from "../../components/ui/Label";
import Input from "../../components/ui/Input";
import TextArea from "../../components/ui/TextArea";
import Button from "../../components/ui/Button";

import {
  getProjects,
  addProject,
  deleteProject,
} from "../../services/projects";

export default function ProjectsModule() {
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

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setProjects(await getProjects());
  }

 async function save() {

  if (!form.title.trim()) {
    alert("Project title is required.");
    return;
  }

  if (!form.github.trim()) {
    alert("GitHub URL is required.");
    return;
  }

  if (
    !form.github.startsWith("https://github.com/")
  ) {
    alert("Enter a valid GitHub URL.");
    return;
  }

  if (
    form.live_demo &&
    !/^https?:\/\/.+/.test(form.live_demo)
  ) {
    alert("Enter a valid Live Demo URL.");
    return;
  }

  if (!form.technologies.trim()) {
    alert("Technologies are required.");
    return;
  }

  if (!form.highlights.trim()) {
    alert("Project highlights are required.");
    return;
  }

  if (!form.keywords.trim()) {
    alert("Project keywords are required.");
    return;
  }

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

  alert("Project Added Successfully.");

 }

  async function remove(index: number) {
    await deleteProject(index);
    load();
  }

  return (
    <Container>
      <SectionHeader
        title="Projects"
        subtitle="Manage Projects"
      />

      <Card title="Add Project">

        <Label>Title</Label>
        <Input
          value={form.title}
          onChange={(e)=>
            setForm({...form,title:e.target.value})
          }
        />

        <Label>GitHub</Label>
        <Input
          value={form.github}
          onChange={(e)=>
            setForm({...form,github:e.target.value})
          }
        />

        <Label>Live Demo</Label>
        <Input
          value={form.live_demo}
          onChange={(e)=>
            setForm({...form,live_demo:e.target.value})
          }
        />

        <Label>Technologies</Label>
        <Input
          value={form.technologies}
          onChange={(e)=>
            setForm({...form,technologies:e.target.value})
          }
        />

        <Label>Highlights</Label>
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

        <Label>Keywords</Label>
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

        <div
          style={{
            display:"flex",
            alignItems:"center",
            gap:10,
            marginTop:15
          }}
        >
          <input
            type="checkbox"
            checked={form.featured}
            onChange={(e)=>
              setForm({
                ...form,
                featured:e.target.checked
              })
            }
          />

          <Label>Featured Project</Label>
        </div>

        <Button onClick={save}>
          Add Project
        </Button>

      </Card>

      <Card title="Project List">

        {projects.map((project,index)=>(
          <div
            key={index}
            style={{
              border:"1px solid #333",
              padding:15,
              marginBottom:15,
              borderRadius:8
            }}
          >
            <h3>{project.title}</h3>

            <p>{project.description}</p>

            <Button
              style={{background:"#dc2626"}}
              onClick={()=>remove(index)}
            >
              Delete
            </Button>
          </div>
        ))}

      </Card>

    </Container>
  );
}