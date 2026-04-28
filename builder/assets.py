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
const featuredUi = readJsonScript('featured-ui-data', { clicksLabel: 'Clicks', likesLabel: 'Likes' });
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

# Refined editorial assets inspired by DESIGN.md/Genesis. The original constants above are
# kept as historical templates; these assignments are the emitted assets.
INDEX_SCRIPT = """const state = { mode: 'all', font: 'all', category: 'all' };
const THEME_STORAGE_KEY = 'dpc-theme-v1';
const CLICK_STORAGE_KEY = 'dpc-click-deltas-v1';
const LIKED_STORAGE_KEY = 'dpc-liked-prompts-v1';
const apiBase = document.body.dataset.apiBase || '../api';

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

function applyTheme(theme) {
  const nextTheme = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = nextTheme;
  document.querySelectorAll('[data-theme-option]').forEach((button) => {
    const active = button.dataset.themeOption === nextTheme;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
  try {
    localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  } catch (error) {
    // Ignore storage failures.
  }
}

function initThemeControls() {
  const initialTheme = document.documentElement.dataset.theme || 'light';
  applyTheme(initialTheme);
  document.querySelectorAll('[data-theme-option]').forEach((button) => {
    button.addEventListener('click', () => applyTheme(button.dataset.themeOption));
  });
}

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

function updateStatContainers(slug, stats) {
  document.querySelectorAll(`[data-stat-for="${slug}"]`).forEach((container) => {
    const clickTarget = container.querySelector('[data-stat-click-count]');
    const likeTarget = container.querySelector('[data-stat-like-count]');
    if (clickTarget) clickTarget.textContent = stats.click_count;
    if (likeTarget) likeTarget.textContent = stats.like_count;
  });
}

function renderTrendingFromItems(items) {
  const root = document.querySelector('.trend-list');
  if (!root || !items.length) return;
  const prompts = promptMap();
  root.innerHTML = items
    .map((item, index) => {
      const prompt = prompts.get(item.slug);
      if (!prompt) return '';
      return `<a href="${escapeHtml(prompt.href)}" class="trend-link" data-trending-item data-track-click data-slug="${escapeHtml(prompt.slug)}" style="--card-accent:${escapeHtml(prompt.accent)};">
  <span class="trend-rank">${String(index + 1).padStart(2, '0')}</span>
  <span class="trend-name">${escapeHtml(prompt.name)}</span>
  <span class="trend-meta">${escapeHtml(prompt.category)}</span>
  <div class="trend-stats" data-stat-for="${escapeHtml(prompt.slug)}">
    <span><strong data-stat-click-count>${item.click_count}</strong> ${escapeHtml(featuredUi.clicksLabel)}</span>
    <span><strong data-stat-like-count>${item.like_count}</strong> ${escapeHtml(featuredUi.likesLabel)}</span>
  </div>
</a>`;
    })
    .join('');
}

function renderTrendingFallback() {
  const ranked = promptIndex
    .map((prompt) => ({ ...prompt, ...getFallbackStats(prompt.slug) }))
    .sort((left, right) => {
      if (right.score !== left.score) return right.score - left.score;
      if (right.like_count !== left.like_count) return right.like_count - left.like_count;
      if (right.click_count !== left.click_count) return right.click_count - left.click_count;
      return left.number - right.number;
    })
    .slice(0, 8);
  renderTrendingFromItems(ranked);
  ranked.forEach((item) => updateStatContainers(item.slug, item));
}

async function refreshTrendingFromApi() {
  if (!promptIndex.length) return false;
  try {
    const response = await fetch(`${apiBase}/featured?limit=8`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    });
    if (!response.ok) return false;
    const payload = await response.json();
    if (!payload.items || !Array.isArray(payload.items)) return false;
    renderTrendingFromItems(payload.items);
    payload.items.forEach((item) => updateStatContainers(item.slug, item));
    return true;
  } catch (error) {
    return false;
  }
}

function setActive(group, button) {
  if (!group) return;
  group.querySelectorAll('[data-selectable]').forEach((item) => item.classList.remove('active'));
  button.classList.add('active');
}

function filterCards() {
  const searchInput = document.getElementById('searchInput');
  const search = searchInput ? searchInput.value.trim().toLowerCase() : '';
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
      card.dataset.categorySearch.includes(search) ||
      (card.dataset.keywords || '').includes(search) ||
      card.textContent.toLowerCase().includes(search);

    const isVisible = matchesMode && matchesFont && matchesCategory && matchesSearch;
    card.hidden = !isVisible;
    if (isVisible) visible += 1;
  });

  const resultCount = document.getElementById('resultCount');
  if (resultCount) {
    const suffix = document.body.dataset.resultsSuffix || 'styles';
    resultCount.textContent = `${visible} ${suffix}`;
  }

  const noResults = document.getElementById('noResults');
  if (noResults) noResults.hidden = visible !== 0;
}

document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const group = button.closest('[data-filter-group]');
    setActive(group, button);
    state[button.dataset.filter] = button.dataset.value;
    filterCards();
  });
});

document.querySelectorAll('[data-topic-category]').forEach((button) => {
  button.addEventListener('click', () => {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.value = '';
    document.querySelectorAll('[data-topic-search]').forEach((item) => item.classList.remove('active'));
    document.querySelectorAll('[data-topic-category]').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    state.category = button.dataset.topicCategory;
    filterCards();
  });
});

document.querySelectorAll('[data-topic-search]').forEach((button) => {
  button.addEventListener('click', () => {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    const allCategoryButton = document.querySelector('[data-topic-category="all"]');
    document.querySelectorAll('[data-topic-category]').forEach((item) => item.classList.remove('active'));
    if (allCategoryButton) allCategoryButton.classList.add('active');
    document.querySelectorAll('[data-topic-search]').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    state.category = 'all';
    searchInput.value = button.dataset.topicSearch;
    filterCards();
  });
});

document.querySelectorAll('[data-locale-link]').forEach((link) => {
  link.addEventListener('click', () => {
    try {
      localStorage.setItem('preferredLocale', link.dataset.locale);
    } catch (error) {
      // Ignore storage failures.
    }
  });
});

const searchInput = document.getElementById('searchInput');
if (searchInput) {
  searchInput.addEventListener('input', () => {
    document.querySelectorAll('[data-topic-search]').forEach((item) => item.classList.remove('active'));
    filterCards();
  });
  document.addEventListener('keydown', (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      searchInput.focus();
    }
  });
}

initThemeControls();
filterCards();
promptIndex.forEach((prompt) => updateStatContainers(prompt.slug, getFallbackStats(prompt.slug)));
renderTrendingFallback();
refreshTrendingFromApi();
"""

