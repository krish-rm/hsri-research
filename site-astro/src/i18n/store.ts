import { writable, derived } from 'svelte/store';
import { en, type LocaleKey, type TranslationDict } from './en';
import { es } from './es';
import { ar } from './ar';
import { rtlStub } from './rtl-stub';

const STORAGE_KEY = 'hr:v1:locale';

const DICTIONARIES: Record<LocaleKey, TranslationDict> = {
  en,
  es,
  ar,
  'rtl-stub': rtlStub
};

export function normalizeLocale(val: string | null | undefined): LocaleKey {
  if (val === 'es' || val === 'ar' || val === 'rtl-stub') return val;
  return 'en';
}

function readInitialLocale(): LocaleKey {
  if (typeof window === 'undefined') return 'en';
  try {
    return normalizeLocale(localStorage.getItem(STORAGE_KEY));
  } catch {
    return 'en';
  }
}

export const activeLocale = writable<LocaleKey>('en');

export function initLocale() {
  const initial = readInitialLocale();
  applyLocaleToDocument(initial);
  activeLocale.set(initial);
}

export function setLocale(next: LocaleKey) {
  applyLocaleToDocument(next);
  activeLocale.set(next);
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // Ignore private browsing quota errors
    }
  }
}

function resolveKeyPath(obj: Record<string, any>, path: string): unknown {
  return path.split('.').reduce((acc, part) => (acc == null ? undefined : acc[part]), obj as any);
}

function syncStaticDomTranslations(currentDict: TranslationDict) {
  if (typeof document === 'undefined') return;
  const nodes = document.querySelectorAll<HTMLElement>('[data-hr-t]');
  nodes.forEach((el) => {
    const key = el.getAttribute('data-hr-t');
    if (!key) return;
    const val = resolveKeyPath(currentDict as unknown as Record<string, any>, key);
    if (typeof val === 'string') {
      el.textContent = val;
    }
  });
}

function applyLocaleToDocument(locale: LocaleKey) {
  if (typeof document === 'undefined') return;
  const d = DICTIONARIES[locale] ?? en;
  const html = document.documentElement;
  if (html.getAttribute('dir') !== d.dir) {
    html.setAttribute('dir', d.dir);
  }
  if (html.getAttribute('lang') !== d.lang) {
    html.setAttribute('lang', d.lang);
  }
  if (html.getAttribute('data-locale-mode') !== locale) {
    html.setAttribute('data-locale-mode', locale);
  }
  syncStaticDomTranslations(d);
}

export const dict = derived(activeLocale, ($loc) => DICTIONARIES[$loc] ?? en);
