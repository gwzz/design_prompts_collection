import { badRequest, jsonResponse, loadStatsSnapshot, readLikedState, setLikeState } from '../_lib/stats.mjs';

export async function POST(request) {
  const body = await request.json().catch(() => null);
  const slug = body?.slug?.trim?.() || '';
  const clientId = body?.clientId?.trim?.() || '';
  const liked = Boolean(body?.liked);

  if (!slug || !clientId) {
    return badRequest('Missing slug or clientId');
  }

  const snapshot = await loadStatsSnapshot();
  if (!snapshot.promptMap.has(slug)) {
    return badRequest('Unknown prompt slug', 404);
  }

  try {
    await setLikeState(slug, clientId, liked);
  } catch (error) {
    return jsonResponse({ error: error instanceof Error ? error.message : 'Like update failed' }, { status: 503 });
  }

  const refreshed = await loadStatsSnapshot();
  const prompt = refreshed.promptMap.get(slug);
  const currentLiked = await readLikedState(slug, clientId);

  return jsonResponse({
    slug,
    liked: currentLiked,
    click_count: prompt.click_count,
    like_count: prompt.like_count,
    score: prompt.score,
  });
}
