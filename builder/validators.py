"""Validation helpers for prompt content and site configuration."""

from __future__ import annotations


REQUIRED_PROMPT_FIELDS = {
    "number",
    "name",
    "slug",
    "mode",
    "font",
    "description",
    "prompt",
    "category_key",
}

ALLOWED_MODES = {"dark", "light"}
ALLOWED_FONTS = {"serif", "sans-serif", "mono"}


def validate_site_config(config: dict) -> None:
    required_fields = {
        "site_name",
        "site_url",
        "author",
        "keywords",
        "locales",
    }
    missing = sorted(required_fields - set(config))
    if missing:
        raise ValueError(f"site config is missing required fields: {', '.join(missing)}")
    for locale_code in ("en", "zh"):
        if locale_code not in config["locales"]:
            raise ValueError(f"site config is missing locale '{locale_code}'")


def validate_prompts(prompts: list[dict]) -> None:
    if not prompts:
        raise ValueError("no prompts were found in content/prompts/")

    seen_numbers: set[int] = set()
    seen_slugs: set[str] = set()

    for prompt in prompts:
        missing = sorted(REQUIRED_PROMPT_FIELDS - set(prompt))
        if missing:
            slug = prompt.get("slug", "<unknown>")
            raise ValueError(f"prompt '{slug}' is missing required fields: {', '.join(missing)}")

        if prompt["mode"] not in ALLOWED_MODES:
            raise ValueError(f"prompt '{prompt['slug']}' has invalid mode '{prompt['mode']}'")
        if prompt["font"] not in ALLOWED_FONTS:
            raise ValueError(f"prompt '{prompt['slug']}' has invalid font '{prompt['font']}'")
        if not isinstance(prompt["number"], int):
            raise ValueError(f"prompt '{prompt['slug']}' number must be an integer")
        if prompt["number"] in seen_numbers:
            raise ValueError(f"duplicate prompt number found: {prompt['number']}")
        if prompt["slug"] in seen_slugs:
            raise ValueError(f"duplicate prompt slug found: {prompt['slug']}")
        if not str(prompt["name"]).strip():
            raise ValueError(f"prompt '{prompt['slug']}' has an empty name")
        if not str(prompt["description"]).strip():
            raise ValueError(f"prompt '{prompt['slug']}' has an empty description")
        if not str(prompt["prompt"]).strip():
            raise ValueError(f"prompt '{prompt['slug']}' has an empty prompt body")

        seen_numbers.add(prompt["number"])
        seen_slugs.add(prompt["slug"])
