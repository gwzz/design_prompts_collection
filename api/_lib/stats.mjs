import { hasRedisConfig, redisCommand, redisPipeline } from './redis.mjs';
import { loadFeaturedSeed, loadPromptSummaries, loadSiteConfig } from './content.mjs';

const CLICK_HASH_KEY = 'dpc:stats:clicks';
const LIKE_HASH_KEY = 'dpc:stats:likes';
const CLICK_DEDUPE_PREFIX = 'dpc:clickdedupe';
const LIKE_CLIENT_PREFIX = 'dpc:likes';
const CLICK_TTL_SECONDS = 60 * 30;

function toInt(value) {
  const parsed = Number.parseInt(String(value ?? 0), 10);
  return Number.isFinite(parsed) ? parsed : 0;
}

export function jsonResponse(data, init = {}) {
  return new Response(JSON.stringify(data), {
    status: init.status || 200,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...init.headers,
    },
  });
}

export async function readJson(request) {
  try {
    return await request.json();
  } catch (error) {
    return null;
  }
}

export function badRequest(message, status = 400) {
  return jsonResponse({ error: message }, { status });
}

export async function loadStatsSnapshot() {
  const [seed, prompts, siteConfig] = await Promise.all([
    loadFeaturedSeed(),
    loadPromptSummaries(),
    loadSiteConfig(),
  ]);

  const fallbackRank = new Map(
    (siteConfig.featured_prompt_slugs || []).map((slug, index) => [slug, index])
  );
  const seededPrompts = seed.prompts || {};
  const weights = seed.weights || { click: 1, like: 5 };

  let clickDeltas = [];
  let likeDeltas = [];

  if (hasRedisConfig() && prompts.length) {
    clickDeltas = await redisCommand('HMGET', CLICK_HASH_KEY, ...prompts.map((prompt) => prompt.slug));
    likeDeltas = await redisCommand('HMGET', LIKE_HASH_KEY, ...prompts.map((prompt) => prompt.slug));
  }

  const promptMap = new Map();
  prompts.forEach((prompt, index) => {
    const seeded = seededPrompts[prompt.slug] || {};
    const clickCount = toInt(seeded.click_count) + toInt(clickDeltas[index]);
    const likeCount = toInt(seeded.like_count) + toInt(likeDeltas[index]);
    promptMap.set(prompt.slug, {
      ...prompt,
      click_count: clickCount,
      like_count: likeCount,
      score: clickCount * toInt(weights.click || 1) + likeCount * toInt(weights.like || 5),
      fallback_rank: fallbackRank.has(prompt.slug) ? fallbackRank.get(prompt.slug) : 999,
    });
  });

  return {
    weights,
    prompts,
    siteConfig,
    promptMap,
  };
}

export function rankPromptStats(promptMap, limit) {
  const ranked = [...promptMap.values()].sort((left, right) => {
    if (right.score !== left.score) return right.score - left.score;
    if (right.like_count !== left.like_count) return right.like_count - left.like_count;
    if (right.click_count !== left.click_count) return right.click_count - left.click_count;
    if (left.fallback_rank !== right.fallback_rank) return left.fallback_rank - right.fallback_rank;
    return left.number - right.number;
  });
  return typeof limit === 'number' ? ranked.slice(0, limit) : ranked;
}

export async function incrementClick(slug, sessionId) {
  if (!hasRedisConfig()) {
    throw new Error('Redis is not configured');
  }

  const dedupeKey = `${CLICK_DEDUPE_PREFIX}:${slug}:${sessionId}`;
  const dedupe = await redisCommand('SET', dedupeKey, '1', 'EX', CLICK_TTL_SECONDS, 'NX');
  if (dedupe === 'OK') {
    await redisCommand('HINCRBY', CLICK_HASH_KEY, slug, 1);
    return true;
  }
  return false;
}

export async function setLikeState(slug, clientId, liked) {
  if (!hasRedisConfig()) {
    throw new Error('Redis is not configured');
  }

  const clientKey = `${LIKE_CLIENT_PREFIX}:${slug}`;
  if (liked) {
    const added = await redisCommand('SADD', clientKey, clientId);
    if (toInt(added) > 0) {
      await redisCommand('HINCRBY', LIKE_HASH_KEY, slug, 1);
    }
  } else {
    const removed = await redisCommand('SREM', clientKey, clientId);
    if (toInt(removed) > 0) {
      await redisCommand('HINCRBY', LIKE_HASH_KEY, slug, -1);
    }
  }
}

export async function readLikedState(slug, clientId) {
  if (!hasRedisConfig()) {
    return false;
  }
  const clientKey = `${LIKE_CLIENT_PREFIX}:${slug}`;
  const result = await redisCommand('SISMEMBER', clientKey, clientId);
  return toInt(result) === 1;
}
