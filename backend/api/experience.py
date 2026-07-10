from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/experience", tags=["Experience"])

FILE = Path("data/personal/experience.json")


@router.get("/")
def get_experience():
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text("[]")

    with open(FILE, "r") as f:
        return json.load(f)


@router.post("/")
def add_experience(data: dict):
    with open(FILE, "r") as f:
        items = json.load(f)

    items.append(data)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Experience Added"}


@router.put("/{index}")
def update_experience(index: int, data: dict):
    with open(FILE, "r") as f:
        items = json.load(f)

    items[index] = data

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Experience Updated"}


@router.delete("/{index}")
def delete_experience(index: int):
    with open(FILE, "r") as f:
        items = json.load(f)

    items.pop(index)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Experience Deleted"}