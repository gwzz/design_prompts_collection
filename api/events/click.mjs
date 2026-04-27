import { badRequest, incrementClick, jsonResponse, loadStatsSnapshot } from '../_lib/stats.mjs';

export async function POST(request) {
  const body = await request.json().catch(() => null);
  const slug = body?.slug?.trim?.() || '';
  const sessionId = body?.sessionId?.trim?.() || '';

  if (!slug || !sessionId) {
    return badRequest('Missing slug or sessionId');
  }

  const snapshot = await loadStatsSnapshot();
  if (!snapshot.promptMap.has(slug)) {
    return badRequest('Unknown prompt slug', 404);
  }

  let accepted = false;
  try {
    accepted = await incrementClick(slug, sessionId);
  } catch (error) {
    return jsonResponse({ error: error instanceof Error ? error.message : 'Click tracking failed' }, { status: 503 });
  }

  const refreshed = await loadStatsSnapshot();
  const prompt = refreshed.promptMap.get(slug);

  return jsonResponse({
    slug,
    accepted,
    click_count: prompt.click_count,
    like_count: prompt.like_count,
    score: prompt.score,
  });
}
