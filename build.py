#!/usr/bin/env python3
"""
Build script for Design Prompts Collection static site.

Usage:  python build.py
Add new prompts: edit source_file.md -> run python build.py -> done
"""

import re, os, json
import html as html_module

SOURCE_FILE = "source_file.md"
OUTPUT_DIR = "site"
PROMPTS_DIR = os.path.join(OUTPUT_DIR, "prompts")
DATA_FILE = "prompts.json"

CATEGORIES = {
    "科技 / SaaS / 金融": ["Tech Style","Modern Dark","Simple Dark","Corporate Trust","Material","Crypto","Terminal CLI","Flat Design","Aurora Mesh"],
    "编辑 / 排版 / 机构感": ["Monochrome","Swiss","Newsprint","Academia","Luxury","Bold Typography","Business Style"],
    "强风格 / 强情绪 / 年轻化": ["Clay","Playful Geometric","Kinetic","Maximalism","Retro","Vaporwave","Neo-brutalism"],
    "物理质感 / 设计史": ["Bauhaus","Art Deco","Industrial","Neumorphism","Botanical / Organic Serif","Organic / Natural","Hand-Drawn / Sketch","Cyberpunk","Glassmorphism"]
}

THEMES = {
    "academia": {"bg":"#1a1612","text":"#d4c5a9","accent":"#b8860b","font":"'Playfair Display',serif","hero_bg":"linear-gradient(135deg,#1a1612,#2d2318)","card_bg":"#2d2318"},
    "art-deco": {"bg":"#0d0d0d","text":"#f0e6d3","accent":"#d4af37","font":"'Playfair Display',serif","hero_bg":"linear-gradient(180deg,#0d0d0d,#1a1a0e)","card_bg":"#1a1a0e"},
    "aurora-mesh": {"bg":"#0f0f1a","text":"#e0e0ff","accent":"#7c3aed","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#0f0f1a,#1a0f2e,#0f1a2e)","card_bg":"rgba(124,58,237,0.08)"},
    "bauhaus": {"bg":"#ffffff","text":"#1a1a1a","accent":"#e63946","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#ffffff 50%,#2563eb 50%)","card_bg":"#f5f5f5"},
    "bold-typography": {"bg":"#0a0a0a","text":"#ffffff","accent":"#ff6b35","font":"'Inter',sans-serif","hero_bg":"#0a0a0a","card_bg":"#141414"},
    "botanical-organic-serif": {"bg":"#faf6f0","text":"#2d3b2d","accent":"#c17f59","font":"'Playfair Display',serif","hero_bg":"linear-gradient(135deg,#faf6f0,#e8e0d4)","card_bg":"#ffffff"},
    "clay": {"bg":"#f0e6ff","text":"#2d1b4e","accent":"#8b5cf6","font":"'Nunito',sans-serif","hero_bg":"linear-gradient(135deg,#f0e6ff,#fce7f3,#dbeafe)","card_bg":"#ffffff"},
    "cyberpunk": {"bg":"#0a0a0a","text":"#00ff41","accent":"#ff0080","font":"'JetBrains Mono',monospace","hero_bg":"#0a0a0a","card_bg":"#111111"},
    "corporate-trust": {"bg":"#ffffff","text":"#1e293b","accent":"#6366f1","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#ffffff,#eef2ff)","card_bg":"#f8fafc"},
    "flat-design": {"bg":"#ffffff","text":"#1a1a1a","accent":"#2563eb","font":"'Inter',sans-serif","hero_bg":"#2563eb","card_bg":"#f3f4f6"},
    "glassmorphism": {"bg":"#0f0f23","text":"#ffffff","accent":"#a855f7","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#0f0f23,#1a0533,#0f2333)","card_bg":"rgba(255,255,255,0.05)"},
    "industrial": {"bg":"#e8e4de","text":"#1a1a1a","accent":"#ff6600","font":"'Space Mono',sans-serif","hero_bg":"linear-gradient(135deg,#e8e4de,#d4cfc7)","card_bg":"#f0ece6"},
    "kinetic": {"bg":"#0a0a0a","text":"#ffffff","accent":"#ffdd00","font":"'Inter',sans-serif","hero_bg":"#0a0a0a","card_bg":"#141414"},
    "luxury": {"bg":"#fafaf8","text":"#1a1a1a","accent":"#b8860b","font":"'Playfair Display',serif","hero_bg":"linear-gradient(135deg,#fafaf8,#f0ece6)","card_bg":"#ffffff"},
    "material": {"bg":"#fffbfe","text":"#1c1b1f","accent":"#6750a4","font":"'Roboto',sans-serif","hero_bg":"#fffbfe","card_bg":"#f3edf7"},
    "maximalism": {"bg":"#0a0a0a","text":"#ffffff","accent":"#ff1493","font":"'Space Grotesk',sans-serif","hero_bg":"linear-gradient(135deg,#0a0a0a,#1a0a2e,#2e0a1a)","card_bg":"#1a1a1a"},
    "simple-dark": {"bg":"#0f172a","text":"#e2e8f0","accent":"#f59e0b","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#0f172a,#1e293b)","card_bg":"rgba(255,255,255,0.05)"},
    "modern-dark": {"bg":"#09090b","text":"#fafafa","accent":"#8b5cf6","font":"'Inter',sans-serif","hero_bg":"#09090b","card_bg":"rgba(255,255,255,0.04)"},
    "monochrome": {"bg":"#ffffff","text":"#000000","accent":"#000000","font":"'Playfair Display',serif","hero_bg":"#ffffff","card_bg":"#f5f5f5"},
    "neo-brutalism": {"bg":"#fffdf0","text":"#1a1a1a","accent":"#ff3333","font":"'Space Grotesk',sans-serif","hero_bg":"#fffdf0","card_bg":"#ffffff"},
    "neumorphism": {"bg":"#e0e5ec","text":"#2d3748","accent":"#6366f1","font":"'Inter',sans-serif","hero_bg":"#e0e5ec","card_bg":"#e0e5ec"},
    "newsprint": {"bg":"#f5f0eb","text":"#1a1a1a","accent":"#cc0000","font":"'Playfair Display',serif","hero_bg":"#f5f0eb","card_bg":"#ffffff"},
    "organic-natural": {"bg":"#faf6f0","text":"#2d3b2d","accent":"#8b6f47","font":"'Playfair Display',serif","hero_bg":"linear-gradient(135deg,#faf6f0,#e8dfd4)","card_bg":"#ffffff"},
    "playful-geometric": {"bg":"#ffffff","text":"#1a1a1a","accent":"#ff6b6b","font":"'Nunito',sans-serif","hero_bg":"#ffffff","card_bg":"#fff0f0"},
    "business-style": {"bg":"#faf8f5","text":"#1a1a1a","accent":"#8b6f47","font":"'Playfair Display',serif","hero_bg":"linear-gradient(135deg,#faf8f5,#f0ece6)","card_bg":"#ffffff"},
    "retro": {"bg":"#c0c0c0","text":"#000000","accent":"#000080","font":"'Tahoma',sans-serif","hero_bg":"#c0c0c0","card_bg":"#ffffff"},
    "tech-style": {"bg":"#ffffff","text":"#0f172a","accent":"#2563eb","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#ffffff,#eff6ff)","card_bg":"#f8fafc"},
    "hand-drawn-sketch": {"bg":"#faf8f0","text":"#2d2d2d","accent":"#e85d04","font":"'Patrick Hand',sans-serif","hero_bg":"#faf8f0","card_bg":"#fff8dc"},
    "swiss": {"bg":"#ffffff","text":"#000000","accent":"#ff0000","font":"'Inter',sans-serif","hero_bg":"#ffffff","card_bg":"#f5f5f5"},
    "terminal-cli": {"bg":"#0c0c0c","text":"#00ff41","accent":"#00ff41","font":"'JetBrains Mono',monospace","hero_bg":"#0c0c0c","card_bg":"#111111"},
    "vaporwave": {"bg":"#1a0033","text":"#ff71ce","accent":"#01cdfe","font":"'VT323',monospace","hero_bg":"linear-gradient(180deg,#1a0033,#330066,#1a0033)","card_bg":"rgba(255,113,206,0.08)"},
    "crypto": {"bg":"#0a0a0a","text":"#e0e0e0","accent":"#f7931a","font":"'Inter',sans-serif","hero_bg":"linear-gradient(135deg,#0a0a0a,#1a1000)","card_bg":"rgba(247,147,26,0.05)"},
}

