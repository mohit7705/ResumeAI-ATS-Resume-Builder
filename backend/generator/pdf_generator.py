from pathlib import Path

from playwright.sync_api import sync_playwright


OUTPUT_DIR = Path("generated/pdf")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_pdf(html_file: Path):
    pdf_file = OUTPUT_DIR / "resume.pdf"

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()

        page.goto(
            html_file.resolve().as_uri(),
            wait_until="networkidle"
        )

        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            margin={
                "top": "10mm",
                "bottom": "10mm",
                "left": "10mm",
                "right": "10mm",
            },
        )

        browser.close()

    return pdf_file