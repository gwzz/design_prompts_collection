"""Static asset templates emitted by the site builder."""

INDEX_SCRIPT = """const state = { mode: 'all', font: 'all', category: 'all' };
const CLICK_STORAGE_KEY = 'dpc-click-deltas-v1';
const LIKED_STORAGE_KEY = 'dpc-liked-prompts-v1';

function readJsonScript(id, fallback) {
  const element = document.getElementById(id);
  if (!element) return fallback;
  try {
    return JSON.parse(element.textContent);
  } catch (error) {
    return fallback;
  }
}

function readStorageMap(key) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : {};
  } catch (error) {
    return {};
  }
}

function writeStorageMap(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    // Ignore storage failures.
  }
}

function readLikedPrompts() {
  try {
    const raw = localStorage.getItem(LIKED_STORAGE_KEY);
    return new Set(raw ? JSON.parse(raw) : []);
  } catch (error) {
    return new Set();
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

const promptIndex = readJsonScript('prompt-index-data', []);
const featuredStatsSeed = readJsonScript('featured-stats-data', { weights: { click: 1, like: 5 }, prompts: {} });
const featuredUi = readJsonScript('featured-ui-data', {
  clicksLabel: 'Clicks',
  likesLabel: 'Likes',
  scoreLabel: 'Score',
  sourceTitle: 'Featured ranking',
  sourceBody: 'Featured ranking blends clicks and likes.',
  limit: 3,
});
const apiBase = document.body.dataset.apiBase || '../api';

function getFallbackStats(slug) {
  const clickDeltas = readStorageMap(CLICK_STORAGE_KEY);
  const likedPrompts = readLikedPrompts();
  const seeded = featuredStatsSeed.prompts[slug] || { click_count: 0, like_count: 0 };
  const clickCount = seeded.click_count + (clickDeltas[slug] || 0);
  const likeCount = seeded.like_count + (likedPrompts.has(slug) ? 1 : 0);
  return {
    click_count: clickCount,
    like_count: likeCount,
    score: clickCount * (featuredStatsSeed.weights.click || 1) + likeCount * (featuredStatsSeed.weights.like || 5),
  };
}

function promptMap() {
  return new Map(promptIndex.map((prompt) => [prompt.slug, prompt]));
}

function renderFeaturedFromItems(items) {
  const root = document.getElementById('featuredList');
  if (!root || !items.length) return;
  const prompts = promptMap();
  root.innerHTML = items
    .map((item) => {
      const prompt = prompts.get(item.slug);
      if (!prompt) return '';
      return `
<a href="${escapeHtml(prompt.href)}" class="featured-link" data-featured-item data-track-click data-slug="${escapeHtml(prompt.slug)}" style="--card-accent:${escapeHtml(prompt.accent)};">
  <span class="featured-index">#${String(prompt.number).padStart(2, '0')}</span>
  <span class="featured-name">${escapeHtml(prompt.name)}</span>
  <span class="featured-note">${escapeHtml(prompt.note)}</span>
  <span class="featured-stats">
    <span class="featured-stat"><strong data-stat-click-count>${item.click_count}</strong> ${escapeHtml(featuredUi.clicksLabel)}</span>
    <span class="featured-stat"><strong data-stat-like-count>${item.like_count}</strong> ${escapeHtml(featuredUi.likesLabel)}</span>
  </span>
</a>`;
    })
    .join('');
}

function renderFeaturedFallback() {
  const ranked = promptIndex
    .map((prompt) => ({ ...prompt, ...getFallbackStats(prompt.slug) }))
    .sort((left, right) => {
      if (right.score !== left.score) return right.score - left.score;
      if (right.like_count !== left.like_count) return right.like_count - left.like_count;
      if (right.click_count !== left.click_count) return right.click_count - left.click_count;
      return left.number - right.number;
    })
    .slice(0, featuredUi.limit || 3);
  renderFeaturedFromItems(ranked);
}

async function refreshFeaturedFromApi() {
  if (!promptIndex.length) return false;
  try {
    const response = await fetch(`${apiBase}/featured?limit=${featuredUi.limit || 3}`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    });
    if (!response.ok) return false;
    const payload = await response.json();
    if (!payload.items || !Array.isArray(payload.items)) return false;
    renderFeaturedFromItems(payload.items);
    return true;
  } catch (error) {
    return false;
  }
}

function setActive(group, button) {
  group.querySelectorAll('[data-selectable]').forEach((item) => item.classList.remove('active'));
  button.classList.add('active');
}

function filterCards() {
  const search = document.getElementById('searchInput').value.trim().toLowerCase();
  let visible = 0;

  document.querySelectorAll('.catalog-item').forEach((card) => {
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

  const suffix = document.body.dataset.resultsSuffix || 'styles';
  document.getElementById('resultCount').textContent = `${visible} ${suffix}`;
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

document.querySelectorAll('[data-locale-link]').forEach((link) => {
  link.addEventListener('click', () => {
    try {
      localStorage.setItem('preferredLocale', link.dataset.locale);
    } catch (error) {
      // Ignore storage failures.
    }
  });
});

filterCards();
renderFeaturedFallback();
refreshFeaturedFromApi();
"""

