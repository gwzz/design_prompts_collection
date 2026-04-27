const KV_URL =
  process.env.KV_REST_API_URL ||
  process.env.prompt_collection_KV_REST_API_URL;

const KV_TOKEN =
  process.env.KV_REST_API_TOKEN ||
  process.env.prompt_collection_KV_REST_API_TOKEN;

export function hasRedisConfig() {
  return Boolean(KV_URL && KV_TOKEN);
}

async function fetchRedis(pathname = '', body = undefined) {
  if (!hasRedisConfig()) {
    throw new Error('Missing KV_REST_API_URL or KV_REST_API_TOKEN');
  }

  const url = pathname ? `${KV_URL}${pathname}` : KV_URL;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${KV_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  const json = await response.json();
  if (!response.ok || json.error) {
    throw new Error(json.error || `Redis request failed with ${response.status}`);
  }
  return json.result;
}

export async function redisCommand(...command) {
  return fetchRedis('', command);
}

export async function redisPipeline(commands) {
  const response = await fetchRedis('/pipeline', commands);
  return response.map((item) => {
    if (item.error) {
      throw new Error(item.error);
    }
    return item.result;
  });
}
