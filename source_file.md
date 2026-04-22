# AI Design Style Prompts — 32 种 UI 设计风格提示词完整版

## 这个仓库是什么

你想让 AI 帮你做一个「瑞士风」「赛博朋克」「学院风」的网页，但不知道怎么把风格翻译成 prompt？

这个仓库就是现成的**风格→提示词词典**。32 种经过验证的 UI 设计风格，每种都是一段**完整的、可直接复制的 prompt**，包含：

- 风格定义（模式、字体、视觉语言）
- 11 个页面区块的具体布局指导（Hero → Stats → Features → Pricing → FAQ → Footer...）

**怎么用：** 找到你想要的风格 → 复制整段 prompt → 粘贴给 AI → 出图/出代码。

---

## 适合谁用

- 用 AI 做前端但总是出来「模板感」的人
- 想快速切换设计风格做 A/B 对比的人
- 给设计师或 AI Agent 写 brief 时缺乏「风格语言」的人
- 用 Claude Code / Cursor / v0 / Bolt 做 UI 的 builder

---

## 风格速查表

| # | 风格 | 模式 | 字体 | 一句话描述 |
|---|------|------|------|------------|
| 1 | [Academia](#1--academia) | `dark` | `serif` | University aesthetic, old libraries, warm paper textures, tr... |
| 2 | [Art Deco](#2--art-deco) | `dark` | `serif` | 1920s Gatsby elegance, geometric precision, metallic gold ac... |
| 3 | [Aurora Mesh](#3--aurora-mesh) | `dark` | `sans-serif` | Flowing mesh gradients, aurora effects, vibrant color transi... |
| 4 | [Bauhaus](#4--bauhaus) | `light` | `sans-serif` | Bold geometric modernism with circles, squares, and triangle... |
| 5 | [Bold Typography](#5--bold-typography) | `dark` | `sans-serif` | Type-driven design that treats massive typography as the pri... |
| 6 | [Botanical / Organic Serif](#6--botanical-organic-serif) | `light` | `serif` | Soft, earthy, elegant design inspired by nature. Features or... |
| 7 | [Clay](#7--clay) | `light` | `sans-serif` | A hyper-realistic 3D aesthetic simulating soft, inflatable c... |
| 8 | [Cyberpunk](#8--cyberpunk) | `dark` | `mono` | High contrast neon on black, glitch animations, terminal/mon... |
| 9 | [Corporate Trust](#9--corporate-trust) | `light` | `sans-serif` | Modern SaaS aesthetic balancing professionalism with approac... |
| 10 | [Flat Design](#10--flat-design) | `light` | `sans-serif` | A design philosophy centered on removing depth cues (shadows... |
| 11 | [Glassmorphism](#11--glassmorphism) | `dark` | `sans-serif` | Apple-inspired aesthetic with rich mesh gradients, premium b... |
| 12 | [Industrial](#12--industrial) | `light` | `sans-serif` | A high-fidelity industrial skeuomorphism aesthetic inspired ... |
| 13 | [Kinetic](#13--kinetic) | `dark` | `sans-serif` | Motion-first design where typography is the primary visual m... |
| 14 | [Luxury](#14--luxury) | `light` | `serif` | Elegant serif typography with monochromatic palette and gold... |
| 15 | [Material](#15--material) | `light` | `sans-serif` | Playful, dynamic color extraction, pill-shaped buttons, and ... |
| 16 | [Maximalism](#16--maximalism) | `dark` | `sans-serif` | Clashing patterns, dense layouts, oversaturated colors, inte... |
| 17 | [Simple Dark](#17--simple-dark) | `dark` | `sans-serif` | An atmospheric dark mode design system built on deep slate t... |
| 18 | [Modern Dark](#18--modern-dark) | `dark` | `sans-serif` | A cinematic, high-precision dark mode design featuring layer... |
| 19 | [Monochrome](#19--monochrome) | `light` | `serif` | A stark, editorial design system built on pure black and whi... |
| 20 | [Neo-brutalism](#20--neo-brutalism) | `light` | `sans-serif` | A raw, high-contrast aesthetic that mimics print design and ... |
| 21 | [Neumorphism](#21--neumorphism) | `light` | `sans-serif` | Extruded and inset elements via dual shadows on monochromati... |
| 22 | [Newsprint](#22--newsprint) | `light` | `serif` | Stark black and white, high contrast, tight grids, newspaper... |
| 23 | [Organic / Natural](#23--organic-natural) | `light` | `serif` | Earth-inspired palette with moss greens, terracotta, and san... |
| 24 | [Playful Geometric](#24--playful-geometric) | `light` | `sans-serif` | A vibrant, high-energy aesthetic that combines a stable stru... |
| 25 | [Business Style](#25--business-style) | `light` | `serif` | An editorial-inspired minimalist design system centered on e... |
| 26 | [Retro](#26--retro) | `light` | `sans-serif` | Ugly-cool 90s nostalgia aesthetic with Windows 95 beveled UI... |
| 27 | [Tech Style](#27--tech-style) | `light` | `sans-serif` | A bold, minimalist-modern visual system combining clean aest... |
| 28 | [Hand-Drawn / Sketch](#28--hand-drawn-sketch) | `light` | `sans-serif` | Organic wobbly borders, handwritten typography, paper textur... |
| 29 | [Swiss](#29--swiss) | `light` | `sans-serif` | A rigorous implementation of the International Typographic S... |
| 30 | [Terminal CLI](#30--terminal-cli) | `dark` | `mono` | A raw, functional, and retro-futuristic command-line interfa... |
| 31 | [Vaporwave](#31--vaporwave) | `dark` | `mono` | A nostalgic, neon-drenched journey into 80s retro-futurism. ... |
| 32 | [Crypto](#32--crypto) | `dark` | `sans-serif` | A bold, futuristic aesthetic inspired by Bitcoin and decentr... |

---

## 风格分类导航

**科技 / SaaS / 金融：** `SaaS` `Modern Dark` `Simple Dark` `Corporate Trust` `Material` `Crypto` `Terminal CLI` `Flat Design` `Aurora Mesh`

**编辑 / 排版 / 机构感：** `Monochrome` `Swiss` `Newsprint` `Academia` `Luxury` `Bold Typography` `Business Style`

**强风格 / 强情绪 / 年轻化：** `Clay` `Playful Geometric` `Kinetic` `Maximalism` `Retro` `Vaporwave` `Neo-brutalism`

**物理质感 / 设计史：** `Bauhaus` `Art Deco` `Industrial` `Neumorphism` `Botanical` `Organic` `Sketch` `Cyberpunk` `Glassmorphism`

---

## 完整风格提示词

> 每个风格是一段完整的 prompt，直接复制整段喂给 AI 即可。

### 1 — Academia

``` dark | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Academia
Mode: dark | Font: serif

University aesthetic, old libraries, warm paper textures, traditional serifs, gold/crimson accents.

--- Layout by Section ---

[Hero]
Asymmetric two-column layout (7/5 split) with ornate decorative corner flourishes. Left column contains brass accent line with establishment date, large serif headline with first word highlighted in brass, drop-cap paragraph, and dual CTAs. Right column features arch-topped sepia image with brass border overlay.

[Stats]
Full-width horizontal band with four equal columns separated by vertical borders. Each stat features large brass numbers in Cinzel, small uppercase labels, and subtle hover interactions that scale numbers and change background opacity.

[Product Detail]
Centered content within ornate frame. Brass horizontal lines flanking 'Proclamation' label, large serif headline, ornate divider, and multi-paragraph body text with drop cap on first paragraph.

[Features]
Three-column grid of cards with corner flourishes. Each card has circular icon container with brass border, Roman numeral label in Cinzel, serif heading, and body text. Cards lift on hover with brass border tint.

[Benefits]
Three-column grid with gradient dividers above each item. Roman numeral labels, serif headings, and body text. Dividers animate from wood-grain to full brass on hover.

[How It Works]
Alternating timeline layout with vertical brass connector line and medallions. Content alternates left/right with Roman numeral medallions centered. Each step features serif heading and description.

[Pricing]
Three-column card layout with highlighted tier featuring brass border and ring. Wax seal badges on featured plans positioned at top-right. Cards include tier name, large price in Cormorant, feature list with check icons, and CTA button.

[Testimonials]
Two-column grid of testimonial blocks. Each features large decorative quote mark, 5-star rating, serif quote text in italic, circular avatar image with sepia filter, author name in Cinzel, and role.

[FAQ]
Accordion with border dividers. Each item has Roman numeral prefix, serif question, and brass-bordered toggle button that rotates on open. Mobile-optimized with larger touch targets (48px min-height).

[Blog]
Three-column grid of article cards. Each card has arch-topped sepia image that scales on hover, metadata row with date and author separated by divider, and serif headline that transitions to brass on hover.

[Footer]
CTA section with two-column split (headline/email signup), ornate divider separator, then three-column footer with logo, copyright, and social links in uppercase Cinzel.
```

</details>

---

### 2 — Art Deco

``` dark | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Art Deco
Mode: dark | Font: serif

1920s Gatsby elegance, geometric precision, metallic gold accents, architectural symmetry, luxury heritage

--- Layout by Section ---

[Hero]
Centered symmetrical composition with massive uppercase serif headline. Radial sunburst gradient emanates from center. Vertical gold line divider adds architectural height. CTAs arranged horizontally with sharp borders and glow effects.

[Stats]
Four-column grid with bordered boxes featuring stepped corner decorations. Large gold numbers with uppercase labels. Subtle hover state intensifies gold borders.

[Product Detail]
Centered heading with two-column text layout below. Left-border accent on paragraphs. Contained in darker card background for depth separation.

[Features]
Three-column responsive grid. Cards feature rotated diamond icon containers, corner decorative elements, and lift-on-hover micro-interaction. Icons rotate back on hover for theatrical effect.

[Blog]
Three-column grid. Images with double-frame treatment (outer border + inner inset border). Grayscale images with gold overlay on hover. Film noir aesthetic with high contrast typography.

[How It Works]
Vertical timeline with central gold divider line. Diamond-shaped step markers with Roman numerals. Alternating left-right text layout creates visual rhythm. Steps use geometric precision.

[Benefits]
Two-column grid with large bordered cards. Corner flourishes (top-left, bottom-right). Rotated diamond checkmarks. Background darkens slightly on hover for depth.

[Testimonials]
Three-column grid. Giant quotation mark watermark in background. Rotated diamond avatar frames with counter-rotated images. Author details with role in gold.

[Pricing]
Three columns with center tier elevated and highlighted. Gold badge floats above popular plan. Feature lists with gold checkmarks. Sharp geometric borders throughout.

[FAQ]
Clean accordion with full-width questions. Chevron indicators. Expanded answers show left gold border accent. Smooth height transitions.

[Footer]
Five-column grid (company spans wider on mobile). Large uppercase serif brand. Gold headings with muted link text. Border separator above social icons.
```

</details>

---

### 3 — Aurora Mesh

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Aurora Mesh
Mode: dark | Font: sans-serif

Flowing mesh gradients, aurora effects, vibrant color transitions, modern startup aesthetic inspired by Stripe and Vercel

--- Layout by Section ---

[Hero]
Full-height hero with animated mesh gradient background. Split layout with headline left (massive typography with gradient text fill), floating 3D-ish card mockup right with aurora glow underneath. CTAs have pill shapes with gradient borders.

[Stats]
Horizontal strip with glass-morphic stat cards floating over a subtle aurora wave. Each stat has a glowing accent bar on top indicating its category color.

[Features]
Asymmetric bento grid with varying card sizes. Cards have dark glass backgrounds with colored gradient borders that pulse subtly. Icons sit in gradient orbs.

[How It Works]
Vertical timeline with a glowing gradient line connecting steps. Each step card has a mesh gradient corner accent. Numbers are oversized with gradient fills.

[Benefits]
Two-column layout with benefit cards stacked. Each card has an aurora streak across the top edge. Checkmark icons with gradient fills.

[Pricing]
Three cards with the featured card elevated and wrapped in an animated gradient border. Background has slow-moving mesh gradient. Prices use gradient text.

[Testimonials]
Carousel or masonry of quote cards with avatar images having gradient ring borders. Quote marks are oversized with aurora gradient fills.

[FAQ]
Accordion style with gradient accent lines on the left. Expanded items reveal answers with a soft glow effect. Plus/minus icons have gradient treatment.

[Blog]
Horizontal scrolling cards with image overlays featuring gradient mesh filters. Date badges have pill shapes with gradient backgrounds.

[Footer]
Dark base with subtle aurora waves at the top edge. Links organized in columns with gradient hover underlines. Social icons in gradient orbs.
```

</details>

---

### 4 — Bauhaus

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Bauhaus
Mode: light | Font: sans-serif

Bold geometric modernism with circles, squares, and triangles. Primary color palette (Red/Blue/Yellow) with stark black borders and hard shadows. Functional yet artistic with constructivist asymmetry.

--- Layout by Section ---

[Hero]
Split-screen layout (50/50) with text on white background and geometric composition on blue. Massive uppercase typography with colored accent border on left.

[Stats]
Equal-width grid with dividers. Each stat has geometric shape icon (circle/square/diamond) numbered 1-4. Yellow background section with white cards.

[Features]
Three-column grid with lifted cards featuring corner decorations (circle/triangle/square). Each card has geometric icon in bordered container. Hover lift effect.

[How It Works]
Horizontal timeline with thick connecting line (desktop only). Steps use alternating geometric shapes (circle/square/rotated square) as numbers. Two-column grid on mobile.

[Benefits]
Grid of white cards on red background. Each card has circular yellow icon with checkmark. Clean borders and hard shadows.

[Pricing]
Three-column layout with center tier elevated and highlighted with yellow background. All tiers have geometric headers and square bullet points.

[Testimonials]
Three-column grid with cards featuring circular avatar cutouts positioned above card. Quote icon and bordered sections. Decorative corner elements.

[FAQ]
Accordion with thick borders. Active items have red background with white text. Inactive items are white. Yellow background for expanded content.

[Blog]
Three-column grid on blue background with white cards. Images alternate between circular and square masks. Grayscale images with color on hover.

[Footer]
Dark background (near-black #121212) with geometric logo. Multi-column layout with social icons as bordered squares. Minimalist link hover states.
```

</details>

---

### 5 — Bold Typography

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Bold Typography
Mode: dark | Font: sans-serif

Type-driven design that treats massive typography as the primary visual element. Ultra-large headlines, extreme contrast, and dramatic negative space create poster-like compositions where words become art.

--- Layout by Section ---

[Hero]
Full-viewport hero with massive H1 (text-4xl to text-8xl responsive) occupying 60%+ of viewport. Stacked layout with headline, subhead, CTAs in strict vertical rhythm. Decorative oversized number in background (hidden on mobile). Typography IS the hero.

[Stats]
Responsive grid (1 col mobile, 2 cols tablet, 4 cols desktop) with huge numbers (text-4xl to text-7xl) and tiny all-caps labels. Numbers in accent color for dramatic pop. Elevated background for section depth.

[Product Detail]
Asymmetric two-column grid (1.2fr / 0.8fr). Left: headline + multi-paragraph description with max-width constraint. Right: typographic card with grade display (A+) featuring layered text shadow for depth and accent top border.

[Features]
Responsive grid (1-2-3 columns) with gap-px border separator technique. Each feature card has icon, title, description. Hover state changes background. Compact on mobile (p-6) expanding to spacious on desktop (p-8).

[Blog]
Magazine-style responsive grid (1-2-3 columns). Each post has image with subtle hover scale, metadata in monospace, oversized titles that change color on hover. Featured badge on first post.

[How It Works]
Vertical stepped list with massive step numbers (text-6xl to text-8xl) in border color that transitions to accent on hover. Three-column grid on desktop (number | title | description) collapses to stacked on mobile.

[Benefits]
Two-column layout (header left, list right on desktop, stacked mobile). Each benefit has oversized accent number + title/description. Generous spacing between items.

[Testimonials]
Responsive grid (1-2-3 columns) with bordered cards. Large display serif quote mark (text-5xl to text-6xl), italic quote in Playfair Display, grayscale avatar, compact author info.

[Pricing]
Responsive grid (1-2-3 pricing tiers). Price as dominant element (text-4xl to text-6xl). Highlighted tier uses 2px accent border. Compact feature lists with small checkmarks. Full-width CTA button at bottom.

[FAQ]
Centered single column with accordion items. Bold questions (text-lg to text-2xl) that change color on hover. Smooth height/opacity animation for answers with max-width for readability.

[Final CTA]
Inverted section (foreground bg, background text) with centered content. Responsive headline sizing. Email input + subscribe button in flex row on tablet+, stacked on mobile. Decorative brand name in background (hidden on mobile).

[Footer]
Minimal footer with responsive 2-4-5 column grid. Company info spans 2 columns on mobile. Compact text sizing (text-xs to text-sm). Bottom row has copyright + social icons with horizontal rule separator.
```

</details>

---

### 6 — Botanical / Organic Serif

``` light | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Botanical / Organic Serif
Mode: light | Font: serif

Soft, earthy, elegant design inspired by nature. Features organic shapes, generous rounded corners, paper grain texture, muted earth tones, and sophisticated serif typography that breathes warmth and natural luxury.

--- Layout by Section ---

[Hero]
Split two-column layout with massive serif typography on left and arched image (200px top radius) on right. Decorative botanical icons float in corners. Quote overlay on image.

[Stats]
Horizontal band with subtle sage background and border. Large serif numbers paired with uppercase sans-serif labels in grid.

[Features]
Three-column grid with staggered vertical offsets (translate-y-12 on middle card). Soft rounded cards with botanical icons in muted circles.

[How It Works]
Dark forest green background with three-step grid. Dotted SVG connecting path. Steps in translucent cards with numbered terracotta badges.

[Benefits]
Alternating zig-zag layout with organic blob-shaped image backgrounds (rotate transform). Checkmark bullets in terracotta circles.

[Pricing]
Three-column grid with center card elevated and scaled. Dark background for highlighted plan with terracotta badge. Pill-shaped buttons.

[Testimonials]
Three-column grid on soft clay background with radial dot pattern overlay. Large quotation marks, circular avatars, serif quotes.

[FAQ]
Centered accordion with rounded items. Smooth expand/collapse animations. Active items get white background and shadow.

[Blog]
Three-column grid with tall aspect-ratio images (3:4) in organic rounded containers (32px radius). Hover lifts cards with scale effect on images.

[Footer]
Rounded top edge (60px radius), dark moss background. Four-column grid for nav links with social icons.
```

</details>

---

### 7 — Clay

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Clay
Mode: light | Font: sans-serif

A hyper-realistic 3D aesthetic simulating soft, inflatable clay objects with multi-layered shadow stacks, vibrant candy-store colors, tactile micro-interactions, and organic floating ambient elements that create a premium, playful digital toy experience.

--- Layout by Section ---

[Hero]
Centered content with massive, progressively scaled typography (text-5xl to text-8xl). Background features large, slowly drifting colored blobs with blur-3xl. Floating 3D shapes orbit the headline with clay-float-slow animation. Trust badge with animated pulse indicator. Gradient text with multi-color stops for headline accent.

[Stats]
Grid of breathing spheres (clay-orb + clay-breathe) with aspect-square ratio. Numbers use Nunito Black in large sizes. Staggered animation delays create organic rhythm. Hover scale transforms provide tactile feedback.

[Features]
Masonry Bento grid with col-span-2/row-span-2 hero card. Varying background opacity creates depth hierarchy. Internal decorative panels positioned absolutely at card bottom with translate-y hover reveals. Icon containers use vibrant gradient backgrounds with rounded-2xl shapes.

[How It Works]
Three-column grid with centered content. Connecting horizontal 'pipe' element (rounded-full bg with shadow-inner). Each step uses large gradient circles (h-28 to h-32 responsive) with bold Nunito numbers. Group-hover scale interactions.

[Benefits]
50/50 split layout. Left: Abstract clay composition with nested rounded shapes, layered backgrounds (aspect-square container). Right: Stacked benefit cards (rounded-[24px]) with gradient check icons, hover lift and enhanced shadow.

[Pricing]
Three-column grid. Center 'popular' card scales to 110% on desktop only (md:scale-110) with enhanced shadow. All cards use consistent rounded-[32px] radius with responsive padding. Chunky check icons in green tones.

[Testimonials]
2-3 column responsive grid. Cards use white backgrounds with shadow-clayCard. Avatars wrapped in white clay rings (shadow-clayButton). Five-star ratings in amber. Group hover lifts cards with enhanced shadows.

[FAQ]
Accordion using native details/summary elements. Cards have rounded-[24px] radius with shadow-clayCard. Open state reveals recessed inset shadow. Summary includes animated rotate-180 chevron indicator.

[Blog]
Polaroid-style cards with rounded-[32px] outer and rounded-[24px] image containers. Thick padding creates photo border effect. Images scale on group-hover. Metadata uses small caps with clay pill badges.

[Footer]
Glass-morphic base (bg-white/40 + backdrop-blur-lg). Social icons as clay buttons (rounded-xl with shadow-clayButton). Hover translates up with shadow enhancement. Grid layout with company info spanning 2 columns.
```

</details>

---

### 8 — Cyberpunk

``` dark | mono```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Cyberpunk
Mode: dark | Font: mono

High contrast neon on black, glitch animations, terminal/monospace fonts, tech-oriented decorations. A dystopian digital aesthetic inspired by 80s sci-fi and hacker culture.

--- Layout by Section ---

[Hero]
Full-bleed dark canvas with massive glitched headline (text-5xl to text-8xl) featuring chromatic aberration and neon glow shadows. Asymmetric 60/40 split with terminal-style subheadline with typing cursor on left, holographic HUD display with animated panels on right. Grid background with radial gradient mask. Scanline overlay across entire page.

[Stats]
Horizontal 2x2 grid on mobile, 4-column on desktop. Each stat in bordered section with monospace labels, large display numbers, and upward trend indicators. Subtle background glow. Border separators between stats.

[Product Details]
Centered holographic card with circuit grid background. Terminal-style label, large heading, and paragraphs prefixed with >> symbols. Authenticated session indicator at bottom with pulsing dot.

[Features]
Three-column grid (stacks on mobile) with chamfered corner cards. Icon in bordered square that transitions to accent background on hover. Card titles change color on hover. Radial gradient background accent. Section header with overline label and gradient accent bars.

[Blog]
Three-column grid of terminal-style cards with VHS scanline overlay on images. Stream ID badges on images. ISO date format, author name, and access link with arrow. Entire card lifts on hover with border glow.

[How It Works]
Vertical timeline with center line. Diamond-shaped step markers (rotated squares) with neon glow. Steps alternate left/right on desktop, stack left on mobile. Terminal-style step numbers (STEP_01, etc).

[Benefits]
Two-column split - left has list of benefits with checkboxes that fill on hover, right has full syntax-highlighted code editor mockup with terminal window chrome (traffic lights), line numbers, and blinking cursor.

[Testimonials]
2x2 grid of cards with terminal headers showing avatar (with tech pattern), author info, and VERIFIED badge. Quote with decorative quotation marks. Transmission complete footer with pulsing indicator.

[Pricing]
Three-column grid with center card scaled and highlighted with thicker accent border and neon glow. Cards show tier name, price in large monospace, feature list with checkmarks, and CTA button. Recommended badge on highlighted tier.

[FAQ]
Vertical stack of chamfered accordion items. Questions prefixed with $ symbol. Collapsible answers with dashed border separator, prefixed with >. Animated expand/collapse with rotating arrow.

[Footer]
Four-column grid (stacks on mobile). Company info, navigation links with underline hover, social icons, copyright. Links styled as terminal commands. Monospace font throughout.
```

</details>

---

### 9 — Corporate Trust

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Corporate Trust
Mode: light | Font: sans-serif

Modern SaaS aesthetic balancing professionalism with approachability. Vibrant indigo/violet gradients, soft colored shadows, isometric depth, and clean geometric sans-serif typography.

--- Layout by Section ---

[Hero]
Split layout with 60/40 composition. Left: Gradient headline split, dual-CTA buttons, trust indicator. Right: Isometric floating card with subtle 3D transforms and decorative elements.

[Stats]
Clean horizontal strip with large bold numbers, subtle text. Bordered top/bottom to create visual break.

[Product Detail]
Two-column layout with text-left, visual-right. Abstract UI mockup inside gradient container with offset shadow element.

[Features]
Zig-zag alternating layout. Icon badges with soft backgrounds, feature cards with isometric perspective transforms, decorative gradient blobs.

[Blog]
Three-column card grid. Image-first design with gradient overlays on hover, metadata above headline.

[How It Works]
Horizontal step timeline with connecting gradient line. Numbered badges with glow effects on dark background.

[Benefits]
Two-column split: checklist items on left, isometric 3D card visualization on right with gradient background.

[Pricing]
Three-column grid with center card elevated and highlighted. Relative positioning badge for 'Most Popular'.

[Testimonials]
Three-column card grid with star ratings, quotes, and user avatars with ring styling.

[FAQ]
Accordion with details/summary HTML. Chevron rotation on expand, subtle background wash on open state.

[Footer]
Four-column grid on desktop, stacked on mobile. Dark slate background with lighter link hover states.
```

</details>

---

### 10 — Flat Design

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Flat Design
Mode: light | Font: sans-serif

A design philosophy centered on removing depth cues (shadows, bevels, gradients) in favor of pure color, typography, and layout. Crisp, two-dimensional, and geometric with bold color blocking.

--- Layout by Section ---

[Hero]
Full-width bold color block background (Primary Blue). Large decorative geometric shapes as background elements. Left-aligned text with massive headline (4xl to 8xl responsive). High-contrast CTA buttons with strong hover states. Right side features abstract geometric composition with overlapping shapes.

[Stats]
Clean 4-column grid with gradient background accent. Large colorful numbers (5xl-6xl) in varied accent colors. Uppercase labels. Hover scale effects on individual stats.

[Features]
3-column grid with section title. Each feature card has distinct soft background color (blue-50, green-50, amber-50, etc.) with white icon circles. Strong hover states with scale and color intensification.

[How It Works]
Dark background (gray-900) for contrast. Horizontal step circles connected by background line. Large numbered circles in primary blue with border. Clean white text on dark.

[Benefits]
50/50 split screen layout. Left side emerald green solid with white text and bullet points. Right side white with abstract geometric overlapping shapes in mix-blend-multiply mode.

[Pricing]
3-column grid. Popular tier is scaled and uses primary blue block. Other tiers use light gray blocks. 'Most Popular' badge on featured tier. All cards have strong hover scale effects.

[Testimonials]
Masonry columns layout. White cards on light gray background. Large decorative quote mark. Avatar circles with bold typography.

[FAQ]
Centered accordion with thick (2px) borders. Plus/Minus icons with bold stroke weight. Clean expansion with no background change.

[Blog]
3-column grid on light gray background. White cards with image top (rounded corners). Strong hover state with image scale. Bold date, title, and 'Read Article' CTA.

[Footer]
Dark gray-900 background. Logo with colored square. Multiple column layout with primary blue section titles. Circular social icons.
```

</details>

---

### 11 — Glassmorphism

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Glassmorphism
Mode: dark | Font: sans-serif

Apple-inspired aesthetic with rich mesh gradients, premium blur, and constrained layouts.
```

</details>

---

### 12 — Industrial

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Industrial
Mode: light | Font: sans-serif

A high-fidelity industrial skeuomorphism aesthetic inspired by Dieter Rams and Teenage Engineering. Features tactile neumorphic elements, matte plastic surfaces, and safety-orange accents. Every component mimics physical hardware with realistic lighting, mechanical interactions, and manufacturing details like screws, vents, and LED indicators.

--- Layout by Section ---

[Hero]
Asymmetric split layout with control panel interface (text/CTAs) on left, and massive interactive 'Device' visualization on right featuring bezels, CRT-style scanlines, power indicators, and physical hardware buttons.

[Stats]
Full-width dark LED readout strip with inset shadow depth, resembling a digital dashboard display. Glowing monospace numbers with color-coded shadows.

[Features]
3-column grid of ventilated hardware modules. Each card has corner screws (CSS gradients), vent slots, recessed icon housings, and hover elevation effects.

[How It Works]
Horizontal process flow with large circular neumorphic step indicators connected by physical cylindrical pipes (3D shadow effect).

[Benefits]
Split-panel control board with dark technical background. Left side has checklist with tactile toggle switches, right side features radar/sonar screen visualization with animated sweep.

[Pricing]
Metal dog-tag style cards with hanging holes at top. Center card elevated with accent ring. Monospace pricing and recessed checkmark icons.

[Testimonials]
Rotated paper note cards pinned to surface with red push-pins. Grayscale avatars and serif quote typography for authenticity.

[FAQ]
Neumorphic accordion drawers with recessed arrow indicators that rotate on open. Inset content areas with subtle inner shadow.

[Blog]
Field log/cassette tape cards with label badges. Grayscale images that colorize on hover, overlaid gradient masks for depth.

[Footer]
Industrial base plate with online status LED, embossed copyright text, and minimal social icon grid with lift-on-hover.
```

</details>

---

### 13 — Kinetic

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Kinetic
Mode: dark | Font: sans-serif

Motion-first design where typography is the primary visual medium. Features infinite marquees, viewport-scaled text, scroll-triggered animations, and aggressive uppercase styling. High contrast, brutalist energy with rhythmic movement.

--- Layout by Section ---

[Hero]
Full viewport height (90vh) with massive text using clamp() for responsive scaling (clamp(3rem,12vw,14rem)). Split headlines across lines with contrasting accent color. Add scroll-triggered scale (1.0→1.2) and opacity (1.0→0) transforms via Framer Motion. Center content with max-w-[95vw].

[Stats]
Infinite horizontal marquee on full-width accent background (py-8). Display huge numbers (6xl-8xl) paired with uppercase labels and decorative symbols (✦). Use react-fast-marquee with speed 80, no gradients—raw, continuous motion with border-y dividers.

[Product Detail]
Two-column grid on desktop with massive heading (5xl-8xl uppercase). Each column has left border-l-4 with massive background numbers (6rem-8rem) positioned absolutely. Paragraphs in muted color with generous line-height. Numbers change color on hover.

[Features]
Sticky scroll cards (top-24/top-32) that stack vertically as user scrolls. Display massive index numbers (6xl-8xl) in muted tones. Feature titles in accent color at 3xl-6xl uppercase. Sharp 2px borders that highlight on hover. Cards use p-8/p-12 with responsive flex layout.

[Blog]
2-3 column grid (md:grid-cols-2 lg:grid-cols-3) with gap-px hairline dividers. Each card shows massive background number (3rem-4rem), uppercase title with translate-x-4 hover effect. Author and date in footer with border-top. Hover transitions to muted background.

[How It Works]
Three-column grid with gap-px hairline dividers creating connected cards. Massive step numbers (8rem-12rem) at top, content at bottom. Full card color inversion on hover (background to accent, text to black). Min-height 500-600px for dramatic scale.

[Benefits]
Full-width list with border-b dividers. Massive titles (4xl-7xl) that translate horizontally on hover (translate-x-4/translate-x-8). Descriptions fade in on hover (opacity-0→100) on desktop, always visible on mobile. Text-right alignment for descriptions on desktop.

[Pricing]
2-3 column grid (md:grid-cols-2 lg:grid-cols-3). Border-based cards with 2px borders. Prices at 6xl-7xl. Full card hover transitions (border and background to accent, text to black). Features use colored square bullets (h-2 w-2). Highlighted tier has muted background.

[Testimonials]
Horizontal scrolling marquee (slower speed 40). Large quotes (4xl bold uppercase) with accent border-left (4px). Author details with square placeholders. Wide spacing (mx-12) between cards for breathing room. No gradients on edges.

[FAQ]
Accordion with large questions (xl-4xl uppercase). Touch-friendly expand/collapse icons in 40x40px containers. Answers in muted color (lg-2xl) with generous line-height. Framer Motion height animations (duration 300ms, easeInOut).

[Footer]
Full-height section (min-h-screen) on accent background with black text. Massive headline using clamp(2.5rem,8vw,10rem). Huge input with border-bottom styling. 2-4 column footer nav grid. Bold 2px border-t divider for copyright section.
```

</details>

---

### 14 — Luxury

``` light | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Luxury
Mode: light | Font: serif

Elegant serif typography with monochromatic palette and gold accents. Ultra-slow animations, generous white space, and architectural precision. High-end fashion magazine editorial aesthetic with depth through subtle shadows and layering.

--- Layout by Section ---

[Hero]
Asymmetric 12-column grid with text content in left 7 columns (bottom-aligned) and hero image in right 5 columns. Decorative horizontal line and 'Est. 2024' label. Massive type scale (text-5xl to text-9xl). Vertical writing mode label on image. Hero image has shadow and inner border.

[Stats]
Horizontal strip with 2-4 column grid. Vertical left border on each stat. Large italic Playfair numerals with tiny uppercase labels. Responsive: 2 cols mobile, 4 cols desktop.

[Product Detail]
Two-column asymmetric layout (5/6 split with offset). Headline on left with gold italic accent. Body text on right with drop cap on first paragraph.

[Features]
Alternating image-text layout with offset columns. Images 3:4 aspect ratio with shadow, grayscale default. Text in 4 columns offset from edges. Numbered labels (01, 02) in gold. 'Read More' link buttons.

[How It Works]
Dark section with inverted palette. Grid of cards with 1px gap simulated borders. Each card has numbered step label, title, and description. Hover effect darkens background.

[Benefits]
Dark section with horizontal line dividers above each benefit (hover turns gold). 3-column grid. Section header split across columns.

[Pricing]
Minimalist cards with top border only. Featured tier has 4px gold top border and 'Most Popular' badge. Subtle shadows that deepen on hover. Check mark list with gold icons.

[Testimonials]
Two-column layout (content/testimonials). Each testimonial has left border (turns gold on hover), 5 gold stars, large italic serif quote, small grayscale avatar (color on hover), author name (gold on hover).

[FAQ]
Left column: section title. Right column: accordion with dividers. Question in italic serif. Plus icon in bordered square rotates to minus when open. Gold accent on open state.

[Blog]
3-column grid. Images 4:5 aspect, grayscale with shadow (deepens on hover). Metadata in tiny uppercase with decorative horizontal divider. Title turns gold on hover.

[Footer]
Dark background. Large CTA headline (gold italic accent) on left, email signup on right. Full footer navigation in 2x4 grid. Bottom bar with company name, copyright, social links. All links hover to gold.
```

</details>

---

### 15 — Material

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Material
Mode: light | Font: sans-serif

Playful, dynamic color extraction, pill-shaped buttons, and distinct elevation states. Based on Google's Material Design 3 with enhanced depth and micro-interactions.

--- Layout by Section ---

[Hero]
Large rounded container (48px radius) with decorative organic blur shapes, split layout with abstract geometric shapes on desktop, centered on mobile

[Stats]
Grid of rounded cards (24px radius) with tonal backgrounds, hover effects with shadow elevation, centered numeric values with primary color accent

[Product Detail]
Two-column split layout with text content and abstract shape visualization, generous padding, shadow-inner on image container

[Features]
Card grid with tonal surface backgrounds, icon containers with secondary color, hover scale and shadow effects, generous padding

[Blog]
Card grid with image aspect ratio 3:2, image zoom on hover, tonal surface backgrounds, uppercase meta text with primary color

[How It Works]
Numbered circular badges with glow effects on hover above rounded content cards, vertical stepper layout with shadow transitions

[Benefits]
Full-width colored container with radial gradient overlays and blur shapes, nested glass-morphism cards with border, backdrop blur, and hover effects

[Testimonials]
Card grid on tonal surface container background, avatar + content layout, star ratings in primary color, hover shadow elevation

[Pricing]
Card grid with elevated center card (-translate-y-4), ring highlight on featured tier, pill-shaped CTA badge, list items with checkmarks and hover translate

[FAQ]
Simple stacked rounded containers on muted background with hover state transitions, single-column centered layout

[Final CTA]
Full-width colored container with multiple blur shapes and radial gradients, centered email input with pill-shaped button

[Footer]
Minimal with top border, horizontal flex layout with links and hover color transitions
```

</details>

---

### 16 — Maximalism

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Maximalism
Mode: dark | Font: sans-serif

Clashing patterns, dense layouts, oversaturated colors, intentional visual clutter. MORE IS MORE.

--- Layout by Section ---

[Hero]
Full-viewport explosion with overlapping elements, floating animated shapes (stars, sparkles, emoji), massive background typography bleeding off edges, stacked multi-color text shadows, and chaotic visual layers with pattern overlays.

[Stats]
Full-width chaotic mosaic grid (2x2 on mobile, 4 columns on desktop) with each stat in a different vibrant background color. Pattern dot overlays, rotated numbers with layered text shadows, and star decorations that rotate on hover.

[Product Details]
Two-column layout with animated concentric spinning circles on left (visual chaos with floating icons at cardinal points). Right side features layered container with offset shadow layer, multi-shadow card, and bordered paragraphs alternating colors.

[Features]
3-column grid with alternating vertical offsets (staggered layout). Each card has colored icon container with rotation on hover, colored header backgrounds with transparency, and multi-layered hard shadows that intensify on hover.

[Blog]
3-column grid with middle card offset vertically. Overlapping card stack with dramatic hover lift effects, colored date badges, gradient image overlays, and scale/rotation transitions.

[How It Works]
3-step layout with horizontal connecting gradient line, numbered circles with different accent colors, cards offset vertically on alternating steps, and centered content.

[Benefits]
Two-column asymmetric layout with left column containing title/CTA and right column with stacked benefit cards. Each card has colored border, icon circle, and transforms on hover (translate + scale).

[Testimonials]
3-column grid with rotated cards (slight rotation at rest, straightens on hover), colored star ratings, bordered avatar images with accent colors, and vertical offset on middle column.

[Pricing]
3-column grid with center card elevated and scaled larger. Highlighted tier has top badge, glowing border shadow, and colored header. Check icons with accent colors for features list.

[FAQ]
Stacked accordion items with vibrant colored borders (changes when open). Chevron icons that rotate 180deg on open. Open state reveals colored top border and patterned background with transparency.

[Footer]
Dense 5-column grid with logo column and 4 navigation columns. Gradient logo, colored section headings rotating through accent colors, and social icons with colored borders that fill on hover.
```

</details>

---

### 17 — Simple Dark

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Simple Dark
Mode: dark | Font: sans-serif

An atmospheric dark mode design system built on deep slate tones with warm amber accents. Features ambient glow effects, glass-like translucent cards, geometric typography, and generous breathing room. Ethereal yet grounded—like a premium app at midnight.

--- Layout by Section ---

[Hero]
Centered layout with massive headline. Ambient glow behind text creates depth. Trust badge floats above with subtle glow and pulsing dot. CTAs side by side with amber glow effect on primary button hover. Background has very subtle radial gradient warmth.

[Stats]
Horizontal strip with glass-effect background. Stats separated by subtle vertical dividers (1px, low opacity). Numbers in display font with amber accent. Subtle top/bottom borders.

[Product Detail]
Two-column layout. Left side has ambient glow orb decoration. Text content right-aligned on left column. Right column has floating glass card with abstract UI mockup inside.

[Features]
Clean 3-column grid of glass cards. Icons in amber-tinted circles. Hover reveals subtle glow. First feature can span 2 columns for emphasis. Consistent card heights.

[How It Works]
Horizontal numbered steps. Large circled numbers with amber fill. Connecting line between steps (subtle, dashed). Cards below each with glass effect.

[Benefits]
Split layout with large ambient orb on left side. Benefits as a clean list on right with amber checkmarks. Generous spacing between items.

[Pricing]
3-column glass cards. Highlighted tier has amber border glow, 'Popular' badge, and is slightly larger (scale-105 + translate-y-4 on desktop for prominence). Prices large in display font. Feature lists with subtle checkmarks.

[Testimonials]
Staggered 3-column layout. Glass cards with subtle amber accent line on left edge. Avatar images with ring border. Quote in italic.

[FAQ]
Clean accordion with plus/minus icons. Questions in medium weight, answers in regular. Subtle dividers between items. No backgrounds.

[Blog]
3-column grid with glass card effect on images. Hover lifts card slightly. Date/author in muted text. Clean typography hierarchy.

[Footer]
Multi-column with subtle top border. Logo and description left. Nav groups right. Social icons as subtle ghost buttons. Very clean, minimal.
```

</details>

---

### 18 — Modern Dark

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Modern Dark
Mode: dark | Font: sans-serif

A cinematic, high-precision dark mode design featuring layered ambient lighting through animated gradient blobs, mouse-tracking spotlight effects, and meticulously crafted micro-interactions that feel like premium software.

--- Layout by Section ---

[Hero]
Centered cinematic hero with parallax scroll effects, gradient headline treatment, and floating announcement badge with ping animation. Trust indicators displayed as overlapping avatars below CTAs.

[Stats]
Bold 4-column grid with gradient text for numbers, trend badges, and subtle hover glow effects. Numbers use massive typography (text-7xl) with gradient fills.

[Product Detail]
Split 2-column layout with text content on left and mock interface visual on right. Mock interface includes macOS-style window controls and abstract UI components with accent highlights.

[Features]
Asymmetric 6-column bento grid with varying card sizes. Hero feature card spans 4 columns and 2 rows with integrated data visualization. Cards use mouse-tracking spotlight effects.

[Blog]
Magazine-style 3-column grid with hover-zoom images, gradient overlays on hover, and clean metadata presentation. Images have subtle opacity transitions.

[How It Works]
3-column grid with numbered cards featuring glowing accent borders. Step numbers displayed in large format with glow effects. Connection line spans across cards on desktop.

[Benefits]
Sticky left column with scrolling right column. Right side features stacked cards with checkmark icons and hover border accent effects.

[Testimonials]
3-column masonry grid with star ratings, quote text, and author cards. Cards lift slightly on hover with subtle shadow enhancement.

[Pricing]
3-column tier grid with highlighted middle tier. Badge labels, large pricing typography, checkmark feature lists, and full-width CTAs. Highlighted tier has enhanced glow shadow.

[FAQ]
Centered single-column accordion with animated height transitions and rotating chevron icons. Smooth expand/collapse with expo-out easing.

[Footer]
5-column grid with brand section, navigation columns, and social links. Subtle separation with top border and legal links in footer bottom.
```

</details>

---

### 19 — Monochrome

``` light | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Monochrome
Mode: light | Font: serif

A stark, editorial design system built on pure black and white. No accent colors—just dramatic contrast, oversized serif typography, and precise geometric layouts. Evokes high-end fashion editorials and architectural portfolios. Austere, sophisticated, unapologetically bold.

--- Layout by Section ---

[Hero]
Full-width single column: badge with dot indicator, massive oversized headline (9xl), decorative thick rule with small bordered square, subheadline, dual CTAs, trust indicator. No images—pure typography as the hero element. Heavy 4px bottom border.

[Stats]
Horizontal strip, inverted (black bg, white text). 4-column grid on desktop, 2-col on mobile. Stats separated by vertical dividers. Oversized numbers in display serif, small caps labels, trend info. Subtle vertical line texture overlay for depth.

[Product Detail]
Two-column editorial spread with section label. Left: large headline. Right: body text with boxed drop cap (bordered square containing first letter) on first paragraph. Grid pattern overlay for texture. Heavy 4px bottom border.

[Features]
Dense 3-column grid with 1px gaps filled with black. Each feature card has bordered icon box + numbered label, headline, description. Cards invert colors on hover (100ms transition). Heavy 4px bottom border.

[How It Works]
3-column centered layout. Bordered square boxes with large step numbers, connected by horizontal lines. Headline + description below each. Diagonal line texture overlay. Heavy 4px bottom border.

[Benefits]
Checklist format with oversized checkmarks (custom SVG, not icons). Benefits as bold headlines with supporting text. Alternating alignment for visual interest.

[Pricing]
3-column grid with 1px gaps. Highlighted tier is inverted (black bg) AND elevated vertically on desktop (-my-8, py-16) with subtle shadow. Non-highlighted tiers have hover bg change. Badge, name, price, description, feature list, CTA button. Heavy 4px bottom border.

[Testimonials]
3-column grid, middle column offset down (mt-8). Oversized quote marks (opacity 10%, increases on hover). Large italic blockquote, author info below with top border that thickens on hover. Heavy 4px bottom border.

[FAQ]
Accordion with plus/minus icons. Questions in bold serif, answers in lighter weight. Heavy bottom borders on each item. No backgrounds—just lines and type.

[Blog]
3-column grid. Each article: bordered image (grayscale → color on hover, border thickens 2px→4px, image scales 105%), date/author metadata, headline, description, 'Read' link. Heavy 4px bottom border.

[Footer]
Dense, newspaper-style footer. Multi-column layout with section headers in small caps. Social icons as simple outlined circles. Heavy top border.
```

</details>

---

### 20 — Neo-brutalism

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Neo-brutalism
Mode: light | Font: sans-serif

A raw, high-contrast aesthetic that mimics print design and DIY punk culture. Characterized by cream backgrounds, thick black borders (4px), hard offset shadows with zero blur, clashing vibrant colors (Hot Red, Vivid Yellow, Soft Violet), and Space Grotesk typography at heavy weights. Embraces asymmetry, rotation, sticker-like layering, and organized visual chaos.

--- Layout by Section ---

[Hero]
Asymmetric split with massive rotated headline text blocks. Left side has border-boxed text with different colors and rotations. Right side features a 'visual chaos' container with overlapping shapes and badges. CTAs use brutalist shadows that translate on hover. Fully responsive with stacked layout on mobile.

[Stats]
4-column brutalist grid (2 columns on tablet, 1 on mobile) with thick white borders on black background. Hover inverts to accent color. Each stat has oversized numbers (text-7xl), uppercase labels, and decorative bars. No icons, just raw numerical data.

[Features]
3-column grid (1 on mobile) of cards with thick black borders and 8px offset shadows. Icons enclosed in bordered, colored accent boxes. Card headers have numbered badges and border separators. Hover lifts cards upward with deeper shadows.

[How It Works]
3 centered boxes (stacked on mobile) connected by dashed line on desktop. Each step has a large rotated number badge at top with accent background and thick border. Hover rotates the badge further. Process badge at top with pill shape.

[Benefits]
Split 2-column (stacked on mobile). Left: vibrant red accent with radial dot pattern overlay, massive white text with text shadow, rotated white card for subtitle. Right: clean cream background with bold list items using square bullets that change color on hover.

[Pricing]
3-column card grid (1 on mobile) with massive hard shadows (12-16px). Highlighted plan scales up slightly and uses black header with white text. Price numbers are huge (text-6xl). Features use custom checkbox bullets. Decorative pattern border at top.

[Testimonials]
Infinite horizontal marquee (react-fast-marquee) with gradient fade edges. Cards are white with thick borders and large shadows. 5-star ratings as large text. Author section has bordered avatar and separate background.

[FAQ]
Stacked accordion with details/summary. Each item is a thick-bordered card with shadow. Open state rotates the +/X icon and reveals border separator. Questions in bold uppercase. Answers on different background (neo-muted).

[Blog]
3-column grid (1 on mobile). Cards with thick borders. Images are grayscale with date badge overlay. Hover restores color and scales image. Title underlines on hover. Author section has border separator at bottom.

[Footer]
Yellow background with thick top border. Logo is rotated text block. Navigation links are bold uppercase with hover state that inverts to black background. Social icons in bordered squares with shadows.
```

</details>

---

### 21 — Neumorphism

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Neumorphism
Mode: light | Font: sans-serif

Extruded and inset elements via dual shadows on monochromatic backgrounds. Soft, tactile, and physically grounded with excellent accessibility.

--- Layout by Section ---

[Hero]
Asymmetric split layout (60/40) with content on left and nested depth visual on right. Features animated floating cards and interactive 3D nested circles that respond to hover with scale and rotation.

[Stats]
Two-stage presentation: inline stats in hero, then dedicated section with four extruded cards inside a deep inset container. Cards lift and scale on hover.

[Features]
Bento-style grid with one large featured card (2 rows) and smaller cards. Deep inset icon wells create tactile depth. Smooth hover scale transforms.

[How It Works]
Three-column horizontal stepper with nested depth circles for step numbers, connected by a visible inset rail with gradient progress indicator.

[Benefits]
Split layout with checklist items in inset containers on left, abstract UI mockup visualization on right showing layered neumorphic elements.

[Pricing]
Three-column grid with center card highlighted via subtle scale (1.05x) and enhanced shadow depth. Badge floating above highlighted tier.

[Testimonials]
Asymmetric grid with one large featured testimonial (2 columns, 2 rows) and four smaller testimonials. Star ratings in inset pills, avatars in deep inset circles.

[FAQ]
Two-column grid with question headers and answers inside inset containers that feel carved into cards.

[Blog]
Three-column grid with first post spanning 2 columns. Image areas with overlay, smooth scale transforms on hover.

[Footer]
Four-column link grid with company info spanning 2 columns. Copyright in centered inset pill at bottom.
```

</details>

---

### 22 — Newsprint

``` light | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Newsprint
Mode: light | Font: serif

Stark black and white, high contrast, tight grids, newspaper aesthetic, sharp lines, editorial depth.

--- Layout by Section ---

[Hero]
Split 8-col/4-col grid. Main column has massive headline (5xl → 9xl), drop-cap intro paragraph, and CTA buttons. Side column contains stats box and ad placeholder with borders.

[Stats]
Full-width black background ticker with horizontal marquee. Monospace labels, bold values, red accent badges.

[Features]
4-column top grid with icons in bordered boxes, 3-column bottom grid with bullet points. All cells separated by black borders (collapsed grid style).

[Blog]
3-column grid with bordered card style. Grayscale images with sepia hover, date/author metadata in monospace, underline on hover.

[How It Works]
Dark inverted section (black bg, white text). 3-column grid with numbered red boxes, horizontal connecting line, vertical layout breakdown.

[Benefits]
Editorial 5-col/7-col split. Left has illustration placeholder, right has numbered list in 2-column text layout.

[Testimonials]
2-column grid with large quote marks, serif quotes, bordered author cards with grayscale images.

[Pricing]
3-column table grid with explicit borders. Highlighted tier has distinct background, massive serif pricing, feature checkmarks.

[FAQ]
4-col/8-col split. Sidebar has help center box. Main area has accordion with plus/minus icons that rotate, expandable answers.

[Footer]
Multi-column site map with strict borders, company description, social icons in bordered boxes, edition/copyright info.
```

</details>

---

### 23 — Organic / Natural

``` light | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Organic / Natural
Mode: light | Font: serif

Earth-inspired palette with moss greens, terracotta, and sand tones. Features organic blob shapes, grain texture overlays, asymmetric rounded corners, and soft shadows. Embraces wabi-sabi philosophy with warmth and natural imperfection.

--- Layout by Section ---

[Hero]
Centered layout with overlapping organic blob backgrounds. Large serif typography with generous spacing. Trust badge with rounded pill shape. Dual CTAs in pill-shaped buttons.

[Stats]
Horizontal grid (2 cols mobile, 4 cols desktop) with centered text. Large serif numbers with hover scale animation. Subtle border separators.

[Product Detail]
Two-column split with rotated image frame and organic blob accent. Image has thick white border and soft shadow. Text constrained to max-w-2xl for readability.

[Features]
3-column responsive grid with cards featuring varied organic border radii. Icon containers with rounded corners that fill on hover. Blob background for ambient depth.

[Blog]
3-column grid of articles. Rounded image containers with overlay that fades on hover. Metadata with dot separators.

[How It Works]
3-step horizontal layout with curved SVG connecting path. Large numbered circles with thick borders. Centered text alignment.

[Benefits]
Two-column layout with dark moss green background and grain texture. Checkmark icons in rounded containers. Image masked with organic blob border-radius shape.

[Testimonials]
3-column grid on textured sand-colored background. Cards with subtle rotation on hover. Large quote marks as decorative element.

[Pricing]
3-column grid with center card scaled and highlighted. Rounded cards with soft shadows. Badge labels for featured tier.

[FAQ]
Vertical accordion with organic rounded borders. Chevron rotates on open. Smooth expand/collapse animation.

[Footer]
Dark charcoal background with 4-column grid. Rounded social icons with hover states. Moss green accent for company branding.
```

</details>

---

### 24 — Playful Geometric

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Playful Geometric
Mode: light | Font: sans-serif

A vibrant, high-energy aesthetic that combines a stable structural grid with whimsical geometric decorations. It relies on bright solid colors, simple primitive shapes (circles, triangles, squiggles), and tactile interactions to create a friendly, optimistic vibe reminiscent of modern Memphis design.

--- Layout by Section ---

[Hero]
Centralized or split layout where the main headline is framed by floating geometric primitives (3D-looking flat shapes). The CTA button sits on a 'blob' or irregular shape background. Background features a subtle dot pattern.

[Stats]
Row of colorful distinct shapes (circle, square, triangle, hexagon) acting as containers for the numbers. The containers vibrate or rotate slightly on hover.

[Product Detail]
Two-column layout. Image side has a 'collage' feel with offset colored rectangles behind the main product image. Text side uses substantial padding and colorful bullets.

[Features]
Bento-box style grid, but each cell has a different playful background color (very light tints) or border radius strategy (some fully round, some leaf-shaped). Icons are solid, colorful circles.

[Blog]
Masonry or grid where featured images are clipped into interesting shapes (arch, pill, circle). Titles use a chunky display font. Tags look like little stickers.

[How It Works]
Horizontal or vertical timeline connected by a literal dashed SVG line that loops and squiggles between steps. Step numbers are inside solid colored stars or bursts.

[Benefits]
Alternating layout. Each benefit text block is paired with a large, abstract geometric composition (e.g., a square balancing on a circle) representing the concept.

[Testimonials]
Cards styled like speech bubbles (with the little tail). They scattered slightly (random rotation +/- 2deg) to feel informal. Avatars pop out of the frame.

[Pricing]
Three distinct columns. The 'Recommended' tier pops out with a thick dashed border and a floating 'Best Value' badge that looks like a sticker. Prices are massive and colorful.

[FAQ]
Accordion items separated by thick distinct borders. When opened, the background fills with a light pattern (dots or lines). The expand icon is a large playful arrow or plus sign.

[Final CTA]
A contained box with a 'wavy' top edge or bottom edge. High contrast background (bright yellow or blue). Button shakes slightly to attract attention.

[Footer]
Background is a dark shape with a 'dripping' paint effect or wave at the top. Large footer links with fun hover underlines (squiggles).
```

</details>

---

### 25 — Business Style

``` light | serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Business Style
Mode: light | Font: serif

An editorial-inspired minimalist design system centered on elegant serif typography. Warm ivory backgrounds with subtle paper texture, refined spacing, rule lines, and classical proportions create a timeless, literary aesthetic. Enhanced depth through layered gradients and multi-toned shadows. The design whispers sophistication through restraint and typographic excellence.

--- Layout by Section ---

[Hero]
Full-width centered layout with dramatic oversized serif headline (2.5rem mobile, 7xl desktop). Generous vertical breathing room (py-32 to py-44). Subtle decorative rule line below headline. Dual CTA buttons with refined hover states including subtle lift. Trust indicator in small caps with generous letter-spacing. Responsive text scaling maintains hierarchy on all devices.

[Stats]
Horizontal 4-column layout (2-column on mobile) with thin vertical rule dividers between stats. Dividers appear between columns on mobile and all stats on desktop. Large display serif numbers (4xl mobile, 5xl desktop). Labels in monospace small caps with wide tracking (0.15em). Clean card background with border lines top and bottom.

[Features]
3-column grid (stacks to 1 column mobile) with generous gaps (gap-8). Each card has 2px accent top border, rounded corners, and enhanced hover effect with background tint. Icon in muted circle background. Serif title with sans-serif description. Hover reveals subtle background shift and enhanced shadow.

[How It Works]
3-column layout with large circular step numbers in serif. Horizontal connecting line on desktop. Each step has generous padding and clean typography hierarchy. Background uses card color for contrast.

[Benefits]
Asymmetric two-column layout (1.3fr / 0.7fr ratio, stacks on mobile). Left column has title, subtitle, and bulleted list with elegant dash markers. Right column features enhanced abstract graphic with gradient backgrounds, layered circles, and hover-interactive elements. Refined typography hierarchy throughout.

[Pricing]
3-column grid (stacks vertically mobile) with center card elevated (-translate-y-4 on desktop). Thin rule borders with accent border on highlighted tier. Large serif price numbers. Feature lists with checkmarks colored by tier importance. Highlighted tier has warm accent background tint (accent-muted). Badge positioning uses absolute positioning.

[Testimonials]
3-column grid (stacks mobile) with large decorative opening quotation mark (100px, 20% opacity) in accent color. Italic serif quotes with generous line-height. Author info with circular avatar (48x48px) and refined typography. Subtle card borders and shadows.

[FAQ]
Clean accordion with serif question titles (text-xl). Circular button with plus icon that rotates 45deg to form X when open. Thin border separators between items. Generous padding (py-6). Sans-serif answer text with relaxed leading (1.75). Smooth height and opacity animations.

[Blog]
3-column grid (stacks mobile) with images in 16:10 aspect ratio. Date in monospace small caps. Serif titles with hover color shift to accent. Images have subtle border and shadow enhancement on hover. 'Read more' link with arrow icon and translate animation.

[Footer]
5-column grid (2 columns for company, 1 each for nav groups, stacks to 2-col on mobile). Logo in serif. Social icons in circular borders with hover state showing accent color. Bottom copyright bar with thin top border and flex layout for alignment. Links have accent hover states.
```

</details>

---

### 26 — Retro

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Retro
Mode: light | Font: sans-serif

Ugly-cool 90s nostalgia aesthetic with Windows 95 beveled UI, system fonts, bright primary colors, marquee scrolling text, and maximum visual chaos.

--- Layout by Section ---

[Hero]
Centered layout with animated rainbow text headline (4s color cycle), dual colored horizontal bars as dividers, full-width CTA buttons with arrow decorations, and retro hit counter display at bottom.

[Stats]
Table-style grid (2x2 on mobile, 1x4 on desktop) with visible cell borders, alternating white/gray backgrounds, inset beveled frame container, and monospace labels.

[Features]
Two-column table layout with 80px colored icon cells (alternating navy/teal backgrounds) and text description cells, thick visible borders between rows, alternating row backgrounds.

[How It Works]
Vertical step list with large beveled yellow numbered badges (48px-64px), gray content panels with outset bevels, groove HR dividers between steps.

[Benefits]
2-column grid of beveled panels on navy background, each with lime green asterisk bullet and gray panel containing title and description.

[Pricing]
3-column card grid with highlighted center tier (yellow header, red border, pulsing badge), beveled window-style cards with title bars, feature lists with green asterisk bullets.

[Testimonials]
Horizontal auto-scrolling marquee (30px/s speed) with fixed-width cards (350px), Windows 95 title bar gradients, yellow inset content panels with 5-star ratings.

[FAQ]
Accordion panels with gradient title bars (navy to blue), expandable sections, yellow answer panels with inset bevels.

[Blog]
3-column card grid with thick beveled borders, blog images with inset borders, monospace metadata, underlined blue read-more links.

[Footer]
4-column navigation grid on navy background with yellow headings and cyan links, groove HR divider above company info, centered layout with social buttons.
```

</details>

---

### 27 — Tech Style

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Tech Style
Mode: light | Font: sans-serif

A bold, minimalist-modern visual system combining clean aesthetics with dynamic execution. Features signature Electric Blue gradients, sophisticated dual-font pairing (Calistoga + Inter), animated hero graphics, inverted contrast sections, and micro-interactions throughout. Professional yet design-forward—confidence without clutter.

--- Layout by Section ---

[Hero]
Asymmetrical two-column grid (1.1fr / 0.9fr). Left: bold headline with gradient text accent on key word, animated badge with pulsing dot, trust indicators with stacked avatars. Right: abstract generative art composition with floating animated cards, rotating outer ring, geometric elements, and bold corner accent block.

[Stats]
INVERTED section with dark background (foreground color). Large display numbers (5xl-6xl), trend badges with arrow icons, dot pattern texture overlay. Vertical dividers between stats on desktop.

[Features]
Asymmetric masonry grid where first card spans 2 rows. Gradient icon backgrounds (not translucent). Hover gradient overlays on cards. Featured card has 'Learn more' link and corner glow effect.

[How It Works]
Horizontal timeline on desktop. Large circular step numbers (24x24) with inner gradient glow. Cards below each step. Arrow connectors between steps using accent-colored circular badges. Centered header layout.

[Benefits]
Two-column asymmetric grid (1.2fr / 0.8fr). Text content with checkmark list items using accent-colored badges. Visual element has asymmetric border-radius (rounded-tl-[4rem] rounded-br-[4rem]) with abstract UI placeholder.

[Pricing]
3-column grid with highlighted tier elevated (-translate-y-4) and featuring gradient border effect (2px gradient stroke). Gradient price text on highlighted tier. Badge hangs off top edge. Gradient checkmarks for highlighted features.

[Testimonials]
3-column grid with center card offset vertically. Large decorative quote mark (120px, 8% opacity). Gradient accent bar at top of each card. Display font for quotes in italic. Larger avatars with accent border.

[FAQ]
Clean accordion with rotating Plus icon. Border-bottom dividers. Question text is semibold xl, answer is muted lg with relaxed line-height.

[Blog]
3-column grid with section label badge. Featured badge on first post. Image hover: scale + gradient overlay from bottom. 'Read more' link with arrow icon on each card. Pill-style 'View all' button in header.

[Footer]
5-column grid (company spans 2). Social icons as rounded-xl buttons with accent hover. Navigation groups with link lists. Bottom bar with border-top separator.
```

</details>

---

### 28 — Hand-Drawn / Sketch

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Hand-Drawn / Sketch
Mode: light | Font: sans-serif

Organic wobbly borders, handwritten typography, paper textures, and playful imperfection. Every element feels sketched with markers and pencils on textured paper.

--- Layout by Section ---

[Hero]
Split 2-column grid with oversized marker-style headline, decorative hand-drawn arrow pointing to CTA, and polaroid-frame product mockup with wobbly borders. Trust indicators use overlapping avatar circles.

[Stats]
Horizontal grid of stats displayed in irregular organic shapes (wobbly circles) with varying border radii. Each stat has playful rotation for authentic hand-drawn feel.

[Product Detail]
Centered content in white card with wobbly borders, sticky-note tag at top center, drop-cap first letter treatment, and constrained text width for readability.

[Features]
3-column grid of post-it yellow cards with tape decoration at top. Each card includes rough circular icon container and wobbly borders for sketchy aesthetic.

[Blog]
3-column grid with polaroid-style frames. Dashed borders on image placeholders, hard offset shadows, and playful rotation on hover for scrapbook feel.

[How It Works]
3-column step layout with decorative squiggly connecting line (desktop). Steps numbered in wobbly-border circles with hard offset shadows.

[Benefits]
Centered white container with thick wobbly border and hard shadow. 2-column grid with hand-drawn bullet points (filled circles) for each benefit item.

[Testimonials]
3-column grid of speech bubbles with geometric tail pointing down-left. Quote icon, italic text, and author info with circular avatar below bubble.

[Pricing]
3-column grid with wobbly-border cards. Highlighted plan has rotating badge, dashed circle overlay, slight scale, and stronger shadow for emphasis.

[FAQ]
Single column, dashed border dividers between questions. Bold headings with relaxed body text for easy scannability.

[Footer]
4-column grid navigation with wavy underline on section headers. Social icons in wobbly circles, dashed border separator at bottom.
```

</details>

---

### 29 — Swiss

``` light | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Swiss
Mode: light | Font: sans-serif

A rigorous implementation of the International Typographic Style (1950s). Characterized by objective typography, sans-serif fonts (Inter), mathematical grids with subtle texture patterns, and a strict black/white/red palette. Prioritizes readability, precision, asymmetrical organization, and visual depth through layered patterns.

--- Layout by Section ---

[Hero]
Split screen composition with asymmetric 8:4 grid ratio. Left: massive typography (text-6xl to text-[10rem]) with geometric accent bar and functional CTAs. Right: geometric abstract composition with grid pattern overlay, featuring basic shapes (circles, rectangles, lines) in black/red on muted background.

[Stats]
Horizontal strip divided by visible borders. 2x2 grid on mobile, 1x4 on desktop. Massive numbers with hover scale animation, rotating plus icons, and color inversion on hover (black → red). No decorative icons, pure data presentation.

[Product Detail]
Split 7:5 grid. Left: 2x2 visual grid of geometric compositions with texture overlays (dots, diagonals, grid patterns). Right: large typographic headline with body text. Mobile stacks vertically.

[Features]
Asymmetric two-column layout. Left: sticky header with dots pattern overlay and numbered label (01. System). Right: stacked feature cards with thick borders, numbered indicators, diagonal arrow icons, and full hover state color inversion.

[How It Works]
Three-column grid with visible borders and black background. Each step features giant watermark numbers (text-8xl at 10% opacity), red accent border on left, and white text on black.

[Benefits]
Asymmetric 5:7 grid split. Left: diagonal pattern overlay with section header. Right: stacked list items with numbered box indicators, hover state inverts to black background with red accent numbers.

[Testimonials]
Three-column responsive grid (1 col mobile, 2 col tablet, 3 col desktop). Large red quotation mark, bold uppercase quote text, thick top border that changes to red on hover, subtle upward translation on hover.

[Pricing]
Three-column card layout with 4px black borders. Highlighted plan uses inverted colors (black bg, white text, red accents). Strict rectangular shapes, no rounded corners.

[FAQ]
Two-column rigid grid (1 col mobile) with 4px black borders and 1px gaps creating visual grid. Each FAQ is a card with numbered label, rotating plus icon, and full hover inversion (white → red bg).

[Blog]
Four-column layout: 1 col sidebar with grid pattern (section header + CTA), 3 col article grid. Articles have date, title, read link with arrow. Hover inverts to black background.

[Footer]
Black background with four-column layout. Large uppercase brand name, underlined email input (not boxed), square social icons with white bg that invert to red on hover.
```

</details>

---

### 30 — Terminal CLI

``` dark | mono```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Terminal CLI
Mode: dark | Font: mono

A raw, functional, and retro-futuristic command-line interface aesthetic. High contrast, monospaced precision, and blinking cursors.

--- Layout by Section ---

[Hero]
A massive ASCII art logo or headline. The subheadline types itself out. CTAs are rendered as command prompts.

[Stats]
Displayed as a system status report or table output (e.g., 'UPTIME: 99.9%', 'USERS: 10k').

[Features]
A grid of terminal windows or 'man page' style entries. Each feature has a command-line flag (e.g., '--speed', '--security').

[How It Works]
A step-by-step shell script execution log. 'Step 1: Initializing...', 'Step 2: Processing...'.

[Benefits]
A split-screen layout like a code editor (vim/vscode) showing 'Before' vs 'After' code blocks.

[Pricing]
An ASCII table layout. Selected plan highlights with an inverted color block.

[Testimonials]
Git commit logs or IRC chat logs. 'User@host says: ...'

[FAQ]
A 'man' page manual layout or a help command output (e.g., 'help --topic billing').

[Blog]
A file directory listing (ls -l). Each post is a file with permissions, date, and author.

[Footer]
A simple system footer showing shell version, current path, and copyright as a comment.
```

</details>

---

### 31 — Vaporwave

``` dark | mono```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Vaporwave
Mode: dark | Font: mono

A nostalgic, neon-drenched journey into 80s retro-futurism. High-contrast neon pinks and cyans against deep void purples. Digital grids, glowing horizons, surreal sunset gradients, and CRT scanline overlays create an immersive synthetic world.

--- Layout by Section ---

[Hero]
Full-screen immersive perspective grid floor with floating neon sun gradient backdrop. Massive glowing headline split across two lines with gradient text effect. Skewed neon-bordered CTAs with transforming hover states. Version badge with skewed container.

[Stats]
Dashboard row with bordered stat containers featuring gradient top accent bars. Hover states trigger cyan glow and color transitions. Grid layout adapts from 4 columns to stacked on mobile.

[Product Detail]
Terminal window interface with cyan borders and window control dots. Split layout with content on left and visual placeholder on right. Command-line styled text prefixes.

[Features]
Grid of glass-morphic cards with cyan laser top borders and pink side borders. Rotating diamond icon containers that spin on hover. Cards lift upward on hover with smooth transitions.

[Blog]
Grid of retro data tape/file cards with duotone gradient overlays on images. Hover triggers cyan border glow and card shadow expansion.

[How It Works]
Vertical timeline with alternating left-right steps. Central pink checkpoint dots with glow effects. Bordered step containers with corner accent decorations. Background dot pattern overlay.

[Benefits]
Windows 95-inspired file explorer window with title bar and status bar. Grid of file icons with centered layouts. Hover states change background to pink tint.

[Testimonials]
IRC/terminal-style chat boxes with user avatars in bordered containers. Author names wrapped in angle brackets. Cyan accent colors for roles.

[Pricing]
Three power-up style cards with gradient glow halos behind highlighted tier. Skewed 'MOST_POPULAR' badge. Cyan titles, massive pricing, gradient accent bars.

[FAQ]
Terminal-style accordion in bordered black container. Questions prefixed with '> QUERY:' in pink, answers with '> RESPONSE:' in cyan. Chevron rotation on expand.

[Footer]
Perspective grid floor effect fading into bottom. Multi-column link groups with cyan headings. Social icons with hover color transitions. Skewed brand logo mark.
```

</details>

---

### 32 — Crypto

``` dark | sans-serif```

<details>
<summary>复制完整 prompt（点击展开）</summary>

```
Design Style: Crypto
Mode: dark | Font: sans-serif

A bold, futuristic aesthetic inspired by Bitcoin and decentralized finance. Deep void backgrounds with Bitcoin orange accents, golden highlights, glowing elements, and precision data visualization.

--- Layout by Section ---

[Hero]
Split layout with 60/40 ratio. Left: Massive headline with Bitcoin orange gradient text and trust badge. Right: Floating animated 3D orb with spinning orbital rings and floating stat cards. Background features subtle grid pattern with radial gradient blur effects.

[Stats]
Horizontal grid of four key metrics with monospace numbers, uppercase labels, and subtle trend indicators. Dark surface background with top/bottom borders for ticker-tape feel.

[Product Detail]
Two-column layout with mockup on left, content on right. Abstract UI mockup with glass morphism, grid backgrounds, and holographic gradients.

[Features]
Three-column grid of elevated cards with background icon watermarks, glowing accent borders on hover, and icon containers with gradient backgrounds.

[Blog]
Three-column grid of image-led cards. Full-bleed images with gradient overlays, date badges, and hover scale effects that increase contrast.

[How It Works]
Vertical timeline with centered connection line. Alternating left/right content cards with numbered nodes on the centerline. Cards have corner accent borders.

[Benefits]
Three-column grid of cards with check icons in glowing circles. Gradient borders appear on hover.

[Testimonials]
Three-column grid of glass-morphic cards with large quote marks, avatar rings with orange glow, and role badges in accent color.

[Pricing]
Three-column grid with center card elevated and scaled. Popular badge floats above. Gradient buttons for highlighted tier.

[FAQ]
Accordion with chevron indicators. Glass-morphic backgrounds with smooth height transitions and padding reveals.

[Footer]
Multi-column grid with brand on left spanning two columns. Monospace section headers, subtle link hover states with orange accent.
```

</details>

---

## 使用方法

### 方法 1：直接复制

找到风格 → 展开 → 复制整段 prompt → 粘贴给 AI，加上你的内容需求就行。

### 方法 2：组合 prompt

```
请用以下设计风格做一个 SaaS landing page：

[粘贴完整风格 prompt]

我的产品信息：
- 产品名：XXX
- 一句话描述：XXX
- 核心功能：XXX
```

