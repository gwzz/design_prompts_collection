import { jsonResponse, loadStatsSnapshot, rankPromptStats } from './_lib/stats.mjs';

export async function GET(request) {
  const url = new URL(request.url);
  const limit = Math.max(1, Math.min(Number.parseInt(url.searchParams.get('limit') || '3', 10), 12));
  const snapshot = await loadStatsSnapshot();
  const items = rankPromptStats(snapshot.promptMap, limit).map((prompt) => ({
    slug: prompt.slug,
    click_count: prompt.click_count,
    like_count: prompt.like_count,
    score: prompt.score,
  }));

  return jsonResponse({
    items,
    weights: snapshot.weights,
    generated_at: new Date().toISOString(),
  });
}
