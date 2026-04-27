const state = { mode: 'all', font: 'all', category: 'all' };
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
