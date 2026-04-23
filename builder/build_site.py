#!/usr/bin/env python3
"""Build the Design Prompts Collection static site from JSON content."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT_DIR / "content"
SITE_DIR = ROOT_DIR / "site"
PROMPTS_DIR = SITE_DIR / "prompts"
ASSETS_DIR = SITE_DIR / "assets"

PROMPTS_FILE = CONTENT_DIR / "prompts.json"
SITE_CONFIG_FILE = CONTENT_DIR / "site.json"


THEMES = {
    "academia": {"bg": "#1a1612", "text": "#d4c5a9", "accent": "#b8860b", "font": "'Playfair Display',serif", "hero_bg": "linear-gradient(135deg,#1a1612,#2d2318)", "card_bg": "#2d2318"},
    "art-deco": {"bg": "#0d0d0d", "text": "#f0e6d3", "accent": "#d4af37", "font": "'Playfair Display',serif", "hero_bg": "linear-gradient(180deg,#0d0d0d,#1a1a0e)", "card_bg": "#1a1a0e"},
    "aurora-mesh": {"bg": "#0f0f1a", "text": "#e0e0ff", "accent": "#7c3aed", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#0f0f1a,#1a0f2e,#0f1a2e)", "card_bg": "rgba(124,58,237,0.08)"},
    "bauhaus": {"bg": "#ffffff", "text": "#1a1a1a", "accent": "#e63946", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#ffffff 50%,#2563eb 50%)", "card_bg": "#f5f5f5"},
    "bold-typography": {"bg": "#0a0a0a", "text": "#ffffff", "accent": "#ff6b35", "font": "'Inter',sans-serif", "hero_bg": "#0a0a0a", "card_bg": "#141414"},
    "botanical-organic-serif": {"bg": "#faf6f0", "text": "#2d3b2d", "accent": "#c17f59", "font": "'Playfair Display',serif", "hero_bg": "linear-gradient(135deg,#faf6f0,#e8e0d4)", "card_bg": "#ffffff"},
    "clay": {"bg": "#f0e6ff", "text": "#2d1b4e", "accent": "#8b5cf6", "font": "'Nunito',sans-serif", "hero_bg": "linear-gradient(135deg,#f0e6ff,#fce7f3,#dbeafe)", "card_bg": "#ffffff"},
    "cyberpunk": {"bg": "#0a0a0a", "text": "#00ff41", "accent": "#ff0080", "font": "'JetBrains Mono',monospace", "hero_bg": "#0a0a0a", "card_bg": "#111111"},
    "corporate-trust": {"bg": "#ffffff", "text": "#1e293b", "accent": "#6366f1", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#ffffff,#eef2ff)", "card_bg": "#f8fafc"},
    "flat-design": {"bg": "#ffffff", "text": "#1a1a1a", "accent": "#2563eb", "font": "'Inter',sans-serif", "hero_bg": "#2563eb", "card_bg": "#f3f4f6"},
    "glassmorphism": {"bg": "#0f0f23", "text": "#ffffff", "accent": "#a855f7", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#0f0f23,#1a0533,#0f2333)", "card_bg": "rgba(255,255,255,0.05)"},
    "industrial": {"bg": "#e8e4de", "text": "#1a1a1a", "accent": "#ff6600", "font": "'Space Mono',sans-serif", "hero_bg": "linear-gradient(135deg,#e8e4de,#d4cfc7)", "card_bg": "#f0ece6"},
    "kinetic": {"bg": "#0a0a0a", "text": "#ffffff", "accent": "#ffdd00", "font": "'Inter',sans-serif", "hero_bg": "#0a0a0a", "card_bg": "#141414"},
    "luxury": {"bg": "#fafaf8", "text": "#1a1a1a", "accent": "#b8860b", "font": "'Playfair Display',serif", "hero_bg": "linear-gradient(135deg,#fafaf8,#f0ece6)", "card_bg": "#ffffff"},
    "material": {"bg": "#fffbfe", "text": "#1c1b1f", "accent": "#6750a4", "font": "'Roboto',sans-serif", "hero_bg": "#fffbfe", "card_bg": "#f3edf7"},
    "maximalism": {"bg": "#0a0a0a", "text": "#ffffff", "accent": "#ff1493", "font": "'Space Grotesk',sans-serif", "hero_bg": "linear-gradient(135deg,#0a0a0a,#1a0a2e,#2e0a1a)", "card_bg": "#1a1a1a"},
    "simple-dark": {"bg": "#0f172a", "text": "#e2e8f0", "accent": "#f59e0b", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#0f172a,#1e293b)", "card_bg": "rgba(255,255,255,0.05)"},
    "modern-dark": {"bg": "#09090b", "text": "#fafafa", "accent": "#8b5cf6", "font": "'Inter',sans-serif", "hero_bg": "#09090b", "card_bg": "rgba(255,255,255,0.04)"},
    "monochrome": {"bg": "#ffffff", "text": "#000000", "accent": "#000000", "font": "'Playfair Display',serif", "hero_bg": "#ffffff", "card_bg": "#f5f5f5"},
    "neo-brutalism": {"bg": "#fffdf0", "text": "#1a1a1a", "accent": "#ff3333", "font": "'Space Grotesk',sans-serif", "hero_bg": "#fffdf0", "card_bg": "#ffffff"},
    "neumorphism": {"bg": "#e0e5ec", "text": "#2d3748", "accent": "#6366f1", "font": "'Inter',sans-serif", "hero_bg": "#e0e5ec", "card_bg": "#e0e5ec"},
    "newsprint": {"bg": "#f5f0eb", "text": "#1a1a1a", "accent": "#cc0000", "font": "'Playfair Display',serif", "hero_bg": "#f5f0eb", "card_bg": "#ffffff"},
    "organic-natural": {"bg": "#faf6f0", "text": "#2d3b2d", "accent": "#8b6f47", "font": "'Playfair Display',serif", "hero_bg": "linear-gradient(135deg,#faf6f0,#e8dfd4)", "card_bg": "#ffffff"},
    "playful-geometric": {"bg": "#ffffff", "text": "#1a1a1a", "accent": "#ff6b6b", "font": "'Nunito',sans-serif", "hero_bg": "#ffffff", "card_bg": "#fff0f0"},
    "business-style": {"bg": "#faf8f5", "text": "#1a1a1a", "accent": "#8b6f47", "font": "'Playfair Display',serif", "hero_bg": "linear-gradient(135deg,#faf8f5,#f0ece6)", "card_bg": "#ffffff"},
    "retro": {"bg": "#c0c0c0", "text": "#000000", "accent": "#000080", "font": "'Tahoma',sans-serif", "hero_bg": "#c0c0c0", "card_bg": "#ffffff"},
    "tech-style": {"bg": "#ffffff", "text": "#0f172a", "accent": "#2563eb", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#ffffff,#eff6ff)", "card_bg": "#f8fafc"},
    "hand-drawn-sketch": {"bg": "#faf8f0", "text": "#2d2d2d", "accent": "#e85d04", "font": "'Patrick Hand',sans-serif", "hero_bg": "#faf8f0", "card_bg": "#fff8dc"},
    "swiss": {"bg": "#ffffff", "text": "#000000", "accent": "#ff0000", "font": "'Inter',sans-serif", "hero_bg": "#ffffff", "card_bg": "#f5f5f5"},
    "terminal-cli": {"bg": "#0c0c0c", "text": "#00ff41", "accent": "#00ff41", "font": "'JetBrains Mono',monospace", "hero_bg": "#0c0c0c", "card_bg": "#111111"},
    "vaporwave": {"bg": "#1a0033", "text": "#ff71ce", "accent": "#01cdfe", "font": "'VT323',monospace", "hero_bg": "linear-gradient(180deg,#1a0033,#330066,#1a0033)", "card_bg": "rgba(255,113,206,0.08)"},
    "crypto": {"bg": "#0a0a0a", "text": "#e0e0e0", "accent": "#f7931a", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#0a0a0a,#1a1000)", "card_bg": "rgba(247,147,26,0.05)"},
}

FALLBACK_THEME = {"bg": "#0f172a", "text": "#e2e8f0", "accent": "#6366f1", "font": "'Inter',sans-serif", "hero_bg": "linear-gradient(135deg,#0f172a,#111827)", "card_bg": "rgba(255,255,255,0.05)"}

CATEGORY_GROUPS = {
    "科技 / SaaS / 金融": {
        "tech-style",
        "modern-dark",
        "simple-dark",
        "corporate-trust",
        "material",
        "crypto",
        "terminal-cli",
        "flat-design",
        "aurora-mesh",
    },
    "编辑 / 排版 / 机构感": {
        "monochrome",
        "swiss",
        "newsprint",
        "academia",
        "luxury",
        "bold-typography",
        "business-style",
    },
    "强风格 / 强情绪 / 年轻化": {
        "clay",
        "playful-geometric",
        "kinetic",
        "maximalism",
        "retro",
        "vaporwave",
        "neo-brutalism",
    },
    "物理质感 / 设计史": {
        "bauhaus",
        "art-deco",
        "industrial",
        "neumorphism",
        "botanical-organic-serif",
        "organic-natural",
        "hand-drawn-sketch",
        "cyberpunk",
        "glassmorphism",
    },
}

INDEX_SCRIPT = """const state = { mode: 'all', font: 'all', category: 'all' };

