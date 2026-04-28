const state = { mode: 'all', font: 'all', category: 'all', tag: 'all' };
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
    const matchesTag = state.tag === 'all' || (card.dataset.tags || '').split(' ').includes(state.tag);
    const matchesSearch =
      !search ||
      card.dataset.name.includes(search) ||
      card.dataset.mode.includes(search) ||
      card.dataset.font.includes(search) ||
      card.dataset.categorySearch.includes(search) ||
      (card.dataset.keywords || '').includes(search) ||
      card.textContent.toLowerCase().includes(search);

    const isVisible = matchesMode && matchesFont && matchesCategory && matchesTag && matchesSearch;
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
    document.querySelectorAll('[data-topic-tag]').forEach((item) => item.classList.remove('active'));
    document.querySelectorAll('[data-topic-category]').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    state.category = button.dataset.topicCategory;
    state.tag = 'all';
    filterCards();
  });
});

document.querySelectorAll('[data-topic-tag]').forEach((button) => {
  button.addEventListener('click', () => {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.value = '';
    const allCategoryButton = document.querySelector('[data-topic-category="all"]');
    document.querySelectorAll('[data-topic-category]').forEach((item) => item.classList.remove('active'));
    if (allCategoryButton) allCategoryButton.classList.add('active');
    document.querySelectorAll('[data-topic-tag]').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    state.category = 'all';
    state.tag = button.dataset.topicTag;
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
    document.querySelectorAll('[data-topic-tag]').forEach((item) => item.classList.remove('active'));
    state.tag = 'all';
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
