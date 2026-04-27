import { badRequest, jsonResponse, loadStatsSnapshot, readLikedState } from './_lib/stats.mjs';

export async function GET(request) {
  const url = new URL(request.url);
  const slug = (url.searchParams.get('slug') || '').trim();
  const clientId = (url.searchParams.get('clientId') || '').trim();

  if (!slug) {
    return badRequest('Missing slug');
  }

  const snapshot = await loadStatsSnapshot();
  const prompt = snapshot.promptMap.get(slug);
  if (!prompt) {
    return badRequest('Unknown prompt slug', 404);
  }

  const liked = clientId ? await readLikedState(slug, clientId) : false;

  return jsonResponse({
    slug,
    click_count: prompt.click_count,
    like_count: prompt.like_count,
    score: prompt.score,
    liked,
    generated_at: new Date().toISOString(),
  });
}
