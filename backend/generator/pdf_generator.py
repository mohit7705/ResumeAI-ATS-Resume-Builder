from pathlib import Path

from playwright.sync_api import sync_playwright


OUTPUT_DIR = Path("generated/pdf")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGE_MARGIN_MM = 9
USABLE_HEIGHT_PX = int((297 - 2 * PAGE_MARGIN_MM) * 96 / 25.4) - 4
USABLE_WIDTH_PX = int((210 - 2 * PAGE_MARGIN_MM) * 96 / 25.4)

MIN_ZOOM = 0.80
MAX_ZOOM = 1.32
ZOOM_STEP = 0.02
FILL_TARGET = 0.985
DROP_ORDER = []

_H = "() => document.querySelector('.container').scrollHeight"
_ZOOM = """(z) => {
    const c = document.querySelector('.container');
    c.style.zoom = z;
    return c.scrollHeight;
}"""
_ZOOM_JS = _ZOOM
_DROP_JS = "(name) => false"
_REVEAL = """() => {
    const li = document.querySelector('[data-extra][hidden]');
    if (!li) return false;
    li.hidden = false;
    return true;
}"""
_HIDE_LAST = """() => {
    const items = [...document.querySelectorAll('[data-extra]:not([hidden])')];
    if (!items.length) return false;
    items[items.length - 1].hidden = true;
    return true;
}"""
_GAP = """(px) => {
    document.querySelectorAll('.section').forEach((section, index) => {
        if (index) section.style.marginTop = px + 'px';
    });
    return document.querySelector('.container').scrollHeight;
}"""


_DROP_LAST_PROJECT = """() => { const p = [...document.querySelectorAll('.project')];
  if (p.length <= 1) return false; p[p.length-1].remove(); return true; }"""


def fit_to_one_page(page) -> dict:
    limit = USABLE_HEIGHT_PX - 6
    page.evaluate(_ZOOM, 1.0)
    height = page.evaluate(_H)

    while height < limit * FILL_TARGET and page.evaluate(_REVEAL):
        height = page.evaluate(_H)
        if height > limit:
            page.evaluate(_HIDE_LAST)
            height = page.evaluate(_H)
            break

    lo, hi, best = MIN_ZOOM, MAX_ZOOM, MIN_ZOOM
    for _ in range(10):
        mid = round((lo + hi) / 2, 3)
        if page.evaluate(_ZOOM, mid) <= limit:
            best, lo = mid, mid
        else:
            hi = mid
    height = page.evaluate(_ZOOM, best)

    sections = page.evaluate(
        "() => document.querySelectorAll('.section').length"
    )
    leftover = limit - height
    if leftover > 0 and sections > 1:
        base = 8
        extra = min(leftover / (sections - 1), 24)
        height = page.evaluate(_GAP, base + extra)
        if height > limit:
            height = page.evaluate(_GAP, base)

    return {
        "zoom": best,
        "height_px": height,
        "fits": height <= limit,
        "dropped_sections": [],
    }


def count_pdf_pages(pdf_file: Path) -> int:
    from pypdf import PdfReader

    return len(PdfReader(str(pdf_file)).pages)


def _validate_names(html_file: Path, output_name: str) -> Path:
    html_file = Path(html_file).resolve()
    if not html_file.is_file():
        raise FileNotFoundError(f"Resume HTML file not found: {html_file}")
    if Path(output_name).name != output_name:
        raise ValueError("output_name must be a filename, not a path")
    if not output_name.lower().endswith(".pdf"):
        raise ValueError("output_name must end with .pdf")
    return html_file


def _render_pdf(browser, html_file: Path, pdf_file: Path) -> None:
    page = browser.new_page(
        viewport={"width": USABLE_WIDTH_PX, "height": 1123},
        device_scale_factor=1,
    )
    try:
        page.goto(html_file.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.evaluate(
            """async () => {
                if (document.fonts) { await document.fonts.ready; }
                await Promise.all(Array.from(document.images).map((img) =>
                    img.complete ? Promise.resolve()
                    : new Promise((resolve) => {
                        img.addEventListener("load", resolve, { once: true });
                        img.addEventListener("error", resolve, { once: true });
                    })));
            }"""
        )
        fit = fit_to_one_page(page)
        zoom = fit["zoom"]

        # Never fail: if the PDF is still 2 pages, remove filler first,
        # then shrink step by step, then drop the last project.
        for _ in range(60):
            page.pdf(
                path=str(pdf_file),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=False,
                margin={
                    "top": f"{PAGE_MARGIN_MM}mm",
                    "bottom": f"{PAGE_MARGIN_MM}mm",
                    "left": f"{PAGE_MARGIN_MM}mm",
                    "right": f"{PAGE_MARGIN_MM}mm",
                },
            )
            if count_pdf_pages(pdf_file) == 1:
                return
            if page.evaluate(_HIDE_LAST):
                continue
            if zoom - 0.03 >= 0.55:
                zoom = round(zoom - 0.03, 3)
                page.evaluate(_ZOOM, zoom)
                continue
            if page.evaluate(_DROP_LAST_PROJECT):
                continue
            break
    finally:
        page.close()

    raise ValueError(
        "Resume is still more than 1 page after auto-fit. "
        "Shorten the summary, project bullets or experience text."
    )


def generate_pdfs(jobs: list[tuple]) -> list[Path]:
    checked = [
        (_validate_names(html_file, output_name), OUTPUT_DIR / output_name)
        for html_file, output_name in jobs
    ]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for html_file, pdf_file in checked:
                _render_pdf(browser, html_file, pdf_file)
        finally:
            browser.close()
    return [pdf_file for _, pdf_file in checked]


def generate_pdf(html_file: Path, output_name: str = "resume.pdf"):
    return generate_pdfs([(html_file, output_name)])[0]