function setActive(group, button) {
  group.querySelectorAll('[data-selectable]').forEach((item) => item.classList.remove('active'));
  button.classList.add('active');
}

function filterCards() {
  const search = document.getElementById('searchInput').value.trim().toLowerCase();
  let visible = 0;

  document.querySelectorAll('.style-card').forEach((card) => {
    const matchesMode = state.mode === 'all' || card.dataset.mode === state.mode;
    const matchesFont = state.font === 'all' || card.dataset.font === state.font;
    const matchesCategory = state.category === 'all' || card.dataset.category === state.category;
    const matchesSearch =
      !search ||
      card.dataset.name.includes(search) ||
      card.dataset.mode.includes(search) ||
      card.dataset.font.includes(search) ||
      card.dataset.categorySearch.includes(search);

    const isVisible = matchesMode && matchesFont && matchesCategory && matchesSearch;
    card.hidden = !isVisible;
    if (isVisible) visible += 1;
  });

  document.getElementById('resultCount').textContent = `${visible} styles`;
  document.getElementById('noResults').hidden = visible !== 0;
}

document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const group = button.closest('[data-filter-group]');
    setActive(group, button);
    state[button.dataset.filter] = button.dataset.value;
    filterCards();
  });
});

document.getElementById('searchInput').addEventListener('input', filterCards);
filterCards();
"""

DETAIL_SCRIPT = """const copyButton = document.querySelector('[data-copy-target]');

