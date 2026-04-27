const CLICK_STORAGE_KEY = 'dpc-click-deltas-v1';
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