DETAIL_SCRIPT = """const CLICK_STORAGE_KEY = 'dpc-click-deltas-v1';
const LIKED_STORAGE_KEY = 'dpc-liked-prompts-v1';
const CLIENT_ID_KEY = 'dpc-client-id-v1';
const SESSION_ID_KEY = 'dpc-session-id-v1';
const LOCAL_CLICK_MARKS_KEY = 'dpc-local-click-marks-v1';
const copyButton = document.querySelector('[data-copy-target]');
const apiBase = document.body.dataset.apiBase || '../../api';

function readJsonScript(id, fallback) {
  const element = document.getElementById(id);
  if (!element) return fallback;
  try {
    return JSON.parse(element.textContent);
  } catch (error) {
    return fallback;
  }
}

function readStorageMap(key) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : {};
  } catch (error) {
    return {};
  }
}

function writeStorageMap(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    // Ignore storage failures.
  }
}

function readLikedPrompts() {
  try {
    const raw = localStorage.getItem(LIKED_STORAGE_KEY);
    return new Set(raw ? JSON.parse(raw) : []);
  } catch (error) {
    return new Set();
  }
}

function writeLikedPrompts(setValue) {
  try {
    localStorage.setItem(LIKED_STORAGE_KEY, JSON.stringify([...setValue]));
  } catch (error) {
    // Ignore storage failures.
  }
}

function randomId(prefix) {
  return `${prefix}-${Math.random().toString(36).slice(2, 10)}${Date.now().toString(36)}`;
}

function getClientId() {
  try {
    const existing = localStorage.getItem(CLIENT_ID_KEY);
    if (existing) return existing;
    const next = randomId('client');
    localStorage.setItem(CLIENT_ID_KEY, next);
    return next;
  } catch (error) {
    return randomId('client');
  }
}

function getSessionId() {
  try {
    const existing = sessionStorage.getItem(SESSION_ID_KEY);
    if (existing) return existing;
    const next = randomId('session');
    sessionStorage.setItem(SESSION_ID_KEY, next);
    return next;
  } catch (error) {
    return randomId('session');
  }
}

const featuredStatsSeed = readJsonScript('featured-stats-data', { weights: { click: 1, like: 5 }, prompts: {} });

function getFallbackStats(slug) {
  const clickDeltas = readStorageMap(CLICK_STORAGE_KEY);
  const likedPrompts = readLikedPrompts();
  const seeded = featuredStatsSeed.prompts[slug] || { click_count: 0, like_count: 0 };
  const clickCount = seeded.click_count + (clickDeltas[slug] || 0);
  const likeCount = seeded.like_count + (likedPrompts.has(slug) ? 1 : 0);
  return {
    click_count: clickCount,
    like_count: likeCount,
    score: clickCount * (featuredStatsSeed.weights.click || 1) + likeCount * (featuredStatsSeed.weights.like || 5),
    liked: likedPrompts.has(slug),
  };
}

function hasLocalClickMark(slug) {
  try {
    const raw = sessionStorage.getItem(LOCAL_CLICK_MARKS_KEY);
    const marks = raw ? JSON.parse(raw) : {};
    return Boolean(marks[slug]);
  } catch (error) {
    return false;
  }
}

function setLocalClickMark(slug) {
  try {
    const raw = sessionStorage.getItem(LOCAL_CLICK_MARKS_KEY);
    const marks = raw ? JSON.parse(raw) : {};
    marks[slug] = true;
    sessionStorage.setItem(LOCAL_CLICK_MARKS_KEY, JSON.stringify(marks));
  } catch (error) {
    // Ignore storage failures.
  }
}

function recordClickFallback(slug) {
  if (!slug || hasLocalClickMark(slug)) return;
  const clickDeltas = readStorageMap(CLICK_STORAGE_KEY);
  clickDeltas[slug] = (clickDeltas[slug] || 0) + 1;
  writeStorageMap(CLICK_STORAGE_KEY, clickDeltas);
  setLocalClickMark(slug);
}

function applyStats(stats) {
  const clickTarget = document.querySelector('[data-stat-click-count]');
  const likeTarget = document.querySelector('[data-stat-like-count]');
  const scoreTarget = document.querySelector('[data-stat-score]');
  if (clickTarget) clickTarget.textContent = stats.click_count;
  if (likeTarget) likeTarget.textContent = stats.like_count;
  if (scoreTarget) scoreTarget.textContent = stats.score;

  const likeButton = document.querySelector('[data-like-button]');
  if (!likeButton) return;
  likeButton.textContent = stats.liked ? document.body.dataset.likedButtonLabel : document.body.dataset.likeButtonLabel;
  likeButton.classList.toggle('active', stats.liked);
  likeButton.setAttribute('aria-pressed', stats.liked ? 'true' : 'false');
}

function hydratePromptStatsFallback() {
  const slug = document.body.dataset.promptSlug;
  if (!slug) return;
  applyStats(getFallbackStats(slug));
}

async function hydratePromptStatsFromApi() {
  const slug = document.body.dataset.promptSlug;
  if (!slug) return false;
  try {
    const response = await fetch(`${apiBase}/stats?slug=${encodeURIComponent(slug)}&clientId=${encodeURIComponent(getClientId())}`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    });
    if (!response.ok) return false;
    const payload = await response.json();
    applyStats(payload);
    return true;
  } catch (error) {
    return false;
  }
}

async function trackPromptView() {
  const slug = document.body.dataset.promptSlug;
  if (!slug) return false;
  try {
    const response = await fetch(`${apiBase}/events/click`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slug, sessionId: getSessionId() }),
      keepalive: true,
    });
    if (!response.ok) {
      throw new Error('Click request failed');
    }
    const payload = await response.json();
    applyStats({ ...payload, liked: readLikedPrompts().has(slug) });
    return true;
  } catch (error) {
    recordClickFallback(slug);
    hydratePromptStatsFallback();
    return false;
  }
}

if (copyButton) {
  copyButton.addEventListener('click', async () => {
    const target = document.getElementById(copyButton.dataset.copyTarget);
    if (!target) return;

    try {
      await navigator.clipboard.writeText(target.textContent);
      const originalLabel = copyButton.textContent;
      const successLabel = document.body.dataset.copySuccess || 'Copied';
      copyButton.textContent = successLabel;
      copyButton.classList.add('copied');
      window.setTimeout(() => {
        copyButton.textContent = originalLabel;
        copyButton.classList.remove('copied');
      }, 1800);
    } catch (error) {
      const failedLabel = document.body.dataset.copyFailed || 'Copy failed';
      copyButton.textContent = failedLabel;
    }
  });
}

const likeButton = document.querySelector('[data-like-button]');

async function toggleLikeViaApi(slug, nextLiked) {
  const response = await fetch(`${apiBase}/events/like`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ slug, clientId: getClientId(), liked: nextLiked }),
  });
  if (!response.ok) {
    throw new Error('Like request failed');
  }
  return response.json();
}

if (likeButton) {
  likeButton.addEventListener('click', async () => {
    const slug = likeButton.dataset.slug;
    const likedPrompts = readLikedPrompts();
    const nextLiked = !likedPrompts.has(slug);

    try {
      const payload = await toggleLikeViaApi(slug, nextLiked);
      if (payload.liked) {
        likedPrompts.add(slug);
      } else {
        likedPrompts.delete(slug);
      }
      writeLikedPrompts(likedPrompts);
      applyStats(payload);
      return;
    } catch (error) {
      if (nextLiked) {
        likedPrompts.add(slug);
      } else {
        likedPrompts.delete(slug);
      }
      writeLikedPrompts(likedPrompts);
      hydratePromptStatsFallback();
    }
  });
}

hydratePromptStatsFallback();
trackPromptView();
hydratePromptStatsFromApi();
"""

