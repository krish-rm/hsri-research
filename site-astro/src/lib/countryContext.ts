import { writable } from 'svelte/store';
import { findCityById, type CountrySky } from './countrySkies';

export interface CountryContextState {
  iso: string;
  cityId: string;
  countryName: string;
  explicit: boolean;
  highlightChecklistIdx: number | null;
}

const DEFAULT_CTX: CountryContextState = {
  iso: 'GLOBAL',
  cityId: 'neutral',
  countryName: 'Global',
  explicit: false,
  highlightChecklistIdx: null
};

export const countryContextStore = writable<CountryContextState>(DEFAULT_CTX);

export function getCountryParamFromUrl(): CountrySky | null {
  if (typeof window === 'undefined') return null;
  try {
    const q = new URLSearchParams(window.location.search).get('c');
    if (!q) return null;
    const match = findCityById(q);
    return match && (match.id === q.toLowerCase() || match.iso.toLowerCase() === q.toLowerCase())
      ? match
      : null;
  } catch {
    return null;
  }
}

export function syncCountryContext(
  sky: CountrySky,
  explicit: boolean,
  highlightChecklistIdx: number | null = null
) {
  countryContextStore.set({
    iso: sky.iso,
    cityId: sky.id,
    countryName: sky.country,
    explicit,
    highlightChecklistIdx
  });

  if (explicit && typeof window !== 'undefined') {
    try {
      const url = new URL(window.location.href);
      if (sky.iso === 'GLOBAL') {
        url.searchParams.delete('c');
      } else {
        url.searchParams.set('c', sky.iso);
      }
      window.history.replaceState({}, '', url.toString());
    } catch {
      // Ignore history API restrictions
    }
  }
}

export function focusSafeguardInCountryCheck(isoOrId: string, checklistIdx: number) {
  const sky = findCityById(isoOrId);
  syncCountryContext(sky, true, checklistIdx);
  if (typeof document !== 'undefined') {
    document.getElementById('country-check')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}
