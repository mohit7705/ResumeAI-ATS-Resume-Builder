from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/certifications", tags=["Certifications"])

FILE = Path("data/personal/certifications.json")


@router.get("/")
def get_certifications():
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text("[]")

    with open(FILE, "r") as f:
        return json.load(f)


@router.post("/")
def add_certification(data: dict):
    with open(FILE, "r") as f:
        items = json.load(f)

    items.append(data)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Certification Added"}


@router.delete("/{index}")
def delete_certification(index: int):
    with open(FILE, "r") as f:
        items = json.load(f)

    items.pop(index)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

    return {"message": "Certification Deleted"}