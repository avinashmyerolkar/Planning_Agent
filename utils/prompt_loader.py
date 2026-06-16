import yaml
from pathlib import Path
from typing import Dict

_PROMPT_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(name: str) -> Dict:
    path = _PROMPT_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)