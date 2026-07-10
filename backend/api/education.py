from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/education", tags=["Education"])

FILE = Path("data/personal/education.json")


@router.get("/")
def get_education():
    with open(FILE, "r") as f:
        return json.load(f)


@router.post("/")
def add_education(data: dict):
    with open(FILE, "r") as f:
        education = json.load(f)

    education.append(data)

    with open(FILE, "w") as f:
        json.dump(education, f, indent=4)

    return {"message": "Education Added"}


@router.put("/{index}")
def update_education(index: int, data: dict):
    with open(FILE, "r") as f:
        education = json.load(f)

    education[index] = data

    with open(FILE, "w") as f:
        json.dump(education, f, indent=4)

    return {"message": "Education Updated"}


@router.delete("/{index}")
def delete_education(index: int):
    with open(FILE, "r") as f:
        education = json.load(f)

    education.pop(index)

    with open(FILE, "w") as f:
        json.dump(education, f, indent=4)

    return {"message": "Education Deleted"}