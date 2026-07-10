from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

FILE = Path("data/personal/summary.json")


@router.get("/")
def get_summary():
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text(
            json.dumps(
                {
                    "summary": ""
                },
                indent=4
            )
        )

    with open(FILE, "r") as f:
        return json.load(f)


@router.put("/")
def save_summary(data: dict):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Summary Updated"
    }