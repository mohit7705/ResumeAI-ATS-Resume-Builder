from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/projects", tags=["Projects"])

FILE = Path("data/projects/projects.json")


@router.get("/")
def get_projects():
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text("[]")

    with open(FILE, "r") as f:
        return json.load(f)


@router.post("/")
def add_project(data: dict):
    with open(FILE, "r") as f:
        projects = json.load(f)

    projects.append(data)

    with open(FILE, "w") as f:
        json.dump(projects, f, indent=4)

    return {"message": "Project Added"}


@router.put("/{index}")
def update_project(index: int, data: dict):
    with open(FILE, "r") as f:
        projects = json.load(f)

    projects[index] = data

    with open(FILE, "w") as f:
        json.dump(projects, f, indent=4)

    return {"message": "Project Updated"}


@router.delete("/{index}")
def delete_project(index: int):
    with open(FILE, "r") as f:
        projects = json.load(f)

    projects.pop(index)

    with open(FILE, "w") as f:
        json.dump(projects, f, indent=4)

    return {"message": "Project Deleted"}