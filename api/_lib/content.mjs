import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..', '..');
const CONTENT_DIR = path.join(ROOT_DIR, 'content');
const PROMPTS_DIR = path.join(CONTENT_DIR, 'prompts');

let cachedSeed = null;
let cachedSite = null;
let cachedPrompts = null;

async function readJson(filePath) {
  const raw = await readFile(filePath, 'utf8');
  return JSON.parse(raw.replace(/^\uFEFF/, ''));
}

export async function loadFeaturedSeed() {
  if (!cachedSeed) {
    cachedSeed = await readJson(path.join(CONTENT_DIR, 'featured_stats.json'));
  }
  return cachedSeed;
}

export async function loadSiteConfig() {
  if (!cachedSite) {
    cachedSite = await readJson(path.join(CONTENT_DIR, 'site.json'));
  }
  return cachedSite;
}

export async function loadPromptSummaries() {
  if (cachedPrompts) {
    return cachedPrompts;
  }

  const directories = await readdir(PROMPTS_DIR, { withFileTypes: true });
  const prompts = [];

  for (const entry of directories) {
    if (!entry.isDirectory() || entry.name.startsWith('_')) {
      continue;
    }

    const promptPath = path.join(PROMPTS_DIR, entry.name, 'prompt.json');
    const prompt = await readJson(promptPath);
    prompts.push({
      slug: prompt.slug,
      number: prompt.number,
      name: prompt.name,
    });
  }

  cachedPrompts = prompts.sort((left, right) => left.number - right.number);
  return cachedPrompts;
}
