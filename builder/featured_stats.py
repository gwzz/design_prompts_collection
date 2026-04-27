"""Helpers for mock featured-prompt engagement stats."""

from __future__ import annotations


DEFAULT_WEIGHTS = {"click": 1, "like": 5}


def _to_int(value: object, default: int = 0) -> int:
    try:
        return max(int(value), 0)
    except (TypeError, ValueError):
        return default


def build_featured_stats_seed(prompts: list[dict], raw_stats: dict | None) -> dict:
    raw_stats = raw_stats or {}
    raw_weights = raw_stats.get("weights", {})
    weights = {
        "click": _to_int(raw_weights.get("click"), DEFAULT_WEIGHTS["click"]),
        "like": _to_int(raw_weights.get("like"), DEFAULT_WEIGHTS["like"]),
    }
    prompt_stats = raw_stats.get("prompts", {})
    stats_by_slug = {}

    for prompt in prompts:
        slug = prompt["slug"]
        seeded = prompt_stats.get(slug, {})
        click_count = _to_int(seeded.get("click_count"))
        like_count = _to_int(seeded.get("like_count"))
        score = click_count * weights["click"] + like_count * weights["like"]
        stats_by_slug[slug] = {
            "click_count": click_count,
            "like_count": like_count,
            "score": score,
        }

    return {
        "weights": weights,
        "prompts": stats_by_slug,
    }


def ranked_featured_prompts(prompts: list[dict], stats_seed: dict, fallback_slugs: list[str], limit: int = 3) -> list[dict]:
    stats_by_slug = stats_seed["prompts"]
    fallback_rank = {slug: index for index, slug in enumerate(fallback_slugs)}

    def sort_key(prompt: dict) -> tuple[int, int, int, int, int]:
        stats = stats_by_slug.get(prompt["slug"], {"score": 0, "like_count": 0, "click_count": 0})
        return (
            -stats["score"],
            -stats["like_count"],
            -stats["click_count"],
            fallback_rank.get(prompt["slug"], 999),
            prompt["number"],
        )

    return sorted(prompts, key=sort_key)[:limit]