def slugify(name):
    s = name.lower().strip().replace(" / ", "-").replace("/", "-")
    s = re.sub(r'[^a-z0-9\-]', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

def esc(s):
    return html_module.escape(s)

def parse_source_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    prompts = []
    pattern = r'### (\d+)\s*[—–-]\s*(.+?)\n\n```\s*(\w+)\s*\|\s*(\S+)\s*```'
    matches = list(re.finditer(pattern, content))
    for i, m in enumerate(matches):
        num, name, mode, font = int(m.group(1)), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
        start, end = m.end(), matches[i+1].start() if i+1 < len(matches) else len(content)
        section = content[start:end]
        pm = re.search(r'```\n(Design Style:.+?)```', section, re.DOTALL)
        prompt_text = pm.group(1).strip() if pm else ""
        tp = rf'\|\s*{num}\s*\|.*?\|\s*`{mode}`\s*\|\s*`{font}`\s*\|\s*(.+?)\s*\|'
        dm = re.search(tp, content)
        desc = dm.group(1).strip() if dm else ""
        slug = slugify(name)
        cat = "其他"
        for cn, cs in CATEGORIES.items():
            if any(sn.lower() == name.lower() or slugify(sn) == slug for sn in cs):
                cat = cn; break
        prompts.append({"number":num,"name":name,"slug":slug,"mode":mode,"font":font,"description":desc,"prompt":prompt_text,"category":cat})
    return prompts

def get_theme(slug):
    return THEMES.get(slug, {"bg":"#1a1a2e","text":"#e0e0e0","accent":"#6366f1","font":"'Inter',sans-serif","hero_bg":"#1a1a2e","card_bg":"rgba(255,255,255,0.05)"})

def gen_preview(p):
    t = get_theme(p["slug"])
    dk = p["mode"]=="dark"
    bc = 'rgba(255,255,255,0.1)' if dk else 'rgba(0,0,0,0.1)'
    tr = 'rgba(255,255,255,0.1)' if dk else 'rgba(0,0,0,0.05)'
    bb = 'rgba(255,255,255,0.2)' if dk else 'rgba(0,0,0,0.2)'
    cb = 'rgba(255,255,255,0.08)' if dk else 'rgba(0,0,0,0.08)'
    br = '0' if p["slug"] in ['neo-brutalism','swiss','newsprint'] else '8px'
    neo = '3px solid #000;box-shadow:4px 4px 0 #000;' if p["slug"]=='neo-brutalism' else 'none;'
    n = esc(p["name"])

    h = f'''<div class="preview-container" style="background:{t['hero_bg']};color:{t['text']};font-family:{t['font']};border-radius:12px;overflow:hidden;min-height:500px;">
<nav style="display:flex;justify-content:space-between;align-items:center;padding:20px 40px;border-bottom:1px solid {bc};"><div style="font-weight:700;font-size:1.25rem;color:{t['accent']};">{n}</div><div style="display:flex;gap:24px;font-size:0.875rem;opacity:0.7;"><span>Features</span><span>Pricing</span><span>About</span></div></nav>
<div style="padding:80px 40px;text-align:center;">
<div style="display:inline-block;padding:6px 16px;border-radius:20px;font-size:0.75rem;letter-spacing:0.05em;text-transform:uppercase;background:{tr};margin-bottom:24px;border:1px solid {bc};">✦ Design System Preview</div>
<h1 style="font-size:clamp(2rem,5vw,3.5rem);font-weight:800;line-height:1.1;margin:0 0 20px;">Build Something<br>Beautiful Today</h1>
<p style="font-size:1.125rem;opacity:0.7;max-width:500px;margin:0 auto 32px;line-height:1.6;">A complete design system crafted with precision and care for the modern web.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
<button style="padding:12px 28px;border-radius:{br};font-weight:600;font-size:0.95rem;cursor:pointer;background:{t['accent']};color:#fff;border:{neo}">Get Started</button>
<button style="padding:12px 28px;border-radius:{br};font-weight:600;font-size:0.95rem;cursor:pointer;background:transparent;color:{t['text']};border:1px solid {bb};">Learn More</button></div></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid {bc};border-bottom:1px solid {bc};">'''
    for j,(v,l) in enumerate([("10K+","Users"),("99.9%","Uptime"),("50+","Features"),("24/7","Support")]):
        bl = f"border-left:1px solid {bc};" if j>0 else ""
        h += f'<div style="padding:32px 20px;text-align:center;{bl}"><div style="font-size:2rem;font-weight:800;color:{t["accent"]};">{v}</div><div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;opacity:0.6;margin-top:4px;">{l}</div></div>'
    h += f'</div><div style="padding:60px 40px;"><h2 style="text-align:center;font-size:2rem;font-weight:700;margin:0 0 40px;">Core Features</h2><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">'
    for ic,ti,de in [("⚡","Lightning Fast","Optimized for peak performance."),("🛡️","Enterprise Security","Bank-grade encryption built in."),("🎨","Beautiful Design","Pixel-perfect components.")]:
        h += f'<div style="padding:32px 24px;border-radius:12px;background:{t["card_bg"]};border:1px solid {cb};"><div style="font-size:2rem;margin-bottom:16px;">{ic}</div><h3 style="font-size:1.125rem;font-weight:700;margin:0 0 8px;">{ti}</h3><p style="font-size:0.875rem;opacity:0.7;line-height:1.6;margin:0;">{de}</p></div>'
    h += f'</div></div><div style="padding:60px 40px;"><h2 style="text-align:center;font-size:2rem;font-weight:700;margin:0 0 40px;">Pricing</h2><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;max-width:900px;margin:0 auto;">'
    for k,(pn,pr,pf) in enumerate([("Starter","$9",["5 Projects","Basic Analytics","Email Support"]),("Pro","$29",["Unlimited Projects","Advanced Analytics","Priority Support","Custom Domain"]),("Enterprise","$99",["Everything in Pro","SSO & SAML","Dedicated Manager","SLA Guarantee"])]):
        ft = k==1
        bd = f"2px solid {t['accent']}" if ft else f"1px solid {cb}"
        ty = "transform:translateY(-8px);" if ft else ""
        pop = f'<div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:{t["accent"]};margin-bottom:8px;font-weight:700;">Most Popular</div>' if ft else ""
        bg = t['accent'] if ft else 'transparent'
        co = '#fff' if ft else t['text']
        h += f'<div style="padding:32px 24px;border-radius:12px;text-align:center;background:{t["card_bg"]};border:{bd};{ty}">{pop}<h3 style="font-size:1.125rem;font-weight:600;margin:0 0 8px;">{pn}</h3><div style="font-size:2.5rem;font-weight:800;color:{t["accent"]};margin:12px 0;">{pr}<span style="font-size:0.875rem;opacity:0.6;">/mo</span></div><ul style="list-style:none;padding:0;margin:20px 0;text-align:left;">'
        for fi in pf: h += f'<li style="padding:6px 0;font-size:0.875rem;opacity:0.8;">✓ {fi}</li>'
        h += f'</ul><button style="width:100%;padding:10px;border-radius:8px;font-weight:600;cursor:pointer;background:{bg};color:{co};border:1px solid {t["accent"]};">Choose Plan</button></div>'
    h += f'</div></div><footer style="padding:40px;text-align:center;opacity:0.5;font-size:0.8rem;border-top:1px solid rgba(128,128,128,0.2);">© 2024 {n} Design System</footer></div>'
    return h

def gen_detail(p):
    t = get_theme(p["slug"])
    ep = esc(p["prompt"]); pv = gen_preview(p)
    mbb = "#1e293b" if p["mode"]=="dark" else "#f1f5f9"
    mbc = "#e2e8f0" if p["mode"]=="dark" else "#334155"
    fc = {"serif":"#92400e","sans-serif":"#1e40af","mono":"#065f46"}.get(p["font"],"#6b7280")
    fb = {"serif":"#fef3c7","sans-serif":"#dbeafe","mono":"#d1fae5"}.get(p["font"],"#f3f4f6")
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(p["name"])} — Design Prompts Collection</title><link rel="stylesheet" href="../styles.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">
</head><body class="detail-page"><header class="detail-header"><a href="../index.html" class="back-link">← Back to Collection</a>
<div class="detail-title-row"><span class="style-number">#{p["number"]:02d}</span><h1>{esc(p["name"])}</h1></div>
<div class="badge-row"><span class="badge" style="background:{mbb};color:{mbc};">{p["mode"]}</span><span class="badge" style="background:{fb};color:{fc};">{p["font"]}</span><span class="badge cat-badge">{esc(p["category"])}</span></div>
<p class="detail-desc">{esc(p["description"])}</p></header>
<section class="preview-section"><div class="section-label"><span class="label-icon">👁</span> Style Preview</div>{pv}</section>
<section class="prompt-section"><div class="section-label"><span class="label-icon">📋</span> Full Prompt <button class="copy-btn" onclick="copyPrompt()">Copy Prompt</button></div>
<pre class="prompt-block"><code id="prompt-text">{ep}</code></pre></section>
<script>function copyPrompt(){{const t=document.getElementById('prompt-text').textContent;navigator.clipboard.writeText(t).then(()=>{{const b=document.querySelector('.copy-btn');b.textContent='Copied!';b.classList.add('copied');setTimeout(()=>{{b.textContent='Copy Prompt';b.classList.remove('copied');}},2000);}});}}</script></body></html>'''

def gen_index(prompts):
    cards = ""
    for p in prompts:
        t = get_theme(p["slug"])
        cards += f'<a href="prompts/{p["slug"]}.html" class="style-card" data-mode="{p["mode"]}" data-font="{p["font"]}" data-category="{esc(p["category"])}" data-name="{esc(p["name"].lower())}" style="--card-accent:{t["accent"]};"><div class="card-preview" style="background:{t["hero_bg"]};color:{t["text"]};font-family:{t["font"]};"><div class="card-preview-text" style="color:{t["accent"]};">Aa</div></div><div class="card-body"><div class="card-number">#{p["number"]:02d}</div><h3 class="card-title">{esc(p["name"])}</h3><div class="card-badges"><span class="mini-badge mode-{p["mode"]}">{p["mode"]}</span><span class="mini-badge font-{p["font"].replace("-","")}">{p["font"]}</span></div><p class="card-desc">{esc(p["description"][:80])}...</p></div></a>\n'
    cn = '<button class="cat-btn active" data-cat="all" onclick="filterCategory(this)">All Categories</button>\n'
    for c in CATEGORIES: cn += f'<button class="cat-btn" data-cat="{esc(c)}" onclick="filterCategory(this)">{esc(c)}</button>\n'
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Design Prompts Collection — 32 UI Design Style Prompts</title><link rel="stylesheet" href="styles.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
</head><body><div class="hero-section"><div class="hero-content"><div class="hero-badge">✦ 32 Verified Styles</div>
<h1 class="hero-title">Design Prompts<br>Collection</h1>
<p class="hero-subtitle">32 种经过验证的 UI 设计风格提示词，每种都是完整的、可直接复制的 prompt。找到风格 → 复制整段 → 粘贴给 AI → 出图/出代码。</p></div></div>
<div class="controls-section"><div class="search-container"><input type="text" id="searchInput" placeholder="Search styles... (e.g. dark, serif, cyberpunk)" oninput="filterCards()"></div>
<div class="filter-row"><div class="filter-group"><label>Mode:</label><button class="filter-btn active" data-filter="mode" data-value="all" onclick="toggleFilter(this)">All</button><button class="filter-btn" data-filter="mode" data-value="dark" onclick="toggleFilter(this)">🌙 Dark</button><button class="filter-btn" data-filter="mode" data-value="light" onclick="toggleFilter(this)">☀️ Light</button></div>
<div class="filter-group"><label>Font:</label><button class="filter-btn active" data-filter="font" data-value="all" onclick="toggleFilter(this)">All</button><button class="filter-btn" data-filter="font" data-value="serif" onclick="toggleFilter(this)">Serif</button><button class="filter-btn" data-filter="font" data-value="sans-serif" onclick="toggleFilter(this)">Sans-serif</button><button class="filter-btn" data-filter="font" data-value="mono" onclick="toggleFilter(this)">Mono</button></div></div>
<div class="category-row">{cn}</div></div>
<div class="cards-grid" id="cardsGrid">{cards}</div>
<div class="no-results" id="noResults" style="display:none;"><p>No styles match your filters.</p></div>
<footer class="site-footer"><p>Design Prompts Collection — 32 UI Design Style Prompts</p><p class="footer-hint">To add new prompts: edit <code>source_file.md</code> → run <code>python build.py</code></p></footer>
<script>let activeMode='all',activeFont='all',activeCategory='all';
function toggleFilter(b){{const f=b.dataset.filter,v=b.dataset.value;b.parentElement.querySelectorAll('.filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');if(f==='mode')activeMode=v;if(f==='font')activeFont=v;filterCards();}}
function filterCategory(b){{document.querySelectorAll('.cat-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');activeCategory=b.dataset.cat;filterCards();}}
function filterCards(){{const s=document.getElementById('searchInput').value.toLowerCase();let v=0;document.querySelectorAll('.style-card').forEach(c=>{{const mm=activeMode==='all'||c.dataset.mode===activeMode,mf=activeFont==='all'||c.dataset.font===activeFont,mc=activeCategory==='all'||c.dataset.category===activeCategory,ms=!s||c.dataset.name.includes(s)||c.dataset.mode.includes(s)||c.dataset.font.includes(s);if(mm&&mf&&mc&&ms){{c.style.display='';v++;}}else c.style.display='none';}});document.getElementById('noResults').style.display=v===0?'block':'none';}}</script></body></html>'''

