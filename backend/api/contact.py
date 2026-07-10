from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/contact", tags=["Contact"])

FILE = Path("data/personal/contact.json")


@router.get("/")
def get_contact():
    with open(FILE, "r") as f:
        return json.load(f)


@router.put("/")
def update_contact(data: dict):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"message": "Contact Updated"}