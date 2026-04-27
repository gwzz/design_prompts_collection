"""Load prompt content and site configuration from disk."""

from __future__ import annotations

import json
import re

from .paths import FEATURED_STATS_FILE, PROMPTS_CONTENT_DIR, SITE_CONFIG_FILE
from .themes import category_for_slug


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_site_config() -> dict:
    return _read_json(SITE_CONFIG_FILE)


def load_featured_stats() -> dict:
    if not FEATURED_STATS_FILE.exists():
        return {}
    return _read_json(FEATURED_STATS_FILE)


def _extract_lead(prompt_text: str) -> str:
    parts = prompt_text.split("\n\n--- Layout by Section ---", 1)
    intro_block = parts[0]
    lines = [line.strip() for line in intro_block.splitlines() if line.strip()]
    if len(lines) >= 3:
        return lines[2]
    return ""


def _extract_sections(prompt_text: str) -> list[str]:
    return re.findall(r"^\[(.+?)\]\s*$", prompt_text, flags=re.MULTILINE)


def _derive_keywords(lead: str) -> list[str]:
    normalized = lead.replace(".", ",")
    chunks = [chunk.strip() for chunk in normalized.split(",") if chunk.strip()]
    return chunks[:3]


def load_prompts() -> list[dict]:
    prompts = []
    for prompt_file in sorted(PROMPTS_CONTENT_DIR.glob("*/prompt.json")):
        if prompt_file.parent.name.startswith("_"):
            continue
        prompt = _read_json(prompt_file)
        prompt["category_key"] = category_for_slug(prompt["slug"])
        prompt["lead"] = _extract_lead(prompt["prompt"])
        prompt["layout_sections"] = _extract_sections(prompt["prompt"])
        prompt["keywords"] = _derive_keywords(prompt["lead"])
        prompts.append(prompt)
    return sorted(prompts, key=lambda item: item["number"])
