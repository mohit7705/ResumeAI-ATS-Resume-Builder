from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/skills", tags=["Skills"])

FILE = Path("data/personal/skills.json")


@router.get("/")
def get_skills():
    with open(FILE, "r") as f:
        return json.load(f)


@router.put("/")
def save_skills(data: dict):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"message": "Skills Updated"}