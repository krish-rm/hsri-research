import { writable, derived } from 'svelte/store';
import { en, type LocaleKey } from './en';
import { rtlStub } from './rtl-stub';

const STORAGE_KEY = 'hr:v1:locale';

function readInitialLocale(): LocaleKey {
  if (typeof window === 'undefined') return 'en';
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved === 'rtl-stub' ? 'rtl-stub' : 'en';
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

function applyLocaleToDocument(locale: LocaleKey) {
  if (typeof document === 'undefined') return;
  const dir = locale === 'rtl-stub' ? 'rtl' : 'ltr';
  if (document.documentElement.getAttribute('dir') !== dir) {
    document.documentElement.setAttribute('dir', dir);
  }
  if (document.documentElement.getAttribute('data-locale-mode') !== locale) {
    document.documentElement.setAttribute('data-locale-mode', locale);
  }
}

export const dict = derived(activeLocale, ($loc) => ($loc === 'rtl-stub' ? rtlStub : en));
