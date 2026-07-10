from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/personal", tags=["Personal"])

PROFILE = Path("data/personal/profile.json")


@router.get("/")
def get_profile():
    with open(PROFILE, "r") as f:
        return json.load(f)


@router.put("/")
def update_profile(data: dict):
    with open(PROFILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"message": "Profile Updated"}