if (copyButton) {
  copyButton.addEventListener('click', async () => {
    const target = document.getElementById(copyButton.dataset.copyTarget);
    if (!target) return;

    try {
      await navigator.clipboard.writeText(target.textContent);
      const originalLabel = copyButton.textContent;
      copyButton.textContent = 'Copied';
      copyButton.classList.add('copied');
      window.setTimeout(() => {
        copyButton.textContent = originalLabel;
        copyButton.classList.remove('copied');
      }, 1800);
    } catch (error) {
      copyButton.textContent = 'Copy failed';
    }
  });
}
"""

STYLESHEET = """:root {
  --bg: #0a0a0f;
  --surface: #12121a;
  --surface-2: #1a1a28;
  --surface-3: #222238;
  --text: #e8e8f0;
  --text-muted: #9a9ab2;
  --accent: #6366f1;
  --accent-soft: rgba(99, 102, 241, 0.14);
  --border: rgba(255, 255, 255, 0.08);
  --shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  --radius: 16px;
  --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --mono: 'JetBrains Mono', 'Fira Code', monospace;
}

*, *::before, *::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: var(--font);
  background:
    radial-gradient(circle at top, rgba(99, 102, 241, 0.18), transparent 32%),
    linear-gradient(180deg, #0b0b12 0%, #090910 100%);
  color: var(--text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a { color: inherit; }

.page-shell {
  min-height: 100vh;
  position: relative;
}

.hero-section {
  padding: 84px 24px 32px;
}

.hero-content,
.controls-section,
.cards-grid,
.site-footer,
.detail-page {
  width: min(1200px, calc(100% - 48px));
  margin: 0 auto;
}

.hero-content {
  padding: 36px;
  border: 1px solid var(--border);
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01)),
    rgba(18, 18, 26, 0.82);
  box-shadow: var(--shadow);
}