STYLESHEET = """:root {
  --bg: #08080b;
  --bg-soft: #0f1018;
  --surface: rgba(255,255,255,0.03);
  --surface-strong: rgba(255,255,255,0.06);
  --text: #f3f2ed;
  --text-muted: #a1a0b3;
  --line: rgba(255,255,255,0.1);
  --line-strong: rgba(255,255,255,0.18);
  --accent: #8ea0ff;
  --accent-soft: rgba(142,160,255,0.14);
  --max: 1240px;
  --radius: 24px;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Inter', sans-serif;
}

*,
*::before,
*::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: var(--sans);
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(142,160,255,0.12), transparent 28%),
    radial-gradient(circle at bottom right, rgba(255,255,255,0.06), transparent 18%),
    linear-gradient(180deg, #08080b 0%, #0c0c12 100%);
}

a { color: inherit; text-decoration: none; }

.page-shell,
.detail-page {
  width: min(var(--max), calc(100% - 32px));
  margin: 0 auto;
}

.masthead {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(18px);
  background: rgba(8,8,11,0.7);
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.masthead-inner {
  width: min(var(--max), calc(100% - 32px));
  margin: 0 auto;
  padding: 14px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.masthead-brand {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #d6d7e8;
}

.masthead-links {
  display: flex;
  gap: 20px;
  color: var(--text-muted);
  font-size: 0.92rem;
}

.masthead-links a:hover { color: var(--text); }

.lang-switcher {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.02);
}

.lang-link {
  min-width: 48px;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 0.84rem;
}

.lang-link.active {
  background: rgba(142,160,255,0.18);
  color: #eef1ff;
}

.hero-section { padding: 36px 0 18px; }

.poster-shell {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.9fr);
  gap: 24px;
  padding: 28px;
  min-height: calc(100svh - 130px);
  border: 1px solid var(--line);
  border-radius: 34px;
  background:
    linear-gradient(140deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01)),
    linear-gradient(180deg, rgba(15,16,24,0.96), rgba(9,9,14,0.96));
  box-shadow: 0 30px 100px rgba(0,0,0,0.34);
}

.hero-copy {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 22px;
  padding: 8px 4px 8px 2px;
}

.hero-badge,
.eyebrow,
.section-kicker {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(142,160,255,0.22);
  background: var(--accent-soft);
  color: #d9deff;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.hero-title {
  margin: 0;
  font-size: clamp(3.6rem, 10vw, 7.8rem);
  line-height: 0.92;
  letter-spacing: -0.07em;
  max-width: 9ch;
}

.hero-title span {
  color: #9fb1ff;
  font-style: italic;
}

.hero-subtitle {
  margin: 0;
  max-width: 52ch;
  color: var(--text-muted);
  font-size: 1.08rem;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.hero-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 18px;
  border-radius: 999px;
  border: 1px solid var(--line-strong);
  color: var(--text);
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.hero-action:hover {
  transform: translateY(-1px);
  border-color: rgba(255,255,255,0.28);
}

.hero-action.primary {
  background: #f2f1ea;
  color: #09090d;
  border-color: #f2f1ea;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  color: #d4d5e3;
  font-size: 0.92rem;
}

.hero-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-self: stretch;
  padding: 18px;
  border-radius: 24px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--line);
}

.hero-panel-label {
  font-family: var(--mono);
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.hero-panel-copy {
  margin: 0 0 4px;
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 0.92rem;
}

.featured-link {
  display: grid;
  gap: 6px;
  padding: 16px 0;
  border-top: 1px solid rgba(255,255,255,0.07);
  transition: color 0.2s ease;
}

.featured-link:first-of-type { border-top: none; }

.featured-link:hover .featured-name { color: var(--card-accent, var(--accent)); }

.featured-index {
  font-family: var(--mono);
  font-size: 0.76rem;
  color: var(--text-muted);
}

.featured-name {
  font-size: 1.1rem;
  font-weight: 600;
}

.featured-note {
  color: var(--text-muted);
  line-height: 1.5;
  font-size: 0.92rem;
}

.featured-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.featured-stat {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.05);
  color: #d8d9e6;
  font-size: 0.74rem;
}

.featured-stat strong {
  color: #fff;
  font-weight: 700;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin: 18px auto 48px;
}

.quick-stat {
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255,255,255,0.02);
}

.quick-stat-value {
  display: block;
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  line-height: 1;
  margin-bottom: 8px;
}

.quick-stat-label {
  display: block;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
}

.support-section,
.catalog-shell {
  margin-bottom: 34px;
  border: 1px solid var(--line);
  border-radius: 30px;
  background: rgba(255,255,255,0.02);
}

.support-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  padding: 28px;
}

.support-copy h2,
.catalog-header h2 {
  margin: 14px 0 12px;
  font-size: clamp(1.9rem, 4vw, 3rem);
  line-height: 1.05;
  letter-spacing: -0.04em;
}

.support-copy p,
.catalog-header-copy {
  max-width: 58ch;
  color: var(--text-muted);
  line-height: 1.7;
}

.support-list {
  display: grid;
  gap: 16px;
}

.support-item {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 14px;
  padding: 18px;
  border-radius: 18px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
}

.support-item span {
  font-family: var(--mono);
  color: var(--accent);
}

.support-item p {
  margin: 0;
  color: #d8d8e5;
}

.catalog-shell { padding: 28px; }

.catalog-header {
  display: grid;
  grid-template-columns: 1fr minmax(280px, 420px);
  gap: 24px;
  margin-bottom: 24px;
}

.controls-section { margin-bottom: 20px; }

.search-container,
.filter-panel,
.section {
  border: 1px solid var(--line);
  border-radius: 22px;
  background: rgba(255,255,255,0.02);
}

.search-container { padding: 12px; margin-bottom: 14px; }

#searchInput {
  width: 100%;
  padding: 16px 18px;
  border: 1px solid transparent;
  border-radius: 16px;
  background: rgba(255,255,255,0.04);
  color: var(--text);
  font: inherit;
}

#searchInput:focus {
  outline: none;
  border-color: rgba(142,160,255,0.48);
  box-shadow: 0 0 0 4px rgba(142,160,255,0.12);
}

.filter-panel { padding: 18px; }

.filter-row,
.category-row,
.card-badges,
.badge-row,
.detail-keywords,
.section-chip-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-row {
  justify-content: space-between;
  gap: 12px 24px;
  margin-bottom: 12px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.filter-label {
  color: var(--text-muted);
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

.filter-btn,
.cat-btn,
.copy-btn,
.like-btn {
  min-height: 40px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font: inherit;
}

.filter-btn:hover,
.cat-btn:hover,
.copy-btn:hover,
.like-btn:hover,
.back-link:hover {
  color: var(--text);
  border-color: rgba(255,255,255,0.26);
}

.filter-btn.active,
.cat-btn.active,
.copy-btn.copied,
.like-btn.active {
  background: var(--accent-soft);
  border-color: rgba(142,160,255,0.26);
  color: #e2e6ff;
}

.result-summary {
  margin: 12px 0 0;
  color: var(--text-muted);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.catalog-item {
  display: grid;
  grid-template-columns: 168px 1fr;
  gap: 18px;
  padding: 14px;
  border-radius: 24px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.02);
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.catalog-item:hover {
  transform: translateY(-3px);
  border-color: var(--card-accent, var(--accent));
  background: rgba(255,255,255,0.03);
}

.catalog-item[hidden] { display: none; }

.catalog-preview {
  min-height: 172px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.catalog-preview-mark {
  font-size: 3rem;
  font-weight: 900;
  opacity: 0.66;
}

.catalog-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.catalog-topline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.card-number {
  font-family: var(--mono);
  font-size: 0.76rem;
  color: var(--text-muted);
}

.catalog-category {
  color: var(--text-muted);
  font-size: 0.78rem;
}

.catalog-title {
  margin: 0;
  font-size: 1.4rem;
  line-height: 1.08;
}

.catalog-lead,
.detail-desc,
.section-copy,
.footer-hint,
.catalog-header-copy,
.no-results {
  color: var(--text-muted);
}

.catalog-lead {
  margin: 0;
  line-height: 1.6;
}

.mini-badge,
.catalog-keyword,
.section-chip,
.badge,
.detail-sections {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 0.74rem;
}

.mode-dark { background: #192334; color: #9fb2cb; }
.mode-light { background: #edf1f5; color: #415266; }
.font-serif { background: #f7e9b8; color: #8d5c00; }
.font-sansserif { background: #d9e8ff; color: #1c57cf; }
.font-mono { background: #ccf3e7; color: #08795b; }
.catalog-sections,
.detail-sections { background: rgba(255,255,255,0.06); color: #d1d3e2; }
.cat-badge,
.catalog-keyword,
.section-chip { background: rgba(142,160,255,0.12); color: #d8ddff; border: 1px solid rgba(142,160,255,0.12); }

.catalog-sections-line {
  margin: 0;
  font-size: 0.82rem;
  color: #c1c2d4;
}

.no-results {
  margin-top: 20px;
  padding: 24px;
  border: 1px dashed var(--line);
  border-radius: 20px;
}

.no-results[hidden] { display: none; }

.site-footer {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 18px;
  padding: 0 0 56px;
}

.footer-branding,
.footer-card {
  padding: 20px 22px;
  border: 1px solid var(--line);
  border-radius: 22px;
  background: rgba(255,255,255,0.02);
}

.footer-title {
  margin: 0 0 10px;
  font-size: 1rem;
  color: var(--text);
}

.footer-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.footer-card h3 {
  margin: 0 0 10px;
  font-size: 0.9rem;
  color: var(--text);
}

.footer-card p,
.footer-hint {
  margin: 0;
  color: var(--text-muted);
  line-height: 1.7;
}

.detail-page { padding: 44px 0 70px; }

.detail-header { margin-bottom: 24px; }

.back-link {
  display: inline-flex;
  margin-bottom: 18px;
  color: #cfd4ff;
}

.detail-title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 14px;
  margin: 10px 0 12px;
}

.detail-title-row h1 {
  margin: 0;
  font-size: clamp(2.4rem, 5vw, 4.4rem);
  line-height: 0.95;
}

.detail-grid {
  display: grid;
  grid-template-columns: minmax(260px, 0.72fr) minmax(0, 1.28fr);
  gap: 20px;
}

.detail-sidebar {
  display: grid;
  gap: 18px;
  align-self: start;
  position: sticky;
  top: 84px;
}

.detail-main {
  display: grid;
  gap: 18px;
}

.engagement-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.engagement-card {
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03);
}

.engagement-card span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-muted);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.engagement-card strong {
  font-size: 1.4rem;
  color: var(--text);
}

.section {
  padding: 24px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: start;
  margin-bottom: 18px;
}

.section-title {
  margin: 0 0 6px;
  font-size: 1.08rem;
}

.preview-container {
  overflow: hidden;
  border-radius: 20px;
  border: 1px solid var(--line);
}

.prompt-block {
  margin: 0;
  padding: 20px;
  border-radius: 18px;
  border: 1px solid var(--line);
  background: rgba(5,5,8,0.6);
  font-family: var(--mono);
  font-size: 0.86rem;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: auto;
}

@media (max-width: 1100px) {
  .poster-shell,
  .catalog-header,
  .support-section,
  .detail-grid,
  .cards-grid,
  .site-footer,
  .footer-meta,
  .engagement-grid {
    grid-template-columns: 1fr;
  }

  .detail-sidebar {
    position: static;
  }

  .quick-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 760px) {
  .page-shell,
  .detail-page,
  .masthead-inner {
    width: min(100% - 20px, var(--max));
  }

  .masthead-links {
    gap: 12px;
    font-size: 0.84rem;
  }

  .masthead-inner {
    flex-wrap: wrap;
  }

  .poster-shell {
    padding: 18px;
    min-height: auto;
  }

  .hero-title {
    font-size: clamp(3rem, 18vw, 5rem);
  }

  .quick-stats {
    grid-template-columns: 1fr;
  }

  .catalog-shell,
  .support-section,
  .section {
    padding: 18px;
  }

  .catalog-item {
    grid-template-columns: 1fr;
  }

  .catalog-preview {
    min-height: 126px;
  }

  .section-head {
    flex-direction: column;
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
  <text x="120" y="430" fill="url(#accent)" font-family="JetBrains Mono, monospace" font-size="28">search / filter / preview / copy</text>
</svg>
"""

ASSET_FILES = {
    "app.js": INDEX_SCRIPT,
    "detail.js": DETAIL_SCRIPT,
    "styles.css": STYLESHEET,
    "favicon.svg": FAVICON,
    "og-cover.svg": OG_COVER,
}
