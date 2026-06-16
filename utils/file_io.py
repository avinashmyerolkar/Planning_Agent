from pathlib import Path

_OUTPUT_DIR = Path(__file__).parent.parent / "outputs"


def save_markdown(title: str, content: str) -> Path:
    _OUTPUT_DIR.mkdir(exist_ok=True)
    filename = title.lower().replace(" ", "_").replace("/", "-") + ".md"
    path = _OUTPUT_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path