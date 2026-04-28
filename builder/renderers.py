"""HTML and text renderers for the generated site."""

from __future__ import annotations

import json
from html import escape

from .featured_stats import ranked_featured_prompts
from .themes import get_theme


def summarize_description(text: str, max_length: int = 96) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 3].rstrip() + "..."


def localized_category(prompt: dict, locale_config: dict) -> str:
    return locale_config["category_labels"].get(prompt["category_key"], locale_config["category_labels"]["other"])


def localized_use_case(prompt: dict, locale_config: dict) -> str:
    return locale_config["use_cases"].get(prompt["category_key"], locale_config["use_cases"]["other"])


def locale_path(locale: str, slug: str | None = None) -> str:
    return f"/{locale}/prompts/{slug}.html" if slug else f"/{locale}/index.html"


def relative_locale_href(current_locale: str | None, target_locale: str, slug: str | None = None, *, current_slug: str | None = None) -> str:
    if current_locale is None:
        return f"./{target_locale}/prompts/{slug}.html" if slug else f"./{target_locale}/index.html"
    if current_slug is None:
        return f"../{target_locale}/prompts/{slug}.html" if slug else f"../{target_locale}/index.html"
    return f"../../{target_locale}/prompts/{slug}.html" if slug else f"../index.html"


def relative_asset_href(current_slug: str | None = None, *, filename: str) -> str:
    prefix = "../../assets" if current_slug is not None else "../assets"
    return f"{prefix}/{filename}"


def absolute_locale_url(site_url: str, locale: str, slug: str | None = None) -> str:
    return site_url.rstrip("/") + locale_path(locale, slug)


def json_script_tag(element_id: str, payload: object) -> str:
    json_text = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    return f'<script id="{element_id}" type="application/json">{json_text}</script>'


def language_switcher(current_locale: str, slug: str | None, ui: dict) -> str:
    items = []
    for locale_code in ("en", "zh"):
        active = " active" if locale_code == current_locale else ""
        href = relative_locale_href(current_locale, locale_code, slug, current_slug=slug)
        label = ui["language"][locale_code]
        items.append(
            f'<a class="lang-link{active}" href="{href}" data-locale-link data-locale="{locale_code}">{escape(label)}</a>'
        )
    return f"""<div class="lang-switcher" aria-label="{escape(ui['language']['label'])}">
  {"".join(items)}
</div>"""


def theme_switcher(ui: dict) -> str:
    labels = ui.get("theme", {})
    light_label = labels.get("light", "Light")
    dark_label = labels.get("dark", "Dark")
    aria_label = labels.get("label", "Theme")
    return f"""<div class="theme-switcher" aria-label="{escape(aria_label)}">
  <button class="theme-option" type="button" data-theme-option="light">{escape(light_label)}</button>
  <button class="theme-option" type="button" data-theme-option="dark">{escape(dark_label)}</button>
</div>"""