.hero-badge,
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid rgba(99, 102, 241, 0.28);
  background: var(--accent-soft);
  color: #c8cbff;
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-title {
  margin: 20px 0 16px;
  font-size: clamp(2.8rem, 7vw, 5.5rem);
  line-height: 0.95;
  letter-spacing: -0.04em;
}

.hero-title span {
  color: #a5b4fc;
}

.hero-subtitle {
  max-width: 760px;
  margin: 0;
  font-size: 1.08rem;
  color: var(--text-muted);
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 24px;
  color: #cfd1e8;
  font-size: 0.9rem;
}

.controls-section {
  padding: 0 0 16px;
}

.search-container,
.filter-panel {
  border: 1px solid var(--border);
  border-radius: 22px;
  background: rgba(18, 18, 26, 0.72);
  backdrop-filter: blur(10px);
}

.search-container {
  padding: 12px;
  margin-bottom: 16px;
}

#searchInput {
  width: 100%;
  padding: 16px 18px;
  border: 1px solid transparent;
  border-radius: 14px;
  background: var(--surface);
  color: var(--text);
  font: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

#searchInput:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.6);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
}

.filter-panel {
  padding: 18px;
}

.filter-row,
.category-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-row {
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.filter-label {
  color: var(--text-muted);
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-right: 4px;
}

.filter-btn,
.cat-btn,
.copy-btn {
  padding: 8px 14px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font: inherit;
  transition: all 0.2s ease;
}

.filter-btn:hover,
.cat-btn:hover,
.copy-btn:hover,
.back-link:hover {
  border-color: rgba(99, 102, 241, 0.55);
  color: var(--text);
}

.filter-btn.active,
.cat-btn.active {
  border-color: rgba(99, 102, 241, 0.36);
  background: var(--accent-soft);
  color: #d8dbff;
}

.result-summary {
  margin: 10px 0 0;
  color: var(--text-muted);
  font-size: 0.88rem;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 18px 0 40px;
}

.style-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid var(--border);
  text-decoration: none;
  background: rgba(18, 18, 26, 0.84);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
  transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
}

.style-card:hover {
  transform: translateY(-5px);
  border-color: var(--card-accent, var(--accent));
  box-shadow: 0 24px 50px rgba(0, 0, 0, 0.26);
}

.style-card[hidden] {
  display: none;
}

.card-preview {
  height: 132px;
  display: grid;
  place-items: center;
}

.card-preview-text {
  font-size: 3rem;
  font-weight: 900;
  opacity: 0.65;
}

.card-body {
  padding: 18px 18px 20px;
}

.card-number,
.detail-kicker {
  font-family: var(--mono);
  color: var(--text-muted);
  font-size: 0.78rem;
}

.card-title {
  margin: 8px 0 10px;
  font-size: 1.16rem;
}

.card-badges,
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.mini-badge,
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.74rem;
}

