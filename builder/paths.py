"""Filesystem paths used by the static site builder."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT_DIR / "content"
PROMPTS_CONTENT_DIR = CONTENT_DIR / "prompts"
SITE_CONFIG_FILE = CONTENT_DIR / "site.json"

SITE_DIR = ROOT_DIR / "site"
SITE_PROMPTS_DIR = SITE_DIR / "prompts"
SITE_ASSETS_DIR = SITE_DIR / "assets"
