from pathlib import Path


def ensure_directory(path: str | Path):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_files(folder: str | Path, extension: str):
    folder = Path(folder)

    if not folder.exists():
        return []

    return sorted(folder.glob(f"*.{extension}"))