def gen_css():
    return ''':root{--bg:#0a0a0f;--surface:#12121a;--surface-2:#1a1a28;--text:#e8e8f0;--text-muted:#8888a0;--accent:#6366f1;--accent-soft:rgba(99,102,241,0.15);--border:rgba(255,255,255,0.08);--radius:12px;--font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;--mono:'JetBrains Mono','Fira Code',monospace;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased;}
.hero-section{padding:80px 24px 40px;text-align:center;background:linear-gradient(180deg,rgba(99,102,241,0.08) 0%,transparent 100%);}
.hero-badge{display:inline-block;padding:6px 16px;border-radius:20px;font-size:0.8rem;letter-spacing:0.05em;background:var(--accent-soft);color:var(--accent);border:1px solid rgba(99,102,241,0.2);margin-bottom:20px;}
.hero-title{font-size:clamp(2.5rem,6vw,4.5rem);font-weight:800;line-height:1.1;margin-bottom:16px;background:linear-gradient(135deg,#fff 30%,var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero-subtitle{font-size:1.1rem;color:var(--text-muted);max-width:600px;margin:0 auto;line-height:1.8;}
.controls-section{padding:0 24px 24px;max-width:1200px;margin:0 auto;}
.search-container{margin-bottom:16px;}
#searchInput{width:100%;padding:14px 20px;border-radius:var(--radius);border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:1rem;font-family:var(--font);outline:none;transition:border-color 0.2s;}
#searchInput:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft);}
#searchInput::placeholder{color:var(--text-muted);}
.filter-row{display:flex;gap:24px;margin-bottom:12px;flex-wrap:wrap;}
.filter-group{display:flex;align-items:center;gap:8px;}
.filter-group label{font-size:0.8rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;}
.filter-btn{padding:6px 14px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text-muted);font-size:0.85rem;cursor:pointer;transition:all 0.2s;font-family:var(--font);}
.filter-btn:hover{border-color:var(--accent);color:var(--text);}
.filter-btn.active{background:var(--accent);color:#fff;border-color:var(--accent);}
.category-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;}
.cat-btn{padding:6px 14px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--text-muted);font-size:0.8rem;cursor:pointer;transition:all 0.2s;font-family:var(--font);}
.cat-btn:hover{border-color:var(--accent);color:var(--text);}
.cat-btn.active{background:var(--accent-soft);color:var(--accent);border-color:rgba(99,102,241,0.3);}
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;padding:24px;max-width:1200px;margin:0 auto;}
.style-card{border-radius:var(--radius);border:1px solid var(--border);background:var(--surface);overflow:hidden;text-decoration:none;color:inherit;transition:all 0.25s ease;display:flex;flex-direction:column;}
.style-card:hover{border-color:var(--card-accent,var(--accent));transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,0,0,0.4);}
.card-preview{height:120px;display:flex;align-items:center;justify-content:center;overflow:hidden;}
.card-preview-text{font-size:3rem;font-weight:900;opacity:0.6;}
.card-body{padding:16px 20px 20px;}
.card-number{font-family:var(--mono);font-size:0.75rem;color:var(--text-muted);margin-bottom:4px;}
.card-title{font-size:1.15rem;font-weight:700;margin-bottom:8px;}
.card-badges{display:flex;gap:6px;margin-bottom:8px;}
.mini-badge{padding:2px 8px;border-radius:4px;font-size:0.7rem;font-weight:500;}
.mode-dark{background:#1e293b;color:#94a3b8;}
.mode-light{background:#f1f5f9;color:#475569;}
.font-serif{background:#fef3c7;color:#92400e;}
.font-sansserif{background:#dbeafe;color:#1e40af;}
.font-mono{background:#d1fae5;color:#065f46;}
.card-desc{font-size:0.8rem;color:var(--text-muted);line-height:1.5;}
.no-results{text-align:center;padding:60px 24px;color:var(--text-muted);}
.site-footer{text-align:center;padding:48px 24px;color:var(--text-muted);font-size:0.85rem;border-top:1px solid var(--border);margin-top:48px;}
.footer-hint{margin-top:8px;font-size:0.75rem;opacity:0.6;}
.footer-hint code{font-family:var(--mono);background:var(--surface-2);padding:2px 6px;border-radius:4px;}
.detail-page{max-width:960px;margin:0 auto;padding:24px;}
.detail-header{padding:40px 0 32px;border-bottom:1px solid var(--border);margin-bottom:32px;}
.back-link{display:inline-block;color:var(--accent);text-decoration:none;font-size:0.9rem;margin-bottom:20px;transition:opacity 0.2s;}
.back-link:hover{opacity:0.7;}
.detail-title-row{display:flex;align-items:baseline;gap:16px;margin-bottom:12px;}
.style-number{font-family:var(--mono);font-size:1.2rem;color:var(--text-muted);}
.detail-title-row h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;}
.badge-row{display:flex;gap:8px;margin-bottom:12px;}
.badge{padding:4px 12px;border-radius:6px;font-size:0.8rem;font-weight:500;}
.cat-badge{background:var(--accent-soft);color:var(--accent);}
.detail-desc{color:var(--text-muted);font-size:1rem;line-height:1.6;}
.preview-section{margin-bottom:40px;}
.section-label{display:flex;align-items:center;gap:8px;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);margin-bottom:16px;}
.label-icon{font-size:1.1rem;}
.preview-container{border:1px solid var(--border);}
.prompt-section{margin-bottom:48px;}
.copy-btn{margin-left:auto;padding:6px 16px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:0.8rem;cursor:pointer;transition:all 0.2s;font-family:var(--font);}
.copy-btn:hover{background:var(--accent);color:#fff;border-color:var(--accent);}
.copy-btn.copied{background:#10b981;border-color:#10b981;color:#fff;}
.prompt-block{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;overflow-x:auto;font-family:var(--mono);font-size:0.85rem;line-height:1.7;white-space:pre-wrap;word-break:break-word;max-height:600px;overflow-y:auto;}
.prompt-block code{font-family:inherit;color:var(--text);}
@media(max-width:768px){.cards-grid{grid-template-columns:1fr;}.filter-row{flex-direction:column;gap:12px;}}
::-webkit-scrollbar{width:8px;height:8px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--surface-2);border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:var(--text-muted);}'''

def build():
    print("Building Design Prompts Collection site...")
    prompts = parse_source_file(SOURCE_FILE)
    print(f"  Parsed {len(prompts)} prompts")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "styles.css"), 'w', encoding='utf-8') as f:
        f.write(gen_css())
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(gen_index(prompts))
    for p in prompts:
        with open(os.path.join(PROMPTS_DIR, f"{p['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(gen_detail(p))
    print(f"  Generated {len(prompts)} prompt pages in site/prompts/")
    print(f"Done! Open site/index.html")

if __name__ == "__main__":
    build()