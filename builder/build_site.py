#!/usr/bin/env python3
"""Build the Design Prompts Collection static site."""

from __future__ import annotations

import shutil

from .assets import ASSET_FILES
from .content_loader import load_prompts, load_site_config
from .paths import SITE_ASSETS_DIR, SITE_DIR
from .renderers import generate_detail_page, generate_index_page, generate_robots, generate_root_router, generate_sitemap
from .validators import validate_prompts, validate_site_config


def write_file(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build() -> None:
    config = load_site_config()
    prompts = load_prompts()
    validate_site_config(config)
    validate_prompts(prompts)

    for stale_dir in (SITE_DIR / "en", SITE_DIR / "zh", SITE_DIR / "prompts"):
        if stale_dir.exists():
            shutil.rmtree(stale_dir)

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    SITE_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, content in ASSET_FILES.items():
        write_file(SITE_ASSETS_DIR / filename, content)

    write_file(SITE_DIR / "index.html", generate_root_router(config))
    write_file(SITE_DIR / "robots.txt", generate_robots(config))
    write_file(SITE_DIR / "sitemap.xml", generate_sitemap(prompts, config))

    for locale_code in ("en", "zh"):
        write_file(SITE_DIR / locale_code / "index.html", generate_index_page(prompts, config, locale_code))
        for prompt in prompts:
            write_file(
                SITE_DIR / locale_code / "prompts" / f"{prompt['slug']}.html",
                generate_detail_page(prompt, config, locale_code),
            )

    print(f"Built {len(prompts)} prompt pages for {len(config['locales'])} locales into {SITE_DIR.name}")


if __name__ == "__main__":
    build()
