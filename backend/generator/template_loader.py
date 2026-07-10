from pathlib import Path


TEMPLATE_DIR = Path("templates/html")


def load_template(template_name: str = "ats_one_page.html") -> str:
    template_path = TEMPLATE_DIR / template_name

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    return template_path.read_text(encoding="utf-8")