DETAIL_SCRIPT = """const THEME_STORAGE_KEY = 'dpc-theme-v1';
const CLICK_STORAGE_KEY = 'dpc-click-deltas-v1';
const LIKED_STORAGE_KEY = 'dpc-liked-prompts-v1';
const CLIENT_ID_KEY = 'dpc-client-id-v1';
const SESSION_ID_KEY = 'dpc-session-id-v1';
const LOCAL_CLICK_MARKS_KEY = 'dpc-local-click-marks-v1';
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

function applyTheme(theme) {
  const nextTheme = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = nextTheme;
  document.querySelectorAll('[data-theme-option]').forEach((button) => {
    const active = button.dataset.themeOption === nextTheme;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
  try {
    localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  } catch (error) {
    // Ignore storage failures.
  }
}

function initThemeControls() {
  const initialTheme = document.documentElement.dataset.theme || 'light';
  applyTheme(initialTheme);
  document.querySelectorAll('[data-theme-option]').forEach((button) => {
    button.addEventListener('click', () => applyTheme(button.dataset.themeOption));
  });
}

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
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

document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;

    const originalLabel = button.textContent;
    try {
      await copyText(target.textContent);
      button.textContent = document.body.dataset.copySuccess || 'Copied';
      button.classList.add('copied');
      window.setTimeout(() => {
        button.textContent = originalLabel;
        button.classList.remove('copied');
      }, 1600);
    } catch (error) {
      button.textContent = document.body.dataset.copyFailed || 'Copy failed';
    }
  });
});

const likeButton = document.querySelector('[data-like-button]');
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

document.querySelectorAll('[data-locale-link]').forEach((link) => {
  link.addEventListener('click', () => {
    try {
      localStorage.setItem('preferredLocale', link.dataset.locale);
    } catch (error) {
      // Ignore storage failures.
    }
  });
});

initThemeControls();
hydratePromptStatsFallback();
trackPromptView();
hydratePromptStatsFromApi();
"""

