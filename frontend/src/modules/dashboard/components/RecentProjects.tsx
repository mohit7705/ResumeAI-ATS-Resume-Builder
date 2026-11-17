import { useEffect, useState } from "react";
import { Folder } from "lucide-react";

import Card from "../../../components/ui/Card";
import Button from "../../../components/ui/Button";
import Chip from "../../../components/ui/Chip";
import EmptyState from "../../../components/ui/EmptyState";
import { useApp } from "../../../context/AppContext";
import { getProjects } from "../../../services/projects";
import { toList } from "../../../utils/format";

export default function RecentProjects() {
  const { setPage } = useApp();
  const [projects, setProjects] = useState<any[]>([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const data = await getProjects();
      setProjects(data.slice(0, 3));
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <Card
      title="Recent projects"
      action={
        projects.length > 0 ? (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setPage("projects")}
          >
            View all
          </Button>
        ) : undefined
      }
    >
      {projects.length === 0 ? (
        <EmptyState
          icon={<Folder size={20} />}
          title="No projects yet"
          text="Projects are the strongest evidence on a fresher resume."
          action={
            <Button size="sm" onClick={() => setPage("projects")}>
              Add a project
            </Button>
          }
        />
      ) : (
        <ul className="recent">
          {projects.map((project, index) => (
            <li key={index}>
              <span className="recent__title">{project.title}</span>

              <span className="chips">
                {toList(project.technologies)
                  .slice(0, 2)
                  .map((tech) => (
                    <Chip key={tech} small>
                      {tech}
                    </Chip>
                  ))}
              </span>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
