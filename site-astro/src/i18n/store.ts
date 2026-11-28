import { writable, derived } from 'svelte/store';
import { en, type TranslationDict } from './en';
import { rtlStub } from './rtl-stub';
import { getLocaleMeta, normalizeLocale, type LocaleKey } from './locales';
import type { StoryLocalePack } from './storyTypes';

export {
  normalizeLocale,
  getLocaleMeta,
  getCountryDisplayName,
  SUPPORTED_LOCALES,
  type LocaleKey,
  type LocaleCode
} from './locales';

const STORAGE_KEY = 'hr:v1:locale';

type DynamicDictLoader = () => Promise<TranslationDict>;
type DynamicStoryLoader = () => Promise<StoryLocalePack>;

const DICT_LOADERS: Partial<Record<LocaleKey, DynamicDictLoader>> = {
  es: () => import('./es').then((m) => m.es),
  ar: () => import('./ar').then((m) => m.ar),
  zh: () => import('./zh').then((m) => m.zh),
  hi: () => import('./hi').then((m) => m.hi),
  fr: () => import('./fr').then((m) => m.fr),
  pt: () => import('./pt').then((m) => m.pt),
  bn: () => import('./bn').then((m) => m.bn),
  ru: () => import('./ru').then((m) => m.ru),
  id: () => import('./id').then((m) => m.id),
  ja: () => import('./ja').then((m) => m.ja),
  de: () => import('./de').then((m) => m.de),
  ko: () => import('./ko').then((m) => m.ko),
  sw: () => import('./sw').then((m) => m.sw)
};

const STORY_LOADERS: Partial<Record<LocaleKey, DynamicStoryLoader>> = {
  zh: () => import('./stories/zh').then((m) => m.zhStories),
  hi: () => import('./stories/hi').then((m) => m.hiStories),
  fr: () => import('./stories/fr').then((m) => m.frStories),
  pt: () => import('./stories/pt').then((m) => m.ptStories),
  bn: () => import('./stories/bn').then((m) => m.bnStories),
  ru: () => import('./stories/ru').then((m) => m.ruStories),
  id: () => import('./stories/id').then((m) => m.idStories),
  ja: () => import('./stories/ja').then((m) => m.jaStories),
  de: () => import('./stories/de').then((m) => m.deStories),
  ko: () => import('./stories/ko').then((m) => m.koStories),
  sw: () => import('./stories/sw').then((m) => m.swStories)
};

const dictCache: Partial<Record<LocaleKey, TranslationDict>> = {
  en,
  'rtl-stub': rtlStub
};

const storyCache: Partial<Record<LocaleKey, StoryLocalePack>> = {};
const dictVersion = writable(0);

export const activeLocale = writable<LocaleKey>('en');
export const localeLoading = writable(false);

function readInitialLocale(): LocaleKey {
  if (typeof window === 'undefined') return 'en';
  try {
    const params = new URLSearchParams(window.location.search);
    const paramLoc = params.get('lang');
    if (paramLoc) {
      const normalized = normalizeLocale(paramLoc);
      try {
        localStorage.setItem(STORAGE_KEY, normalized);
      } catch {
        // Ignore private browsing errors
      }
      return normalized;
    }
    return normalizeLocale(localStorage.getItem(STORAGE_KEY));
  } catch {
    return 'en';
  }
}

async function ensureLocaleLoaded(loc: LocaleKey): Promise<TranslationDict> {
  if (dictCache[loc]) {
    if (STORY_LOADERS[loc] && !storyCache[loc]) {
      storyCache[loc] = await STORY_LOADERS[loc]!();
      dictVersion.update((n) => n + 1);
    }
    return dictCache[loc]!;
  }
  const dictLoader = DICT_LOADERS[loc];
  if (!dictLoader) return en;

  const [loadedDict, loadedStory] = await Promise.all([
    dictLoader(),
    STORY_LOADERS[loc] ? STORY_LOADERS[loc]!() : Promise.resolve(undefined)
  ]);

  dictCache[loc] = loadedDict;
  if (loadedStory) storyCache[loc] = loadedStory;
  dictVersion.update((n) => n + 1);
  return loadedDict;
}

let localeInitialized = false;
let initPromise: Promise<void> | null = null;

export async function initLocale(): Promise<void> {
  if (localeInitialized) return initPromise ?? Promise.resolve();
  localeInitialized = true;
  initPromise = (async () => {
    const initial = readInitialLocale();
    applyMetaToDocument(initial, dictCache[initial] ?? en);
    activeLocale.set(initial);
    if (initial !== 'en' && initial !== 'rtl-stub') {
      localeLoading.set(true);
      try {
        const d = await ensureLocaleLoaded(initial);
        applyMetaToDocument(initial, d);
      } finally {
        localeLoading.set(false);
      }
    }
  })();
  return initPromise;
}

export async function setLocale(rawNext: LocaleKey | string): Promise<void> {
  localeInitialized = true;
  const next = normalizeLocale(rawNext);
  applyMetaToDocument(next, dictCache[next] ?? en);
  activeLocale.set(next);

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEY, next);
      const url = new URL(window.location.href);
      if (url.searchParams.has('lang')) {
        url.searchParams.set('lang', next);
        window.history.replaceState(null, '', url.toString());
      }
    } catch {
      // Ignore private browsing quota errors
    }
  }

  if (next !== 'en' && next !== 'rtl-stub' && (!dictCache[next] || (STORY_LOADERS[next] && !storyCache[next]))) {
    localeLoading.set(true);
    try {
      const d = await ensureLocaleLoaded(next);
      applyMetaToDocument(next, d);
    } finally {
      localeLoading.set(false);
    }
  }
}

function resolveKeyPath(obj: Record<string, unknown>, path: string): unknown {
  return path.split('.').reduce<unknown>((acc, part) => {
    if (acc && typeof acc === 'object') return (acc as Record<string, unknown>)[part];
    return undefined;
  }, obj);
}

function syncStaticDomTranslations(currentDict: TranslationDict) {
  if (typeof document === 'undefined') return;
  const nodes = document.querySelectorAll<HTMLElement>('[data-hr-t]');
  nodes.forEach((el) => {
    const key = el.getAttribute('data-hr-t');
    if (!key) return;
    const val = resolveKeyPath(currentDict as unknown as Record<string, unknown>, key);
    if (typeof val === 'string') {
      el.textContent = val;
    }
  });
}

function applyMetaToDocument(locale: LocaleKey, d: TranslationDict) {
  if (typeof document === 'undefined') return;
  const meta = getLocaleMeta(locale);
  const html = document.documentElement;
  if (html.getAttribute('dir') !== meta.dir) {
    html.setAttribute('dir', meta.dir);
  }
  if (html.getAttribute('lang') !== meta.code) {
    html.setAttribute('lang', meta.code);
  }
  if (html.getAttribute('data-locale-mode') !== locale) {
    html.setAttribute('data-locale-mode', locale);
  }
  syncStaticDomTranslations(d);
}

export const dict = derived([activeLocale, dictVersion], ([$loc]) => {
  return dictCache[$loc] ?? en;
});

export const storyOverlay = derived([activeLocale, dictVersion], ([$loc]): StoryLocalePack | null => {
  return storyCache[$loc] ?? null;
});
