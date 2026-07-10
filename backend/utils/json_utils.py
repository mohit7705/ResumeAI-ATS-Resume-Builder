import json
from pathlib import Path


def load_json(file_path: str | Path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, file_path: str | Path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)