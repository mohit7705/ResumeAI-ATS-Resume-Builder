from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/achievements", tags=["Achievements"])

FILE = Path("data/personal/achievements.json")


@router.get("/")
def get_achievements():
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text("[]")

    with open(FILE, "r") as f:
        return json.load(f)


@router.post("/")
def add_achievement(data: dict):
    with open(FILE, "r") as f:
        items = json.load(f)

    items.append(data)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Achievement Added"}


@router.delete("/{index}")
def delete_achievement(index: int):
    with open(FILE, "r") as f:
        items = json.load(f)

    items.pop(index)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Achievement Deleted"}