def base_head(
    site_config: dict,
    locale_code: str,
    locale_config: dict,
    *,
    title: str,
    description: str,
    canonical: str,
    stylesheet_path: str,
    favicon_path: str,
    og_title: str | None = None,
    slug: str | None = None,
) -> str:
    og_title = og_title or title
    site_name = escape(site_config["site_name"])
    desc = escape(description)
    canonical_url = escape(canonical)
    og_image = escape(f"{site_config['site_url'].rstrip('/')}/assets/og-cover.svg")
    keywords = escape(", ".join(site_config["keywords"]))
    alternates = []
    for alternate_locale in ("en", "zh"):
        href = absolute_locale_url(site_config["site_url"], alternate_locale, slug)
        hreflang = "en" if alternate_locale == "en" else "zh-CN"
        alternates.append(f'<link rel="alternate" hreflang="{hreflang}" href="{escape(href)}">')
    alternates.append(f'<link rel="alternate" hreflang="x-default" href="{escape(absolute_locale_url(site_config["site_url"], "en", slug))}">')
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="theme-color" content="#fafafa">
<link rel="canonical" href="{canonical_url}">
{''.join(alternates)}
<link rel="icon" href="{escape(favicon_path)}" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{escape(og_title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(og_title)}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<title>{escape(title)}</title>
<script>
  (function() {{
    try {{
      var stored = localStorage.getItem('dpc-theme-v1');
      var theme = stored === 'dark' || stored === 'light' ? stored : 'light';
      document.documentElement.dataset.theme = theme;
    }} catch (error) {{
      document.documentElement.dataset.theme = 'light';
    }}
  }})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Nunito:wght@400;700;900&family=Patrick+Hand&family=Playfair+Display:wght@400;700;900&family=Roboto:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&family=VT323&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{stylesheet_path}">"""


def generate_preview(prompt: dict, locale_ui: dict) -> str:
    theme = get_theme(prompt["slug"])
    dark_mode = prompt["mode"] == "dark"
    border_color = "rgba(255,255,255,0.12)" if dark_mode else "rgba(0,0,0,0.12)"
    soft_border = "rgba(255,255,255,0.08)" if dark_mode else "rgba(0,0,0,0.08)"
    button_radius = "0" if prompt["slug"] in {"neo-brutalism", "swiss", "newsprint"} else "10px"
    headline = escape(prompt["name"])
    preview_ui = locale_ui["preview"]
    return f"""<div class="preview-container" style="background:{theme['hero_bg']};color:{theme['text']};font-family:{theme['font']};">
  <nav style="display:flex;justify-content:space-between;align-items:center;padding:18px 28px;border-bottom:1px solid {border_color};">
    <div style="font-weight:700;color:{theme['accent']};">{headline}</div>
    <div style="display:flex;gap:18px;font-size:0.85rem;opacity:0.78;">
      <span>{escape(preview_ui['nav'][0])}</span><span>{escape(preview_ui['nav'][1])}</span><span>{escape(preview_ui['nav'][2])}</span>
    </div>
  </nav>
  <section style="padding:64px 28px 54px;text-align:center;">
    <div style="display:inline-block;padding:6px 14px;border-radius:999px;border:1px solid {border_color};background:rgba(255,255,255,0.04);font-size:0.74rem;text-transform:uppercase;letter-spacing:0;">{escape(preview_ui['badge'])}</div>
    <h2 class="preview-headline" style="font-size:3.1rem;line-height:1.05;margin:22px 0 14px;">{preview_ui['headline_html']}</h2>
    <p style="max-width:560px;margin:0 auto 24px;font-size:1.02rem;opacity:0.76;">{escape(preview_ui['body'])}</p>
    <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
      <button style="padding:12px 24px;border-radius:{button_radius};border:1px solid {theme['accent']};background:{theme['accent']};color:#fff;font-weight:600;">{escape(preview_ui['primary_button'])}</button>
      <button style="padding:12px 24px;border-radius:{button_radius};border:1px solid {border_color};background:transparent;color:{theme['text']};font-weight:600;">{escape(preview_ui['secondary_button'])}</button>
    </div>
  </section>
  <section class="preview-stats" style="display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid {border_color};border-bottom:1px solid {border_color};">
    <div style="padding:22px;text-align:center;"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">10K+</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0;">{escape(preview_ui['stats'][0])}</div></div>
    <div style="padding:22px;text-align:center;border-left:1px solid {border_color};"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">99.9%</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0;">{escape(preview_ui['stats'][1])}</div></div>
    <div style="padding:22px;text-align:center;border-left:1px solid {border_color};"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">50+</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0;">{escape(preview_ui['stats'][2])}</div></div>
    <div style="padding:22px;text-align:center;border-left:1px solid {border_color};"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">24/7</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0;">{escape(preview_ui['stats'][3])}</div></div>
  </section>
  <section style="padding:42px 28px;">
    <h3 style="margin:0 0 18px;text-align:center;font-size:1.7rem;">{escape(preview_ui['features_title'])}</h3>
    <div class="preview-features-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;">
      <article style="padding:24px;border-radius:14px;background:{theme['card_bg']};border:1px solid {soft_border};"><div style="font-size:1.8rem;margin-bottom:12px;">A</div><strong>{escape(preview_ui['feature_cards'][0]['title'])}</strong><p style="margin:8px 0 0;opacity:0.75;font-size:0.9rem;">{escape(preview_ui['feature_cards'][0]['body'])}</p></article>
      <article style="padding:24px;border-radius:14px;background:{theme['card_bg']};border:1px solid {soft_border};"><div style="font-size:1.8rem;margin-bottom:12px;">B</div><strong>{escape(preview_ui['feature_cards'][1]['title'])}</strong><p style="margin:8px 0 0;opacity:0.75;font-size:0.9rem;">{escape(preview_ui['feature_cards'][1]['body'])}</p></article>
      <article style="padding:24px;border-radius:14px;background:{theme['card_bg']};border:1px solid {soft_border};"><div style="font-size:1.8rem;margin-bottom:12px;">C</div><strong>{escape(preview_ui['feature_cards'][2]['title'])}</strong><p style="margin:8px 0 0;opacity:0.75;font-size:0.9rem;">{escape(preview_ui['feature_cards'][2]['body'])}</p></article>
    </div>
  </section>
</div>"""


def generate_root_router(site_config: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url=./en/index.html">
  <title>{escape(site_config['site_name'])}</title>
  <script>
    (function() {{
      try {{
        var stored = localStorage.getItem('preferredLocale');
        var preferred = stored || (navigator.languages && navigator.languages[0]) || navigator.language || 'en';
        var locale = /^zh/i.test(preferred) ? 'zh' : 'en';
        window.location.replace('./' + locale + '/index.html');
      }} catch (error) {{
        window.location.replace('./en/index.html');
      }}
    }})();
  </script>
</head>
<body>
  <p>Redirecting... <a href="./en/index.html">English</a> / <a href="./zh/index.html">中文</a></p>
</body>
</html>"""


def generate_index_page(prompts: list[dict], site_config: dict, locale_code: str, featured_stats: dict) -> str:
    locale_config = site_config["locales"][locale_code]
    ui = locale_config["ui"]
    featured_slugs = site_config.get("featured_prompt_slugs", [])
    featured_prompts = ranked_featured_prompts(prompts, featured_stats, featured_slugs, limit=3)
    stats_by_slug = featured_stats["prompts"]
    total_sections = sum(len(prompt["layout_sections"]) for prompt in prompts)
    cards = []
    prompt_index_data = []

    for prompt in prompts:
        theme = get_theme(prompt["slug"])
        category_label = localized_category(prompt, locale_config)
        keyword_badges = "".join(f'<span class="catalog-keyword">{escape(keyword)}</span>' for keyword in prompt["keywords"])
        section_preview = " / ".join(prompt["layout_sections"][:4])
        sections_label = f"{len(prompt['layout_sections'])} {ui['detail']['sections_suffix']}"
        prompt_stats = stats_by_slug[prompt["slug"]]
        prompt_index_data.append(
            {
                "slug": prompt["slug"],
                "number": prompt["number"],
                "name": prompt["name"],
                "note": prompt["lead"] or summarize_description(prompt["description"], 72),
                "href": f"prompts/{prompt['slug']}.html",
                "accent": theme["accent"],
                "category": category_label,
                "click_count": prompt_stats["click_count"],
                "like_count": prompt_stats["like_count"],
                "score": prompt_stats["score"],
            }
        )
        cards.append(
            f"""<a href="prompts/{prompt['slug']}.html" class="catalog-item" data-track-click data-slug="{escape(prompt['slug'])}" data-mode="{escape(prompt['mode'])}" data-font="{escape(prompt['font'])}" data-category="{escape(category_label)}" data-category-search="{escape(category_label.lower())}" data-name="{escape(prompt['name'].lower())}" style="--card-accent:{theme['accent']};">
  <div class="catalog-preview" style="background:{theme['hero_bg']};color:{theme['text']};font-family:{theme['font']};">
    <div class="catalog-preview-mark" style="color:{theme['accent']};">Aa</div>
  </div>
  <div class="catalog-body">
    <div class="catalog-topline">
      <span class="card-number">#{prompt['number']:02d}</span>
      <span class="catalog-category">{escape(category_label)}</span>
    </div>
    <h2 class="catalog-title">{escape(prompt['name'])}</h2>
    <p class="catalog-lead">{escape(prompt['lead'] or summarize_description(prompt['description']))}</p>
    <div class="card-badges">
      <span class="mini-badge mode-{escape(prompt['mode'])}">{escape(prompt['mode'])}</span>
      <span class="mini-badge font-{escape(prompt['font'].replace('-', ''))}">{escape(prompt['font'])}</span>
      <span class="mini-badge catalog-sections">{escape(sections_label)}</span>
    </div>
    <div class="catalog-keywords">{keyword_badges}</div>
    <p class="catalog-sections-line">{escape(section_preview)}</p>
    {stats_markup(prompt["slug"], prompt_stats, ui)}
  </div>
</a>"""
        )

    category_buttons = [f'<button class="cat-btn active" type="button" data-selectable data-filter="category" data-value="all">{escape(ui["filters"]["all_categories"])}</button>']
    for category_key in ("tech", "editorial", "expressive", "tactile"):
        category_label = locale_config["category_labels"][category_key]
        category_buttons.append(f'<button class="cat-btn" type="button" data-selectable data-filter="category" data-value="{escape(category_label)}">{escape(category_label)}</button>')

    featured_markup = []
    for prompt in featured_prompts:
        theme = get_theme(prompt["slug"])
        prompt_stats = stats_by_slug[prompt["slug"]]
        featured_markup.append(
            f"""<a href="prompts/{prompt['slug']}.html" class="featured-link" data-featured-item data-track-click data-slug="{escape(prompt['slug'])}" style="--card-accent:{theme['accent']};">
  <span class="featured-index">#{prompt['number']:02d}</span>
  <span class="featured-name">{escape(prompt['name'])}</span>
  <span class="featured-note">{escape(prompt['lead'] or summarize_description(prompt['description'], 72))}</span>
  <span class="featured-stats">
    <span class="featured-stat"><strong data-stat-click-count>{prompt_stats['click_count']}</strong> {escape(ui['featured']['clicks_label'])}</span>
    <span class="featured-stat"><strong data-stat-like-count>{prompt_stats['like_count']}</strong> {escape(ui['featured']['likes_label'])}</span>
  </span>
</a>"""
        )

    head = base_head(
        site_config,
        locale_code,
        locale_config,
        title=locale_config["site_title"],
        description=locale_config["site_description"],
        canonical=absolute_locale_url(site_config["site_url"], locale_code),
        stylesheet_path=relative_asset_href(filename="styles.css"),
        favicon_path=relative_asset_href(filename="favicon.svg"),
    )

    featured_ui_payload = {
        "clicksLabel": ui["featured"]["clicks_label"],
        "likesLabel": ui["featured"]["likes_label"],
    }
    language_markup = language_switcher(locale_code, None, ui)
    featured_ui_payload = {
        "clicksLabel": ui["featured"]["clicks_label"],
        "likesLabel": ui["featured"]["likes_label"],
        "scoreLabel": ui["featured"]["score_label"],
        "sourceTitle": ui["featured"]["source_title"],
        "sourceBody": ui["featured"]["source_body"],
        "limit": 3,
    }

    return f"""<!DOCTYPE html>
<html lang="{escape(locale_config['lang'])}">
<head>
{head}
</head>
<body data-results-suffix="{escape(ui['results_suffix'])}" data-api-base="../api">
  <div class="page-shell">
    <section class="masthead">
      <div class="masthead-inner">
        <span class="masthead-brand">{escape(site_config["site_name"])}</span>
        <div class="masthead-links">
          <a href="#catalog">{escape(ui['nav']['browse'])}</a>
          <a href="#featured">{escape(ui['nav']['featured'])}</a>
          <a href="#why">{escape(ui['nav']['how_to_use'])}</a>
        </div>
        {language_markup}
      </div>
    </section>
    <section class="hero-section">
      <div class="hero-content poster-shell">
        <div class="hero-copy">
          <div class="hero-badge">{escape(ui["hero_badge"])}</div>
          <h1 class="hero-title">{ui["hero_title_html"]}</h1>
          <p class="hero-subtitle">{escape(locale_config["home_intro"])}</p>
          <div class="hero-actions">
            <a class="hero-action primary" href="#catalog">{escape(ui["hero_cta_primary"])}</a>
            <a class="hero-action" href="#featured">{escape(ui["hero_cta_secondary"])}</a>
          </div>
          <div class="hero-meta">{"".join(f"<span>{escape(item)}</span>" for item in ui["hero_meta"])}</div>
        </div>
        <aside class="hero-panel" id="featured">
          <div class="hero-panel-label">{escape(ui["featured_label"])}</div>
          <p class="hero-panel-copy">{escape(ui['featured']['source_body'])}</p>
          <div id="featuredList">
            {"".join(featured_markup)}
          </div>
        </aside>
      </div>
    </section>

    <section class="quick-stats">
      <div class="quick-stat"><span class="quick-stat-value">{len(prompts)}</span><span class="quick-stat-label">{escape(ui['stats']['styles'])}</span></div>
      <div class="quick-stat"><span class="quick-stat-value">4</span><span class="quick-stat-label">{escape(ui['stats']['categories'])}</span></div>
      <div class="quick-stat"><span class="quick-stat-value">3</span><span class="quick-stat-label">{escape(ui['stats']['font_modes'])}</span></div>
      <div class="quick-stat"><span class="quick-stat-value">{total_sections}</span><span class="quick-stat-label">{escape(ui['stats']['sections'])}</span></div>
    </section>

    <section class="support-section" id="why">
      <div class="support-copy">
        <p class="section-kicker">{escape(ui['support']['kicker'])}</p>
        <h2>{escape(ui['support']['title'])}</h2>
        <p>{escape(ui['support']['body'])}</p>
      </div>
      <div class="support-list">
        <div class="support-item"><span>01</span><p>{escape(ui['support']['items'][0])}</p></div>
        <div class="support-item"><span>02</span><p>{escape(ui['support']['items'][1])}</p></div>
        <div class="support-item"><span>03</span><p>{escape(ui['support']['items'][2])}</p></div>
      </div>
    </section>

    <section class="catalog-shell" id="catalog">
      <div class="catalog-header">
        <div>
          <p class="section-kicker">{escape(ui['catalog']['kicker'])}</p>
          <h2>{escape(ui['catalog']['title'])}</h2>
        </div>
        <p class="catalog-header-copy">{escape(ui['catalog']['body'])}</p>
      </div>

      <div class="controls-section">
        <div class="search-container">
          <input id="searchInput" type="search" placeholder="{escape(ui['search_placeholder'])}">
        </div>

        <div class="filter-panel">
          <div class="filter-row">
            <div class="filter-group" data-filter-group>
              <span class="filter-label">{escape(ui['filters']['mode_label'])}</span>
              <button class="filter-btn active" type="button" data-selectable data-filter="mode" data-value="all">{escape(ui['filters']['mode']['all'])}</button>
              <button class="filter-btn" type="button" data-selectable data-filter="mode" data-value="dark">{escape(ui['filters']['mode']['dark'])}</button>
              <button class="filter-btn" type="button" data-selectable data-filter="mode" data-value="light">{escape(ui['filters']['mode']['light'])}</button>
            </div>

            <div class="filter-group" data-filter-group>
              <span class="filter-label">{escape(ui['filters']['font_label'])}</span>
              <button class="filter-btn active" type="button" data-selectable data-filter="font" data-value="all">{escape(ui['filters']['font']['all'])}</button>
              <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="serif">{escape(ui['filters']['font']['serif'])}</button>
              <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="sans-serif">{escape(ui['filters']['font']['sans-serif'])}</button>
              <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="mono">{escape(ui['filters']['font']['mono'])}</button>
            </div>
          </div>

          <div class="category-row" data-filter-group">
            {"".join(category_buttons)}
          </div>
          <p class="result-summary" id="resultCount">{len(prompts)} {escape(ui['results_suffix'])}</p>
        </div>
      </div>

      <main class="cards-grid" aria-label="{escape(ui['cards_aria_label'])}">
        {"".join(cards)}
      </main>

      <div class="no-results" id="noResults" hidden>
        <p>{escape(ui['no_results'])}</p>
      </div>
    </section>

    <footer class="site-footer">
      <div class="footer-branding">
        <p class="footer-title">{escape(site_config['site_name'])}</p>
        <p class="footer-hint">{escape(ui['footer_hint'])}</p>
      </div>
      <div class="footer-meta">
        <section class="footer-card">
          <h3>{escape(ui['footer']['privacy_title'])}</h3>
          <p>{escape(ui['footer']['privacy_body'])}</p>
        </section>
        <section class="footer-card">
          <h3>{escape(ui['footer']['contact_title'])}</h3>
          <p>{escape(ui['footer']['contact_body'])}</p>
        </section>
      </div>
    </footer>
  </div>
  {json_script_tag("prompt-index-data", prompt_index_data)}
  {json_script_tag("featured-stats-data", featured_stats)}
  {json_script_tag("featured-ui-data", featured_ui_payload)}
  <script src="{relative_asset_href(filename='app.js')}" defer></script>
</body>
</html>"""


def generate_detail_page(prompt: dict, site_config: dict, locale_code: str, featured_stats: dict) -> str:
    locale_config = site_config["locales"][locale_code]
    ui = locale_config["ui"]
    category_label = localized_category(prompt, locale_config)
    use_case = localized_use_case(prompt, locale_config)
    prompt_stats = featured_stats["prompts"][prompt["slug"]]

    mode_badge_bg = "#1e293b" if prompt["mode"] == "dark" else "#f1f5f9"
    mode_badge_color = "#cbd5e1" if prompt["mode"] == "dark" else "#334155"
    font_colors = {"serif": ("#fef3c7", "#92400e"), "sans-serif": ("#dbeafe", "#1d4ed8"), "mono": ("#d1fae5", "#047857")}
    font_bg, font_color = font_colors.get(prompt["font"], ("#e5e7eb", "#374151"))

    title = f"{prompt['name']} | {site_config['site_name']}"
    description = summarize_description(prompt["description"], 150)
    canonical = absolute_locale_url(site_config["site_url"], locale_code, prompt["slug"])
    head = base_head(
        site_config,
        locale_code,
        locale_config,
        title=title,
        description=description,
        canonical=canonical,
        stylesheet_path=relative_asset_href(prompt["slug"], filename="styles.css"),
        favicon_path=relative_asset_href(prompt["slug"], filename="favicon.svg"),
        og_title=prompt["name"],
        slug=prompt["slug"],
    )

    sections_label = f"{len(prompt['layout_sections'])} {ui['detail']['sections_suffix']}"
    language_markup = language_switcher(locale_code, prompt["slug"], ui)

    return f"""<!DOCTYPE html>
<html lang="{escape(locale_config['lang'])}">
<head>
{head}
</head>
<body data-copy-success="{escape(ui['detail'].get('copy_success', 'Copied'))}" data-copy-failed="{escape(ui['detail'].get('copy_failed', 'Copy failed'))}" data-clicks-label="{escape(ui['detail']['clicks_label'])}" data-likes-label="{escape(ui['detail']['likes_label'])}" data-score-label="{escape(ui['detail']['score_label'])}" data-like-button-label="{escape(ui['detail']['like_button'])}" data-liked-button-label="{escape(ui['detail']['liked_button'])}" data-prompt-slug="{escape(prompt['slug'])}" data-api-base="../../api">
  <main class="detail-page">
    <section class="masthead">
      <div class="masthead-inner">
        <span class="masthead-brand">{escape(site_config["site_name"])}</span>
        <div class="masthead-links">
          <a href="../index.html">{escape(ui['nav']['browse'])}</a>
          <a href="../index.html#featured">{escape(ui['nav']['featured'])}</a>
        </div>
        {language_markup}
      </div>
    </section>
    <header class="detail-header">
      <a class="back-link" href="../index.html">{escape(ui['detail']['back_link'])}</a>
      <div class="eyebrow">{escape(ui['detail']['eyebrow'])}</div>
      <div class="detail-title-row">
        <span class="detail-kicker">#{prompt['number']:02d}</span>
        <h1>{escape(prompt['name'])}</h1>
      </div>
      <div class="badge-row">
        <span class="badge" style="background:{mode_badge_bg};color:{mode_badge_color};">{escape(prompt['mode'])}</span>
        <span class="badge" style="background:{font_bg};color:{font_color};">{escape(prompt['font'])}</span>
        <span class="badge cat-badge">{escape(category_label)}</span>
        <span class="badge detail-sections">{escape(sections_label)}</span>
      </div>
      <p class="detail-desc">{escape(prompt['lead'] or prompt['description'])}</p>
    </header>

    <section class="detail-grid">
      <aside class="detail-sidebar">
        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['analytics_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['analytics_copy'])}</p>
            </div>
            <button class="like-btn" type="button" data-like-button data-slug="{escape(prompt['slug'])}">{escape(ui['detail']['like_button'])}</button>
          </div>
          <div class="engagement-grid">
            <article class="engagement-card">
              <span>{escape(ui['detail']['clicks_label'])}</span>
              <strong data-stat-click-count>{prompt_stats['click_count']}</strong>
            </article>
            <article class="engagement-card">
              <span>{escape(ui['detail']['likes_label'])}</span>
              <strong data-stat-like-count>{prompt_stats['like_count']}</strong>
            </article>
            <article class="engagement-card">
              <span>{escape(ui['detail']['score_label'])}</span>
              <strong data-stat-score>{prompt_stats['score']}</strong>
            </article>
          </div>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['fit_title'])}</h2>
              <p class="section-copy">{escape(use_case)}</p>
            </div>
          </div>
          <div class="detail-keywords">{"".join(f'<span class="catalog-keyword">{escape(keyword)}</span>' for keyword in prompt['keywords'])}</div>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['coverage_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['coverage_copy'])}</p>
            </div>
          </div>
          <div class="section-chip-grid">{"".join(f'<span class="section-chip">{escape(section)}</span>' for section in prompt['layout_sections'])}</div>
        </section>
      </aside>

      <div class="detail-main">
        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['preview_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['preview_copy'])}</p>
            </div>
          </div>
          {generate_preview(prompt, ui)}
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['prompt_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['prompt_copy'])}</p>
            </div>
            <button class="copy-btn" type="button" data-copy-target="prompt-text">{escape(ui['detail']['copy_button'])}</button>
          </div>
          <pre class="prompt-block"><code id="prompt-text">{escape(prompt['prompt'])}</code></pre>
        </section>
      </div>
    </section>
  </main>
  {json_script_tag("featured-stats-data", featured_stats)}
  <script src="{relative_asset_href(prompt['slug'], filename='detail.js')}" defer></script>
</body>
</html>"""


def home_labels(ui: dict) -> dict:
    return {
        "search_label": ui.get("search_label", "Search"),
        "hero_visual_label": ui.get("hero_visual_label", "Prompt index"),
        "featured_title": ui.get("featured", {}).get("section_title", ui.get("featured_label", "Featured")),
        "featured_body": ui.get("featured", {}).get("section_body", ui.get("featured", {}).get("source_body", "")),
        "trending_title": ui.get("trending", {}).get("title", "Trending"),
        "trending_body": ui.get("trending", {}).get("body", "Popular styles from the collection."),
        "just_added_title": ui.get("just_added", {}).get("title", "Just Added"),
        "just_added_body": ui.get("just_added", {}).get("body", "Recently added prompt styles."),
        "tags_title": ui.get("tags", {}).get("title", "Browse by Tag"),
        "tags_body": ui.get("tags", {}).get("body", "Jump into broad visual families and reusable keywords."),
        "directory_title": ui.get("catalog", {}).get("directory_title", ui.get("catalog", {}).get("title", "Prompt Catalog")),
        "directory_body": ui.get("catalog", {}).get("directory_body", ui.get("catalog", {}).get("body", "")),
        "all_prompts_label": ui.get("all_prompts_label", "All prompts"),
    }


def detail_labels(ui: dict) -> dict:
    detail = ui["detail"]
    return {
        "visual_tab": detail.get("visual_tab", "Visual"),
        "raw_tab": detail.get("raw_tab", "Prompt"),
        "palette_title": detail.get("palette_title", "Color Palette"),
        "palette_copy": detail.get("palette_copy", "Key colors inferred from this prompt style."),
        "typography_title": detail.get("typography_title", "Typography"),
        "typography_copy": detail.get("typography_copy", "Font family and scale cues for adapting the prompt."),
        "anatomy_title": detail.get("anatomy_title", "Prompt Anatomy"),
        "anatomy_copy": detail.get("anatomy_copy", "The main building blocks covered by this prompt."),
        "sticky_title": detail.get("sticky_title", "Use this prompt"),
        "sticky_copy": detail.get("sticky_copy", "Copy the prompt, then adapt details to your own product, audience, and content."),
        "primary_color": detail.get("primary_color", "Primary"),
        "background_color": detail.get("background_color", "Background"),
        "surface_color": detail.get("surface_color", "Surface"),
        "text_color": detail.get("text_color", "Text"),
    }


def stats_markup(slug: str, stats: dict, ui: dict, *, class_name: str = "card-stats") -> str:
    return f"""<div class="{class_name}" data-stat-for="{escape(slug)}">
  <span><strong data-stat-click-count>{stats['click_count']}</strong> {escape(ui['featured']['clicks_label'])}</span>
  <span><strong data-stat-like-count>{stats['like_count']}</strong> {escape(ui['featured']['likes_label'])}</span>
</div>"""


def compact_prompt_card(prompt: dict, locale_config: dict, *, class_name: str, index_label: str | None = None, stats: dict | None = None, ui: dict | None = None) -> str:
    theme = get_theme(prompt["slug"])
    category_label = localized_category(prompt, locale_config)
    note = summarize_description(prompt["lead"] or prompt["description"], 128)
    index_markup = f'<span class="card-number">{escape(index_label)}</span>' if index_label else f'<span class="card-number">#{prompt["number"]:02d}</span>'
    keyword_markup = "".join(f'<span>{escape(keyword)}</span>' for keyword in prompt["keywords"][:3])
    stat_line = stats_markup(prompt["slug"], stats, ui) if stats and ui else ""
    return f"""<a href="prompts/{prompt['slug']}.html" class="{class_name}" style="--card-accent:{theme['accent']};--card-bg:{theme['hero_bg']};--card-text:{theme['text']};" data-track-click data-slug="{escape(prompt['slug'])}">
  <div class="prompt-art" style="background:{theme['hero_bg']};color:{theme['text']};font-family:{theme['font']};">
    <span style="color:{theme['accent']};">Aa</span>
  </div>
  <div class="prompt-card-copy">
    <div class="catalog-topline">
      {index_markup}
      <span class="catalog-category">{escape(category_label)}</span>
    </div>
    <h3>{escape(prompt['name'])}</h3>
    <p>{escape(note)}</p>
    <div class="micro-tags">{keyword_markup}</div>
    {stat_line}
  </div>
</a>"""


def generate_index_page(prompts: list[dict], site_config: dict, locale_code: str, featured_stats: dict) -> str:
    locale_config = site_config["locales"][locale_code]
    ui = locale_config["ui"]
    labels = home_labels(ui)
    featured_slugs = site_config.get("featured_prompt_slugs", [])
    prompt_by_slug = {prompt["slug"]: prompt for prompt in prompts}
    featured_prompts = [prompt_by_slug[slug] for slug in featured_slugs if slug in prompt_by_slug]
    if len(featured_prompts) < 3:
        featured_prompts.extend(prompt for prompt in prompts if prompt not in featured_prompts)
    featured_prompts = featured_prompts[:3]
    trending_prompts = ranked_featured_prompts(prompts, featured_stats, featured_slugs, limit=8)
    just_added_prompts = sorted(prompts, key=lambda item: item["number"], reverse=True)[:8]
    total_sections = sum(len(prompt["layout_sections"]) for prompt in prompts)
    prompt_index_data = []
    cards = []

    for prompt in prompts:
        theme = get_theme(prompt["slug"])
        category_label = localized_category(prompt, locale_config)
        keyword_badges = "".join(f'<span class="catalog-keyword">{escape(keyword)}</span>' for keyword in prompt["keywords"][:4])
        section_preview = " / ".join(prompt["layout_sections"][:4])
        sections_label = f"{len(prompt['layout_sections'])} {ui['detail']['sections_suffix']}"
        prompt_stats = featured_stats["prompts"][prompt["slug"]]
        prompt_index_data.append(
            {
                "slug": prompt["slug"],
                "number": prompt["number"],
                "name": prompt["name"],
                "note": prompt["lead"] or summarize_description(prompt["description"], 72),
                "href": f"prompts/{prompt['slug']}.html",
                "accent": theme["accent"],
                "click_count": prompt_stats["click_count"],
                "like_count": prompt_stats["like_count"],
                "score": prompt_stats["score"],
            }
        )
        cards.append(
            f"""<a href="prompts/{prompt['slug']}.html" class="catalog-item" data-track-click data-slug="{escape(prompt['slug'])}" data-mode="{escape(prompt['mode'])}" data-font="{escape(prompt['font'])}" data-category="{escape(category_label)}" data-category-search="{escape(category_label.lower())}" data-keywords="{escape(' '.join(prompt['keywords']).lower())}" data-name="{escape(prompt['name'].lower())}" style="--card-accent:{theme['accent']};--card-bg:{theme['hero_bg']};--card-text:{theme['text']};">
  <div class="catalog-preview" style="background:{theme['hero_bg']};color:{theme['text']};font-family:{theme['font']};">
    <span class="catalog-preview-mark" style="color:{theme['accent']};">Aa</span>
  </div>
  <div class="catalog-body">
    <div class="catalog-topline">
      <span class="card-number">#{prompt['number']:02d}</span>
      <span class="catalog-category">{escape(category_label)}</span>
    </div>
    <h2 class="catalog-title">{escape(prompt['name'])}</h2>
    <p class="catalog-lead">{escape(summarize_description(prompt['lead'] or prompt['description'], 128))}</p>
    <div class="card-badges">
      <span class="mini-badge mode-{escape(prompt['mode'])}">{escape(prompt['mode'])}</span>
      <span class="mini-badge font-{escape(prompt['font'].replace('-', ''))}">{escape(prompt['font'])}</span>
      <span class="mini-badge catalog-sections">{escape(sections_label)}</span>
    </div>
    <div class="catalog-keywords">{keyword_badges}</div>
    <p class="catalog-sections-line">{escape(section_preview)}</p>
  </div>
</a>"""
        )

    category_tags = [f'<button class="topic-chip active" type="button" data-topic-category="all">{escape(ui["filters"]["all_categories"])}</button>']
    for category_key in ("tech", "editorial", "expressive", "tactile"):
        category_label = locale_config["category_labels"][category_key]
        category_tags.append(f'<button class="topic-chip" type="button" data-topic-category="{escape(category_label)}">{escape(category_label)}</button>')

    keyword_tags = []
    seen_keywords: set[str] = set()
    for prompt in prompts:
        for keyword in prompt["keywords"]:
            if keyword.lower() in seen_keywords:
                continue
            seen_keywords.add(keyword.lower())
            keyword_tags.append(f'<button class="topic-chip subtle" type="button" data-topic-search="{escape(keyword)}">{escape(keyword)}</button>')
            if len(keyword_tags) >= 8:
                break
        if len(keyword_tags) >= 8:
            break

    head = base_head(
        site_config,
        locale_code,
        locale_config,
        title=locale_config["site_title"],
        description=locale_config["site_description"],
        canonical=absolute_locale_url(site_config["site_url"], locale_code),
        stylesheet_path=relative_asset_href(filename="styles.css"),
        favicon_path=relative_asset_href(filename="favicon.svg"),
    )

    featured_ui_payload = {
        "clicksLabel": ui["featured"]["clicks_label"],
        "likesLabel": ui["featured"]["likes_label"],
    }
    language_markup = language_switcher(locale_code, None, ui)
    theme_markup = theme_switcher(ui)
    hero_visual_items = "".join(
        compact_prompt_card(prompt, locale_config, class_name="hero-prompt-card", index_label=f"{index:02d}", stats=featured_stats["prompts"][prompt["slug"]], ui=ui)
        for index, prompt in enumerate(featured_prompts, start=1)
    )
    featured_markup = "".join(compact_prompt_card(prompt, locale_config, class_name="feature-card", stats=featured_stats["prompts"][prompt["slug"]], ui=ui) for prompt in featured_prompts)
    trending_markup = "".join(
        f"""<a href="prompts/{prompt['slug']}.html" class="trend-link" data-trending-item data-track-click data-slug="{escape(prompt['slug'])}" style="--card-accent:{get_theme(prompt['slug'])['accent']};">
  <span class="trend-rank">{index:02d}</span>
  <span class="trend-name">{escape(prompt['name'])}</span>
  <span class="trend-meta">{escape(localized_category(prompt, locale_config))}</span>
  {stats_markup(prompt["slug"], featured_stats["prompts"][prompt["slug"]], ui, class_name="trend-stats")}
</a>"""
        for index, prompt in enumerate(trending_prompts, start=1)
    )
    just_added_markup = "".join(
        f"""<a href="prompts/{prompt['slug']}.html" class="added-link" style="--card-accent:{get_theme(prompt['slug'])['accent']};">
  <span>#{prompt['number']:02d}</span>
  <strong>{escape(prompt['name'])}</strong>
  <em>{escape(prompt['mode'])} / {escape(prompt['font'])}</em>
</a>"""
        for prompt in just_added_prompts
    )

    return f"""<!DOCTYPE html>
<html lang="{escape(locale_config['lang'])}">
<head>
{head}
</head>
<body data-results-suffix="{escape(ui['results_suffix'])}" data-api-base="../api">
  <header class="masthead">
    <div class="masthead-inner">
      <a class="masthead-brand" href="#top">{escape(site_config["site_name"])}</a>
      <nav class="masthead-links" aria-label="Primary">
        <a href="#featured">{escape(ui['nav']['featured'])}</a>
        <a href="#catalog">{escape(ui['nav']['browse'])}</a>
      </nav>
      <div class="masthead-actions">
        {theme_markup}
        {language_markup}
      </div>
    </div>
  </header>

  <main class="page-shell" id="top">
    <section class="home-hero">
      <div class="hero-copy">
        <p class="hero-badge">{escape(ui["hero_badge"])}</p>
        <h1 class="hero-title">{ui["hero_title_html"]}</h1>
        <p class="hero-subtitle">{escape(locale_config["home_intro"])}</p>
        <label class="hero-search" for="searchInput">
          <span>{escape(labels['search_label'])}</span>
          <input id="searchInput" type="search" placeholder="{escape(ui['search_placeholder'])}">
        </label>
        <div class="hero-meta">{"".join(f"<span>{escape(item)}</span>" for item in ui["hero_meta"])}</div>
      </div>
      <div class="hero-visual" aria-label="{escape(labels['hero_visual_label'])}">
        <div class="hero-visual-head">
          <span>{escape(labels['all_prompts_label'])}</span>
          <strong>{len(prompts)}</strong>
        </div>
        <div class="hero-card-stack">{hero_visual_items}</div>
      </div>
    </section>

    <section class="quick-stats" aria-label="Collection stats">
      <div class="quick-stat"><span class="quick-stat-value">{len(prompts)}</span><span class="quick-stat-label">{escape(ui['stats']['styles'])}</span></div>
      <div class="quick-stat"><span class="quick-stat-value">4</span><span class="quick-stat-label">{escape(ui['stats']['categories'])}</span></div>
      <div class="quick-stat"><span class="quick-stat-value">3</span><span class="quick-stat-label">{escape(ui['stats']['font_modes'])}</span></div>
      <div class="quick-stat"><span class="quick-stat-value">{total_sections}</span><span class="quick-stat-label">{escape(ui['stats']['sections'])}</span></div>
    </section>

    <section class="section-block" id="featured">
      <div class="section-heading">
        <div>
          <p class="section-kicker">{escape(ui['featured_label'])}</p>
          <h2>{escape(labels['featured_title'])}</h2>
        </div>
        <p>{escape(labels['featured_body'])}</p>
      </div>
      <div class="feature-grid">{featured_markup}</div>
    </section>

    <section class="split-block">
      <div class="section-block compact">
        <div class="section-heading stacked">
          <p class="section-kicker">{escape(labels['trending_title'])}</p>
          <h2>{escape(labels['trending_body'])}</h2>
        </div>
        <div class="trend-list">{trending_markup}</div>
      </div>
      <div class="section-block compact">
        <div class="section-heading stacked">
          <p class="section-kicker">{escape(labels['just_added_title'])}</p>
          <h2>{escape(labels['just_added_body'])}</h2>
        </div>
        <div class="added-list">{just_added_markup}</div>
      </div>
    </section>

    <section class="catalog-shell" id="catalog">
      <div class="catalog-header">
        <div>
          <p class="section-kicker">{escape(ui['catalog']['kicker'])}</p>
          <h2>{escape(labels['directory_title'])}</h2>
        </div>
        <p class="catalog-header-copy">{escape(labels['directory_body'])}</p>
      </div>

      <div class="catalog-tools">
        <div class="topic-panel" id="topics">
          <div>
            <p class="section-kicker">{escape(labels['tags_title'])}</p>
            <p class="topic-copy">{escape(labels['tags_body'])}</p>
          </div>
          <div class="topic-cloud">{"".join(category_tags)}{"".join(keyword_tags)}</div>
        </div>

      <div class="filter-panel">
        <div class="filter-row">
          <div class="filter-group" data-filter-group>
            <span class="filter-label">{escape(ui['filters']['mode_label'])}</span>
            <button class="filter-btn active" type="button" data-selectable data-filter="mode" data-value="all">{escape(ui['filters']['mode']['all'])}</button>
            <button class="filter-btn" type="button" data-selectable data-filter="mode" data-value="dark">{escape(ui['filters']['mode']['dark'])}</button>
            <button class="filter-btn" type="button" data-selectable data-filter="mode" data-value="light">{escape(ui['filters']['mode']['light'])}</button>
          </div>

          <div class="filter-group" data-filter-group>
            <span class="filter-label">{escape(ui['filters']['font_label'])}</span>
            <button class="filter-btn active" type="button" data-selectable data-filter="font" data-value="all">{escape(ui['filters']['font']['all'])}</button>
            <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="serif">{escape(ui['filters']['font']['serif'])}</button>
            <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="sans-serif">{escape(ui['filters']['font']['sans-serif'])}</button>
            <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="mono">{escape(ui['filters']['font']['mono'])}</button>
          </div>
        </div>

        <p class="result-summary" id="resultCount">{len(prompts)} {escape(ui['results_suffix'])}</p>
      </div>
      </div>

      <main class="cards-grid" aria-label="{escape(ui['cards_aria_label'])}">
        {"".join(cards)}
      </main>

      <div class="no-results" id="noResults" hidden>
        <p>{escape(ui['no_results'])}</p>
      </div>
    </section>

    <footer class="site-footer">
      <p class="footer-title">{escape(site_config['site_name'])}</p>
      <p class="footer-hint">{escape(ui['footer_hint'])}</p>
    </footer>
  </main>
  {json_script_tag("prompt-index-data", prompt_index_data)}
  {json_script_tag("featured-stats-data", featured_stats)}
  {json_script_tag("featured-ui-data", featured_ui_payload)}
  <script src="{relative_asset_href(filename='app.js')}" defer></script>
</body>
</html>"""


def generate_detail_page(prompt: dict, site_config: dict, locale_code: str, featured_stats: dict) -> str:
    locale_config = site_config["locales"][locale_code]
    ui = locale_config["ui"]
    labels = detail_labels(ui)
    category_label = localized_category(prompt, locale_config)
    use_case = localized_use_case(prompt, locale_config)
    prompt_stats = featured_stats["prompts"][prompt["slug"]]
    theme = get_theme(prompt["slug"])

    title = f"{prompt['name']} | {site_config['site_name']}"
    description = summarize_description(prompt["description"], 150)
    canonical = absolute_locale_url(site_config["site_url"], locale_code, prompt["slug"])
    head = base_head(
        site_config,
        locale_code,
        locale_config,
        title=title,
        description=description,
        canonical=canonical,
        stylesheet_path=relative_asset_href(prompt["slug"], filename="styles.css"),
        favicon_path=relative_asset_href(prompt["slug"], filename="favicon.svg"),
        og_title=prompt["name"],
        slug=prompt["slug"],
    )

    sections_label = f"{len(prompt['layout_sections'])} {ui['detail']['sections_suffix']}"
    language_markup = language_switcher(locale_code, prompt["slug"], ui)
    theme_markup = theme_switcher(ui)
    palette = [
        (labels["primary_color"], theme["accent"]),
        (labels["background_color"], theme["bg"]),
        (labels["surface_color"], theme["card_bg"]),
        (labels["text_color"], theme["text"]),
    ]
    palette_markup = "".join(
        f"""<div class="palette-item">
  <span class="palette-swatch" style="background:{value};"></span>
  <strong>{escape(name)}</strong>
  <code>{escape(value)}</code>
</div>"""
        for name, value in palette
    )
    type_markup = f"""<div class="type-spec display" style="font-family:{theme['font']};">Aa</div>
<div class="type-spec-copy">
  <span>{escape(prompt['font'])}</span>
  <strong style="font-family:{theme['font']};">{escape(prompt['name'])}</strong>
  <p>{escape(summarize_description(prompt['lead'] or prompt['description'], 140))}</p>
</div>"""
    anatomy_markup = "".join(
        f"""<article class="anatomy-item">
  <span>{index:02d}</span>
  <strong>{escape(section)}</strong>
</article>"""
        for index, section in enumerate(prompt["layout_sections"], start=1)
    )

    return f"""<!DOCTYPE html>
<html lang="{escape(locale_config['lang'])}">
<head>
{head}
</head>
<body data-copy-success="{escape(ui['detail'].get('copy_success', 'Copied'))}" data-copy-failed="{escape(ui['detail'].get('copy_failed', 'Copy failed'))}" data-like-button-label="{escape(ui['detail']['like_button'])}" data-liked-button-label="{escape(ui['detail']['liked_button'])}" data-prompt-slug="{escape(prompt['slug'])}" data-api-base="../../api">
  <header class="masthead">
    <div class="masthead-inner">
      <a class="masthead-brand" href="../index.html">{escape(site_config["site_name"])}</a>
      <nav class="masthead-links" aria-label="Primary">
        <a href="../index.html#catalog">{escape(ui['nav']['browse'])}</a>
        <a href="../index.html#featured">{escape(ui['nav']['featured'])}</a>
      </nav>
      <div class="masthead-actions">
        {theme_markup}
        {language_markup}
      </div>
    </div>
  </header>

  <main class="detail-page" style="--prompt-accent:{theme['accent']};">
    <section class="detail-hero">
      <a class="back-link" href="../index.html">{escape(ui['detail']['back_link'])}</a>
      <div class="detail-hero-grid">
        <div>
          <p class="eyebrow">{escape(ui['detail']['eyebrow'])}</p>
          <div class="detail-title-row">
            <span class="detail-kicker">#{prompt['number']:02d}</span>
            <h1>{escape(prompt['name'])}</h1>
          </div>
          <p class="detail-desc">{escape(prompt['lead'] or prompt['description'])}</p>
          <div class="detail-tabs">
            <a href="#visual">{escape(labels['visual_tab'])}</a>
            <a href="#raw">{escape(labels['raw_tab'])}</a>
          </div>
        </div>
        <aside class="detail-meta-panel">
          <div class="badge-row">
            <span class="badge">{escape(prompt['mode'])}</span>
            <span class="badge">{escape(prompt['font'])}</span>
            <span class="badge cat-badge">{escape(category_label)}</span>
            <span class="badge detail-sections">{escape(sections_label)}</span>
          </div>
          <p>{escape(use_case)}</p>
        </aside>
      </div>
    </section>

    <section class="detail-layout">
      <aside class="detail-sidebar">
        <section class="section sticky-action">
          <h2 class="section-title">{escape(labels['sticky_title'])}</h2>
          <p class="section-copy">{escape(labels['sticky_copy'])}</p>
          <button class="copy-btn primary" type="button" data-copy-target="prompt-text">{escape(ui['detail']['copy_button'])}</button>
        </section>
        <section class="section engagement-section">
          <div class="engagement-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['analytics_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['analytics_copy'])}</p>
            </div>
            <button class="like-btn" type="button" data-like-button data-slug="{escape(prompt['slug'])}" aria-pressed="false">{escape(ui['detail']['like_button'])}</button>
          </div>
          <div class="engagement-grid">
            <article class="engagement-card">
              <span>{escape(ui['detail']['clicks_label'])}</span>
              <strong data-stat-click-count>{prompt_stats['click_count']}</strong>
            </article>
            <article class="engagement-card">
              <span>{escape(ui['detail']['likes_label'])}</span>
              <strong data-stat-like-count>{prompt_stats['like_count']}</strong>
            </article>
            <article class="engagement-card">
              <span>{escape(ui['detail']['score_label'])}</span>
              <strong data-stat-score>{prompt_stats['score']}</strong>
            </article>
          </div>
        </section>
        <section class="section">
          <h2 class="section-title">{escape(ui['detail']['fit_title'])}</h2>
          <p class="section-copy">{escape(use_case)}</p>
          <div class="detail-keywords">{"".join(f'<span class="catalog-keyword">{escape(keyword)}</span>' for keyword in prompt['keywords'])}</div>
        </section>
        <section class="section">
          <h2 class="section-title">{escape(ui['detail']['coverage_title'])}</h2>
          <p class="section-copy">{escape(ui['detail']['coverage_copy'])}</p>
          <div class="section-chip-grid">{"".join(f'<span class="section-chip">{escape(section)}</span>' for section in prompt['layout_sections'])}</div>
        </section>
      </aside>

      <div class="detail-main">
        <section class="section preview-section" id="visual">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['preview_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['preview_copy'])}</p>
            </div>
          </div>
          {generate_preview(prompt, ui)}
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(labels['palette_title'])}</h2>
              <p class="section-copy">{escape(labels['palette_copy'])}</p>
            </div>
          </div>
          <div class="palette-grid">{palette_markup}</div>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(labels['typography_title'])}</h2>
              <p class="section-copy">{escape(labels['typography_copy'])}</p>
            </div>
          </div>
          <div class="type-panel">{type_markup}</div>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(labels['anatomy_title'])}</h2>
              <p class="section-copy">{escape(labels['anatomy_copy'])}</p>
            </div>
          </div>
          <div class="anatomy-grid">{anatomy_markup}</div>
        </section>

        <section class="section" id="raw">
          <div class="section-head">
            <div>
              <h2 class="section-title">{escape(ui['detail']['prompt_title'])}</h2>
              <p class="section-copy">{escape(ui['detail']['prompt_copy'])}</p>
            </div>
            <button class="copy-btn" type="button" data-copy-target="prompt-text">{escape(ui['detail']['copy_button'])}</button>
          </div>
          <pre class="prompt-block"><code id="prompt-text">{escape(prompt['prompt'])}</code></pre>
        </section>
      </div>
    </section>
  </main>
  {json_script_tag("featured-stats-data", featured_stats)}
  <script src="{relative_asset_href(prompt['slug'], filename='detail.js')}" defer></script>
</body>
</html>"""


def generate_robots(site_config: dict) -> str:
    sitemap_url = f"{site_config['site_url'].rstrip('/')}/sitemap.xml"
    return f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"


def generate_sitemap(prompts: list[dict], site_config: dict) -> str:
    urls = [site_config["site_url"].rstrip("/") + "/"]
    for locale_code in ("en", "zh"):
        urls.append(absolute_locale_url(site_config["site_url"], locale_code))
        urls.extend(absolute_locale_url(site_config["site_url"], locale_code, prompt["slug"]) for prompt in prompts)
    body = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""
