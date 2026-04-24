"""Theme and category metadata for prompt rendering."""

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

FALLBACK_THEME = {
    "bg": "#0f172a",
    "text": "#e2e8f0",
    "accent": "#6366f1",
    "font": "'Inter',sans-serif",
    "hero_bg": "linear-gradient(135deg,#0f172a,#111827)",
    "card_bg": "rgba(255,255,255,0.05)",
}

CATEGORY_GROUPS = {
    "tech": {
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
    "editorial": {
        "monochrome",
        "swiss",
        "newsprint",
        "academia",
        "luxury",
        "bold-typography",
        "business-style",
    },
    "expressive": {
        "clay",
        "playful-geometric",
        "kinetic",
        "maximalism",
        "retro",
        "vaporwave",
        "neo-brutalism",
    },
    "tactile": {
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


def get_theme(slug: str) -> dict[str, str]:
    return THEMES.get(slug, FALLBACK_THEME)


def category_for_slug(slug: str) -> str:
    for category, slugs in CATEGORY_GROUPS.items():
        if slug in slugs:
            return category
    return "other"
