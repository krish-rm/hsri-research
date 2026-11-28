import heritageIndexRaw from '../data/heritage/index.json';
import {
  toPlayableHeritageWish,
  type HeritageFullRecord,
  type HeritageIndexEntry,
  type PlayableHeritageWish
} from './heritageTypes';

export const HERITAGE_INDEX: HeritageIndexEntry[] =
  heritageIndexRaw as unknown as HeritageIndexEntry[];

const scriptLoaders = import.meta.glob('../data/heritage/scripts/*.json');

const loadedCache = new Map<string, PlayableHeritageWish>();

export function findHeritageForCountryAndDoor(
  iso: string | null | undefined,
  door: string
): HeritageIndexEntry | null {
  if (!iso || iso === 'GLOBAL') return null;
  const code = iso.toUpperCase();
  return HERITAGE_INDEX.find((h) => h.door === door && h.countries.includes(code)) ?? null;
}

export function findAnyHeritageForCountry(
  iso: string | null | undefined
): HeritageIndexEntry | null {
  if (!iso || iso === 'GLOBAL') return null;
  const code = iso.toUpperCase();
  return HERITAGE_INDEX.find((h) => h.countries.includes(code)) ?? null;
}

export function doorHasHeritageForCountry(
  iso: string | null | undefined,
  door: string
): boolean {
  return findHeritageForCountryAndDoor(iso, door) !== null;
}

export async function loadHeritageBreakthrough(
  id: string
): Promise<PlayableHeritageWish | null> {
  if (loadedCache.has(id)) return loadedCache.get(id)!;
  const matchKey = Object.keys(scriptLoaders).find((k) => k.endsWith(`/${id}.json`));
  if (!matchKey) return null;
  const mod = (await scriptLoaders[matchKey]()) as { default?: HeritageFullRecord } | HeritageFullRecord;
  const rec = ((mod as { default?: HeritageFullRecord }).default ?? mod) as HeritageFullRecord;
  const playable = toPlayableHeritageWish(rec);
  loadedCache.set(id, playable);
  return playable;
}