STYLESHEET = """:root {
  --bg: #fafafa;
  --surface: #ffffff;
  --surface-soft: #f4f4f5;
  --text: #0a0a0a;
  --text-muted: #6b6b6b;
  --text-soft: #9c9c9c;
  --line: #e8e8ec;
  --line-strong: #d7d7df;
  --accent: #6366f1;
  --accent-hover: #4f46e5;
  --secondary: #20970b;
  --dot: #e7e7eb;
  --masthead-bg: rgba(250, 250, 250, 0.88);
  --shadow: rgba(15, 23, 42, 0.08);
  --shadow-soft: rgba(15, 23, 42, 0.06);
  --code-bg: #0f172a;
  --code-text: #e5e7eb;
  --max: 1180px;
  --radius: 8px;
  --sans: 'Inter', sans-serif;
  --mono: 'JetBrains Mono', monospace;
  color-scheme: light;
}

:root[data-theme="dark"] {
  --bg: #0b0c0f;
  --surface: #111318;
  --surface-soft: #171a21;
  --text: #f4f4f5;
  --text-muted: #a1a1aa;
  --text-soft: #71717a;
  --line: #272a33;
  --line-strong: #3a3d48;
  --accent: #8b8df8;
  --accent-hover: #a5a7ff;
  --secondary: #44c05b;
  --dot: #20232b;
  --masthead-bg: rgba(11, 12, 15, 0.86);
  --shadow: rgba(0, 0, 0, 0.32);
  --shadow-soft: rgba(0, 0, 0, 0.24);
  --code-bg: #05070b;
  --code-text: #e5e7eb;
  color-scheme: dark;
}

*,
*::before,
*::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: var(--sans);
  color: var(--text);
  background-color: var(--bg);
  background-image: radial-gradient(var(--dot) 1px, transparent 1px);
  background-size: 22px 22px;
  transition: background-color 0.22s ease, color 0.22s ease;
}

a { color: inherit; text-decoration: none; }

button,
input { font: inherit; }

.page-shell,
.detail-page {
  width: min(var(--max), calc(100% - 32px));
  margin: 0 auto;
}

.masthead {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--line);
  background: var(--masthead-bg);
  backdrop-filter: blur(18px);
}

.masthead-inner {
  width: min(var(--max), calc(100% - 32px));
  min-height: 64px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 20px;
}

.masthead-brand {
  font-weight: 800;
  color: var(--text);
}

.masthead-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  color: var(--text-muted);
  font-size: 0.92rem;
}

.masthead-links a:hover { color: var(--text); }

.masthead-actions {
  justify-self: end;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.lang-switcher,
.theme-switcher {
  display: inline-flex;
  gap: 4px;
  padding: 3px;
  border: 1px solid var(--line);
  border-radius: 7px;
  background: var(--surface);
}

.lang-link,
.theme-option {
  min-width: 42px;
  min-height: 32px;
  padding: 0 10px;
  border: 0;
  border-radius: 5px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.82rem;
  cursor: pointer;
}

.lang-link.active,
.theme-option.active {
  color: #fff;
  background: var(--accent);
}

.theme-option:hover,
.lang-link:hover {
  color: var(--text);
}

.home-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(340px, 0.82fr);
  gap: 56px;
  align-items: center;
  padding: 76px 0 46px;
}

.hero-copy {
  display: grid;
  gap: 22px;
}

.hero-badge,
.section-kicker,
.eyebrow {
  margin: 0;
  color: var(--secondary);
  font-family: var(--mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0;
}

.hero-title {
  margin: 0;
  max-width: 760px;
  font-size: 6.4rem;
  line-height: 0.94;
  letter-spacing: 0;
}

.hero-title span { color: var(--accent); }

.hero-subtitle {
  max-width: 680px;
  margin: 0;
  color: var(--text-muted);
  font-size: 1.08rem;
  line-height: 1.8;
}

.hero-search {
  width: min(100%, 650px);
  min-height: 62px;
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 14px;
  padding: 8px 14px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: 0 18px 42px var(--shadow-soft);
}

.hero-search span {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.76rem;
  text-transform: uppercase;
}

.hero-search input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  color: var(--text);
  background: transparent;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero-meta span,
.topic-chip,
.micro-tags span,
.catalog-keyword,
.section-chip,
.badge,
.mini-badge {
  display: inline-flex;
  min-height: 30px;
  align-items: center;
  padding: 0 10px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text-muted);
  font-size: 0.78rem;
}

.hero-visual {
  display: grid;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: color-mix(in srgb, var(--surface) 82%, transparent);
}

.hero-visual-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-muted);
  font-size: 0.88rem;
}

.hero-visual-head strong {
  color: var(--text);
  font-size: 1.5rem;
}

.hero-card-stack,
.feature-grid,
.cards-grid {
  display: grid;
  gap: 14px;
}

.hero-prompt-card,
.feature-card,
.catalog-item {
  display: grid;
  grid-template-columns: 132px 1fr;
  gap: 16px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
}

.hero-prompt-card:hover,
.feature-card:hover,
.catalog-item:hover {
  transform: translateY(-2px);
  border-color: var(--card-accent, var(--accent));
  box-shadow: 0 16px 34px var(--shadow);
}

.prompt-art,
.catalog-preview {
  min-height: 122px;
  border-radius: 6px;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.prompt-art span,
.catalog-preview-mark {
  font-size: 2.75rem;
  font-weight: 900;
}

.prompt-card-copy,
.catalog-body {
  display: grid;
  gap: 10px;
  align-content: start;
}

.prompt-card-copy h3,
.catalog-title {
  margin: 0;
  font-size: 1.22rem;
  line-height: 1.15;
}

.prompt-card-copy p,
.catalog-lead {
  margin: 0;
  color: var(--text-muted);
  line-height: 1.58;
}

.catalog-topline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.card-number,
.trend-rank,
.added-link span {
  color: var(--text-soft);
  font-family: var(--mono);
  font-size: 0.75rem;
}

.catalog-category {
  color: var(--text-muted);
  font-size: 0.78rem;
}

.micro-tags,
.card-badges,
.catalog-keywords,
.badge-row,
.detail-keywords,
.section-chip-grid,
.topic-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.card-stats,
.trend-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--text-muted);
  font-size: 0.78rem;
}

.card-stats span,
.trend-stats span {
  display: inline-flex;
  gap: 4px;
  align-items: center;
}

.card-stats strong,
.trend-stats strong {
  color: var(--text);
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  overflow: hidden;
  margin: 0 0 54px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--line);
}

.quick-stat {
  padding: 18px;
  background: var(--surface);
}

.quick-stat-value {
  display: block;
  margin-bottom: 8px;
  font-size: 2rem;
  font-weight: 800;
}

.quick-stat-label {
  display: block;
  color: var(--text-muted);
  font-size: 0.76rem;
  text-transform: uppercase;
}

.section-block,
.catalog-shell {
  padding: 46px 0;
  border-top: 1px solid var(--line);
}

.section-block.compact {
  padding: 32px 0 0;
}

.section-heading,
.catalog-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(300px, 420px);
  gap: 32px;
  align-items: start;
  margin-bottom: 24px;
}

.section-heading.stacked {
  grid-template-columns: 1fr;
  gap: 10px;
}

.section-heading h2,
.catalog-header h2 {
  margin: 8px 0 0;
  max-width: 760px;
  font-size: 2.35rem;
  line-height: 1.08;
  letter-spacing: 0;
}

.section-heading p,
.catalog-header-copy {
  margin: 0;
  color: var(--text-muted);
  line-height: 1.7;
}

.split-block {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 44px;
  border-top: 1px solid var(--line);
}

.trend-list,
.added-list {
  display: grid;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--surface);
}

.trend-link,
.added-link {
  display: grid;
  gap: 12px;
  align-items: center;
  min-height: 58px;
  padding: 0 14px;
  border-top: 1px solid var(--line);
}

.trend-link {
  grid-template-columns: 42px minmax(0, 1fr) minmax(110px, auto) auto;
}

.added-link {
  grid-template-columns: 42px minmax(0, 1fr) auto;
}

.trend-link:first-child,
.added-link:first-child { border-top: 0; }

.trend-link:hover,
.added-link:hover { color: var(--card-accent, var(--accent)); }

.trend-name,
.added-link strong {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.trend-meta,
.added-link em {
  color: var(--text-muted);
  font-size: 0.8rem;
  font-style: normal;
}

.trend-stats {
  justify-self: end;
  white-space: nowrap;
}

.catalog-tools {
  display: grid;
  gap: 12px;
  margin-bottom: 18px;
}

.topic-panel {
  display: grid;
  grid-template-columns: minmax(180px, 0.38fr) minmax(0, 1fr);
  gap: 18px;
  align-items: start;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: color-mix(in srgb, var(--surface) 88%, transparent);
}

.topic-copy {
  margin: 8px 0 0;
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 0.9rem;
}

.topic-chip {
  min-height: 34px;
  background: var(--surface);
  cursor: pointer;
}

.topic-chip:hover,
.topic-chip.active {
  border-color: var(--accent);
  color: var(--accent);
}

.topic-chip.active {
  background: color-mix(in srgb, var(--accent) 12%, var(--surface));
}

.topic-chip.subtle {
  background: transparent;
}

.filter-panel {
  padding: 14px;
  margin-bottom: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
}

.catalog-tools .filter-panel {
  margin-bottom: 0;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  gap: 12px 24px;
  margin-bottom: 12px;
}

.filter-group,
.category-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.filter-label {
  color: var(--text-muted);
  font-family: var(--mono);
  font-size: 0.72rem;
  text-transform: uppercase;
}

.filter-btn,
.cat-btn,
.copy-btn,
.like-btn {
  min-height: 36px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text-muted);
  cursor: pointer;
}

.filter-btn:hover,
.cat-btn:hover,
.copy-btn:hover,
.back-link:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.filter-btn.active,
.cat-btn.active,
.copy-btn.copied {
  border-color: var(--accent);
  background: var(--accent);
  color: #fff;
}

.copy-btn.primary {
  width: 100%;
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.result-summary {
  margin: 12px 0 0;
  color: var(--text-muted);
}

.cards-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.catalog-item[hidden] { display: none; }

.mode-dark { background: #111827; color: #e5e7eb; }
.mode-light { background: #f1f5f9; color: #334155; }
.font-serif { background: #fef3c7; color: #92400e; }
.font-sansserif { background: #dbeafe; color: #1d4ed8; }
.font-mono { background: #d1fae5; color: #047857; }
.catalog-sections,
.detail-sections { background: #f4f4f5; color: var(--text-muted); }
.cat-badge,
.catalog-keyword,
.section-chip { background: #eef2ff; color: #3730a3; border-color: #dfe3ff; }

.catalog-sections-line,
.no-results,
.footer-hint,
.detail-desc,
.section-copy {
  color: var(--text-muted);
}

.catalog-sections-line {
  margin: 0;
  font-size: 0.82rem;
}

.no-results {
  margin-top: 20px;
  padding: 24px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius);
  background: var(--surface);
}

.no-results[hidden] { display: none; }

.site-footer {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding: 32px 0 56px;
  border-top: 1px solid var(--line);
}

.footer-title,
.footer-hint {
  margin: 0;
}

.footer-title {
  font-weight: 800;
}

.footer-hint {
  max-width: 620px;
  line-height: 1.7;
  text-align: right;
}

.detail-page { padding: 42px 0 70px; }

.detail-hero {
  padding: 22px 0 38px;
  border-bottom: 1px solid var(--line);
}

.back-link {
  display: inline-flex;
  margin-bottom: 18px;
  color: var(--text-muted);
}

.detail-hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 36px;
  align-items: end;
}

.detail-title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 14px;
  margin: 10px 0 16px;
}

.detail-title-row h1 {
  margin: 0;
  font-size: 5rem;
  line-height: 0.95;
  letter-spacing: 0;
}

.detail-kicker {
  color: var(--prompt-accent, var(--accent));
  font-family: var(--mono);
}

.detail-desc {
  max-width: 760px;
  margin: 0;
  font-size: 1.04rem;
  line-height: 1.8;
}

.detail-tabs {
  display: flex;
  gap: 8px;
  margin-top: 22px;
}

.detail-tabs a {
  min-height: 36px;
  display: inline-flex;
  align-items: center;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text-muted);
}

.detail-tabs a:hover {
  border-color: var(--prompt-accent, var(--accent));
  color: var(--prompt-accent, var(--accent));
}

.detail-meta-panel,
.section {
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
}

.detail-meta-panel p {
  margin: 16px 0 0;
  color: var(--text-muted);
  line-height: 1.7;
}

.detail-layout {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 20px;
  padding-top: 22px;
}

.detail-sidebar {
  display: grid;
  gap: 14px;
  align-self: start;
  position: sticky;
  top: 84px;
}

.detail-main {
  display: grid;
  gap: 14px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: start;
  margin-bottom: 18px;
}

.section-title {
  margin: 0 0 8px;
  font-size: 1.1rem;
}

.section-copy {
  margin: 0 0 14px;
  line-height: 1.7;
}

.engagement-head {
  display: grid;
  gap: 12px;
}

.like-btn {
  width: 100%;
}

.like-btn:hover,
.like-btn.active {
  border-color: var(--accent);
  background: var(--accent);
  color: #fff;
}

.engagement-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.engagement-card {
  min-width: 0;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface-soft);
}

.engagement-card span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 0.76rem;
}

.engagement-card strong {
  color: var(--text);
  font-size: 1.25rem;
}

.preview-container {
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: var(--radius);
}

.palette-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.palette-item {
  display: grid;
  gap: 8px;
  min-width: 0;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface-soft);
}

.palette-swatch {
  width: 100%;
  height: 58px;
  border: 1px solid rgba(10, 10, 10, 0.1);
  border-radius: 6px;
}

.palette-item code {
  overflow: hidden;
  color: var(--text-muted);
  font-family: var(--mono);
  font-size: 0.72rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.type-panel {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 18px;
  align-items: center;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface-soft);
}

.type-spec.display {
  display: grid;
  place-items: center;
  min-height: 150px;
  border-radius: 6px;
  background: var(--surface);
  font-size: 4rem;
  font-weight: 900;
}

.type-spec-copy span {
  color: var(--text-muted);
  font-family: var(--mono);
  font-size: 0.75rem;
  text-transform: uppercase;
}

.type-spec-copy strong {
  display: block;
  margin: 8px 0;
  font-size: 2rem;
}

.type-spec-copy p {
  margin: 0;
  color: var(--text-muted);
  line-height: 1.7;
}

.anatomy-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.anatomy-item {
  min-height: 68px;
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 10px;
  align-items: center;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface-soft);
}

.anatomy-item span {
  color: var(--text-soft);
  font-family: var(--mono);
  font-size: 0.78rem;
}

.prompt-block {
  margin: 0;
  max-height: 680px;
  padding: 18px;
  overflow: auto;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--code-bg);
  color: var(--code-text);
  font-family: var(--mono);
  font-size: 0.86rem;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
}

@media (max-width: 1100px) {
  .home-hero,
  .section-heading,
  .catalog-header,
  .topic-panel,
  .split-block,
  .detail-hero-grid,
  .detail-layout,
  .cards-grid,
  .palette-grid {
    grid-template-columns: 1fr;
  }

  .detail-sidebar {
    position: static;
  }

  .hero-title,
  .detail-title-row h1 {
    font-size: 4.6rem;
  }
}

@media (max-width: 760px) {
  .page-shell,
  .detail-page,
  .masthead-inner {
    width: min(100% - 20px, var(--max));
  }

  .masthead-inner {
    grid-template-columns: 1fr auto;
    min-height: auto;
    padding: 10px 0;
  }

  .masthead-links {
    grid-column: 1 / -1;
    justify-content: flex-start;
    gap: 14px;
    overflow-x: auto;
  }

  .home-hero {
    gap: 26px;
    padding: 42px 0 30px;
  }

  .hero-title,
  .detail-title-row h1 {
    font-size: 3.35rem;
  }

  .hero-search {
    grid-template-columns: 1fr;
  }

  .hero-prompt-card,
  .feature-card,
  .catalog-item,
  .type-panel {
    grid-template-columns: 1fr;
  }

  .quick-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-row,
  .section-head,
  .site-footer {
    flex-direction: column;
  }

  .site-footer {
    display: grid;
  }

  .footer-hint {
    text-align: left;
  }

  .trend-link,
  .added-link {
    grid-template-columns: 36px minmax(0, 1fr);
  }

  .trend-meta,
  .added-link em,
  .trend-stats {
    grid-column: 2;
    justify-self: start;
  }

  .anatomy-grid {
    grid-template-columns: 1fr;
  }

  .preview-headline {
    font-size: 2.25rem !important;
  }

  .preview-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }

  .preview-features-grid {
    grid-template-columns: 1fr !important;
  }
}
"""

ASSET_FILES = {
    "app.js": INDEX_SCRIPT,
    "detail.js": DETAIL_SCRIPT,
    "styles.css": STYLESHEET,
    "favicon.svg": FAVICON,
    "og-cover.svg": OG_COVER,
}