.mode-dark { background: #1e293b; color: #9fb2cb; }
.mode-light { background: #f1f5f9; color: #475569; }
.font-serif { background: #fef3c7; color: #92400e; }
.font-sansserif { background: #dbeafe; color: #1d4ed8; }
.font-mono { background: #d1fae5; color: #047857; }
.cat-badge { background: rgba(99, 102, 241, 0.16); color: #cfd2ff; }

.card-desc,
.detail-desc,
.footer-hint,
.section-copy {
  color: var(--text-muted);
}

.no-results {
  width: min(1200px, calc(100% - 48px));
  margin: 0 auto 40px;
  padding: 24px;
  border: 1px dashed var(--border);
  border-radius: 18px;
  color: var(--text-muted);
  text-align: center;
}

.no-results[hidden] {
  display: none;
}

.site-footer {
  padding: 12px 0 56px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.footer-hint code,
.prompt-block {
  font-family: var(--mono);
}

.detail-page {
  padding: 56px 0 72px;
}

.detail-header {
  margin-bottom: 34px;
}

.back-link {
  display: inline-flex;
  margin-bottom: 20px;
  text-decoration: none;
  color: #cfd2ff;
}

.detail-title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 14px;
  margin: 10px 0 14px;
}

.detail-title-row h1 {
  margin: 0;
  font-size: clamp(2rem, 5vw, 3.4rem);
  line-height: 1;
}

.detail-desc {
  max-width: 760px;
  margin-top: 14px;
  font-size: 1rem;
}

.section {
  margin-bottom: 34px;
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: rgba(18, 18, 26, 0.8);
}

.section-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 18px;
}

.section-title {
  margin: 0;
  font-size: 1.1rem;
}

.preview-container {
  overflow: hidden;
  border-radius: 18px;
  border: 1px solid var(--border);
}

.prompt-block {
  margin: 0;
  padding: 20px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  border-radius: 18px;
  background: #0d0d14;
  border: 1px solid var(--border);
  font-size: 0.86rem;
  line-height: 1.75;
}

.copy-btn.copied {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

@media (max-width: 800px) {
  .hero-content,
  .controls-section,
  .cards-grid,
  .site-footer,
  .detail-page,
  .no-results {
    width: min(100% - 24px, 1200px);
  }

  .hero-section {
    padding: 68px 0 24px;
  }

  .hero-content,
  .section {
    padding: 22px;
  }

  .filter-row {
    flex-direction: column;
    gap: 12px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .section-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="16" fill="#0b0b12"/>
  <rect x="8" y="8" width="48" height="48" rx="12" fill="url(#g)" opacity="0.14"/>
  <path d="M18 19h28v6H18zm0 10h20v6H18zm0 10h28v6H18z" fill="url(#g)"/>
  <circle cx="46" cy="42" r="4" fill="#a5b4fc"/>
</svg>
"""

OG_COVER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0b12"/>
      <stop offset="100%" stop-color="#17172a"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <circle cx="220" cy="120" r="220" fill="#818cf8" opacity="0.12"/>
  <circle cx="980" cy="120" r="180" fill="#22d3ee" opacity="0.08"/>
  <circle cx="1010" cy="520" r="220" fill="#818cf8" opacity="0.1"/>
  <rect x="74" y="74" width="1052" height="482" rx="36" fill="none" stroke="rgba(255,255,255,0.12)"/>
  <text x="120" y="250" fill="white" font-family="Inter, Arial, sans-serif" font-size="72" font-weight="700">Design Prompts Collection</text>
  <text x="120" y="330" fill="#a5b4fc" font-family="Inter, Arial, sans-serif" font-size="38">32 verified UI style prompts for focused static inspiration</text>
  <text x="120" y="430" fill="url(#accent)" font-family="JetBrains Mono, monospace" font-size="28">search • filter • preview • copy</text>
</svg>
"""


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def get_theme(slug: str) -> dict[str, str]:
    return THEMES.get(slug, FALLBACK_THEME)


def category_for_slug(slug: str) -> str:
    for category, slugs in CATEGORY_GROUPS.items():
        if slug in slugs:
            return category
    return "其他"


def normalize_prompts(prompts: list[dict]) -> list[dict]:
    normalized = []
    for prompt in prompts:
        item = dict(prompt)
        item["category"] = category_for_slug(item["slug"])
        normalized.append(item)
    return sorted(normalized, key=lambda item: item["number"])


def slug_path(site_url: str, slug: str | None = None) -> str:
    base = site_url.rstrip("/")
    return f"{base}/prompts/{slug}.html" if slug else f"{base}/index.html"


def summarize_description(text: str, max_length: int = 96) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 3].rstrip() + "..."


def base_head(config: dict, *, title: str, description: str, canonical: str, og_title: str | None = None) -> str:
    og_title = og_title or title
    site_name = escape(config["site_name"])
    desc = escape(description)
    canonical_url = escape(canonical)
    og_image = escape(f"{config['site_url'].rstrip('/')}/assets/og-cover.svg")
    keywords = escape(", ".join(config["keywords"]))
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{escape(config['author'])}">
<meta name="theme-color" content="#0b0b12">
<link rel="canonical" href="{canonical_url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Nunito:wght@400;700;900&family=Patrick+Hand&family=Playfair+Display:wght@400;700;900&family=Roboto:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&family=VT323&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ '../assets/styles.css' if canonical.endswith('.html') and '/prompts/' in canonical else './assets/styles.css' }">"""


def generate_preview(prompt: dict) -> str:
    theme = get_theme(prompt["slug"])
    dark_mode = prompt["mode"] == "dark"
    border_color = "rgba(255,255,255,0.12)" if dark_mode else "rgba(0,0,0,0.12)"
    soft_border = "rgba(255,255,255,0.08)" if dark_mode else "rgba(0,0,0,0.08)"
    button_radius = "0" if prompt["slug"] in {"neo-brutalism", "swiss", "newsprint"} else "10px"
    headline = escape(prompt["name"])

    return f"""<div class="preview-container" style="background:{theme['hero_bg']};color:{theme['text']};font-family:{theme['font']};">
  <nav style="display:flex;justify-content:space-between;align-items:center;padding:18px 28px;border-bottom:1px solid {border_color};">
    <div style="font-weight:700;color:{theme['accent']};">{headline}</div>
    <div style="display:flex;gap:18px;font-size:0.85rem;opacity:0.78;">
      <span>Features</span><span>Pricing</span><span>About</span>
    </div>
  </nav>
  <section style="padding:64px 28px 54px;text-align:center;">
    <div style="display:inline-block;padding:6px 14px;border-radius:999px;border:1px solid {border_color};background:rgba(255,255,255,0.04);font-size:0.74rem;text-transform:uppercase;letter-spacing:0.08em;">Design system preview</div>
    <h2 style="font-size:clamp(2rem,5vw,3.5rem);line-height:1.05;margin:22px 0 14px;">Build something<br>beautiful today</h2>
    <p style="max-width:560px;margin:0 auto 24px;font-size:1.02rem;opacity:0.76;">A complete visual system shaped for the modern web, with clear structure, strong hierarchy, and focused interaction.</p>
    <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
      <button style="padding:12px 24px;border-radius:{button_radius};border:1px solid {theme['accent']};background:{theme['accent']};color:#fff;font-weight:600;">Get started</button>
      <button style="padding:12px 24px;border-radius:{button_radius};border:1px solid {border_color};background:transparent;color:{theme['text']};font-weight:600;">Learn more</button>
    </div>
  </section>
  <section style="display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid {border_color};border-bottom:1px solid {border_color};">
    <div style="padding:22px;text-align:center;"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">10K+</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0.1em;">Users</div></div>
    <div style="padding:22px;text-align:center;border-left:1px solid {border_color};"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">99.9%</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0.1em;">Uptime</div></div>
    <div style="padding:22px;text-align:center;border-left:1px solid {border_color};"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">50+</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0.1em;">Features</div></div>
    <div style="padding:22px;text-align:center;border-left:1px solid {border_color};"><div style="font-size:1.9rem;font-weight:800;color:{theme['accent']};">24/7</div><div style="font-size:0.75rem;opacity:0.65;text-transform:uppercase;letter-spacing:0.1em;">Support</div></div>
  </section>
  <section style="padding:42px 28px;">
    <h3 style="margin:0 0 18px;text-align:center;font-size:1.7rem;">Core features</h3>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;">
      <article style="padding:24px;border-radius:14px;background:{theme['card_bg']};border:1px solid {soft_border};"><div style="font-size:1.8rem;margin-bottom:12px;">A</div><strong>Fast setup</strong><p style="margin:8px 0 0;opacity:0.75;font-size:0.9rem;">A focused starting point with clean visual direction.</p></article>
      <article style="padding:24px;border-radius:14px;background:{theme['card_bg']};border:1px solid {soft_border};"><div style="font-size:1.8rem;margin-bottom:12px;">B</div><strong>Clear hierarchy</strong><p style="margin:8px 0 0;opacity:0.75;font-size:0.9rem;">Strong layout rhythm keeps content readable and sharp.</p></article>
      <article style="padding:24px;border-radius:14px;background:{theme['card_bg']};border:1px solid {soft_border};"><div style="font-size:1.8rem;margin-bottom:12px;">C</div><strong>Reusable language</strong><p style="margin:8px 0 0;opacity:0.75;font-size:0.9rem;">A visual reference you can lift directly into prompts and prototypes.</p></article>
    </div>
  </section>
</div>"""


def generate_index_page(prompts: list[dict], config: dict) -> str:
    cards = []
    for prompt in prompts:
        theme = get_theme(prompt["slug"])
        category_search = escape(prompt["category"].lower())
        cards.append(
            f"""<a href="prompts/{prompt['slug']}.html" class="style-card" data-mode="{escape(prompt['mode'])}" data-font="{escape(prompt['font'])}" data-category="{escape(prompt['category'])}" data-category-search="{category_search}" data-name="{escape(prompt['name'].lower())}" style="--card-accent:{theme['accent']};">
  <div class="card-preview" style="background:{theme['hero_bg']};color:{theme['text']};font-family:{theme['font']};">
    <div class="card-preview-text" style="color:{theme['accent']};">Aa</div>
  </div>
  <div class="card-body">
    <div class="card-number">#{prompt['number']:02d}</div>
    <h2 class="card-title">{escape(prompt['name'])}</h2>
    <div class="card-badges">
      <span class="mini-badge mode-{escape(prompt['mode'])}">{escape(prompt['mode'])}</span>
      <span class="mini-badge font-{escape(prompt['font'].replace('-', ''))}">{escape(prompt['font'])}</span>
    </div>
    <p class="card-desc">{escape(summarize_description(prompt['description']))}</p>
  </div>
</a>"""
        )

    category_buttons = ['<button class="cat-btn active" type="button" data-selectable data-filter="category" data-value="all">All categories</button>']
    for category in config["categories"]:
        category_buttons.append(
            f'<button class="cat-btn" type="button" data-selectable data-filter="category" data-value="{escape(category)}">{escape(category)}</button>'
        )

    head = base_head(
        config,
        title=config["site_title"],
        description=config["site_description"],
        canonical=slug_path(config["site_url"]),
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
{head}
</head>
<body>
  <div class="page-shell">
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-badge">Focused static inspiration library</div>
        <h1 class="hero-title">Design prompts<br><span>collection</span></h1>
        <p class="hero-subtitle">{escape(config['home_intro'])}</p>
        <div class="hero-meta">
          <span>32 curated styles</span>
          <span>Prompt-first structure</span>
          <span>Search, filter, preview, copy</span>
        </div>
      </div>
    </section>

    <section class="controls-section">
      <div class="search-container">
        <input id="searchInput" type="search" placeholder="Search styles, modes, fonts, or categories">
      </div>

      <div class="filter-panel">
        <div class="filter-row">
          <div class="filter-group" data-filter-group>
            <span class="filter-label">Mode</span>
            <button class="filter-btn active" type="button" data-selectable data-filter="mode" data-value="all">All</button>
            <button class="filter-btn" type="button" data-selectable data-filter="mode" data-value="dark">Dark</button>
            <button class="filter-btn" type="button" data-selectable data-filter="mode" data-value="light">Light</button>
          </div>

          <div class="filter-group" data-filter-group>
            <span class="filter-label">Font</span>
            <button class="filter-btn active" type="button" data-selectable data-filter="font" data-value="all">All</button>
            <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="serif">Serif</button>
            <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="sans-serif">Sans-serif</button>
            <button class="filter-btn" type="button" data-selectable data-filter="font" data-value="mono">Mono</button>
          </div>
        </div>

        <div class="category-row" data-filter-group>
          {"".join(category_buttons)}
        </div>
        <p class="result-summary" id="resultCount">{len(prompts)} styles</p>
      </div>
    </section>

    <main class="cards-grid" aria-label="Prompt styles">
      {"".join(cards)}
    </main>

    <div class="no-results" id="noResults" hidden>
      <p>No styles match the current filters.</p>
    </div>

    <footer class="site-footer">
      <p>{escape(config['site_name'])}</p>
      <p class="footer-hint">Source: <code>content/prompts.json</code> • Build: <code>python build.py</code></p>
    </footer>
  </div>
  <script src="./assets/app.js" defer></script>
</body>
</html>"""


def generate_detail_page(prompt: dict, config: dict) -> str:
    mode_badge_bg = "#1e293b" if prompt["mode"] == "dark" else "#f1f5f9"
    mode_badge_color = "#cbd5e1" if prompt["mode"] == "dark" else "#334155"
    font_colors = {
        "serif": ("#fef3c7", "#92400e"),
        "sans-serif": ("#dbeafe", "#1d4ed8"),
        "mono": ("#d1fae5", "#047857"),
    }
    font_bg, font_color = font_colors.get(prompt["font"], ("#e5e7eb", "#374151"))

    title = f"{prompt['name']} | {config['site_name']}"
    description = summarize_description(prompt["description"], 150)
    canonical = slug_path(config["site_url"], prompt["slug"])
    head = base_head(config, title=title, description=description, canonical=canonical, og_title=prompt["name"])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
{head}
</head>
<body>
  <main class="detail-page">
    <header class="detail-header">
      <a class="back-link" href="../index.html">Back to collection</a>
      <div class="eyebrow">Prompt detail</div>
      <div class="detail-title-row">
        <span class="detail-kicker">#{prompt['number']:02d}</span>
        <h1>{escape(prompt['name'])}</h1>
      </div>
      <div class="badge-row">
        <span class="badge" style="background:{mode_badge_bg};color:{mode_badge_color};">{escape(prompt['mode'])}</span>
        <span class="badge" style="background:{font_bg};color:{font_color};">{escape(prompt['font'])}</span>
        <span class="badge cat-badge">{escape(prompt['category'])}</span>
      </div>
      <p class="detail-desc">{escape(prompt['description'])}</p>
    </header>

    <section class="section">
      <div class="section-head">
        <div>
          <h2 class="section-title">Style preview</h2>
          <p class="section-copy">A generated landing-page fragment that echoes the prompt's visual language.</p>
        </div>
      </div>
      {generate_preview(prompt)}
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2 class="section-title">Full prompt</h2>
          <p class="section-copy">Copy this prompt directly into your AI workflow.</p>
        </div>
        <button class="copy-btn" type="button" data-copy-target="prompt-text">Copy prompt</button>
      </div>
      <pre class="prompt-block"><code id="prompt-text">{escape(prompt['prompt'])}</code></pre>
    </section>
  </main>
  <script src="../assets/detail.js" defer></script>
</body>
</html>"""


def generate_robots(config: dict) -> str:
    sitemap_url = f"{config['site_url'].rstrip('/')}/sitemap.xml"
    return f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"


def generate_sitemap(prompts: list[dict], config: dict) -> str:
    urls = [slug_path(config["site_url"])]
    urls.extend(slug_path(config["site_url"], prompt["slug"]) for prompt in prompts)
    body = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build() -> None:
    config = load_json(SITE_CONFIG_FILE)
    prompts = normalize_prompts(load_json(PROMPTS_FILE))

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    write_file(ASSETS_DIR / "styles.css", STYLESHEET)
    write_file(ASSETS_DIR / "app.js", INDEX_SCRIPT)
    write_file(ASSETS_DIR / "detail.js", DETAIL_SCRIPT)
    write_file(ASSETS_DIR / "favicon.svg", FAVICON)
    write_file(ASSETS_DIR / "og-cover.svg", OG_COVER)
    write_file(SITE_DIR / "index.html", generate_index_page(prompts, config))
    write_file(SITE_DIR / "robots.txt", generate_robots(config))
    write_file(SITE_DIR / "sitemap.xml", generate_sitemap(prompts, config))

    for prompt in prompts:
        write_file(PROMPTS_DIR / f"{prompt['slug']}.html", generate_detail_page(prompt, config))

    print(f"Built {len(prompts)} prompt pages into {SITE_DIR.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    build()
