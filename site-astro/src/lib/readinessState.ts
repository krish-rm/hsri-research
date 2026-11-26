// Local-first state for the 5 Readiness Lights, completed breakthroughs, Trail Card & Shadow Map
// Internal hr:v1:* keys (including hr:v1:wishes) are preserved unchanged for saved-progress compatibility.
// All data stored strictly on the visitor's browser (zero PII, zero network transmission).
import { writable, derived } from 'svelte/store';
import { trackEvent } from './privacyStorage';

export type LightKey = 'Clarity' | 'Foresight' | 'Fairness' | 'Wisdom' | 'Capability';
export type ShadowKey = 'Control' | 'Dependence' | 'Power' | 'Truth' | 'Speed';
export type TrailArchetypeKey = 'Verifier' | 'Neighbour' | 'Builder' | 'Keeper';

export interface CompletedWishEntry {
  wishId: string;
  wishTitle: string;
  guessedWobble: boolean;
  weightChoiceId: 'a' | 'b' | 'c';
  weightLight: LightKey;
  weightShadow: ShadowKey;
  pledged: boolean;
  durationSec: number;
  completedAt: string;
}

export interface SelectedCountryRef {
  iso: string;
  name: string;
  kind: 'rated' | 'unrated';
  checklistCount?: number;
}

export type LightsGlowMap = Record<LightKey, 0 | 1 | 2 | 3>;
export type ShadowCounts = Record<ShadowKey, number>;

export interface ReadinessState {
  wishes: Record<string, CompletedWishEntry>;
  lights: LightsGlowMap;
  selectedCountry: SelectedCountryRef | null;
}

const KEY_WISHES = 'hr:v1:wishes'; // Internal Phase 2 key retained; holds completed breakthroughs
const KEY_LIGHTS = 'hr:v1:lights';
const KEY_COUNTRY = 'hr:v1:country';
export const KEY_INTRO_SEEN = 'hr:v1:intro_seen';

export function hasSeenTotoIntro(): boolean {
  if (typeof window === 'undefined') return false;
  try {
    return localStorage.getItem(KEY_INTRO_SEEN) === 'true' || localStorage.getItem(KEY_INTRO_SEEN) === '1';
  } catch {
    return false;
  }
}

export function markTotoIntroSeen(method: 'begin' | 'skip' = 'begin') {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(KEY_INTRO_SEEN, 'true');
  } catch {
    // Ignore quota errors
  }
  trackEvent('toto_intro_seen', { method });
}

function clampGlow(n: number): 0 | 1 | 2 | 3 {
  if (n <= 0) return 0;
  if (n === 1) return 1;
  if (n === 2) return 2;
  return 3;
}

/**
 * Deterministic 0-3 Light Glow Formula (documented in DECISIONS.md):
 * - Clarity:    1 point per unique completed wish (max 3)
 * - Foresight:  1 point per unique wish with pre-wobble foresight guess OR Foresight worry choice (max 3)
 * - Fairness:   1 point per unique wish choosing a Fairness worry choice + +1 if Capability includes equity-ready country (max 3)
 * - Wisdom:     1 point per unique wish choosing a Wisdom worry choice OR Way human habit pledge (up to 3 total)
 * - Capability: 1 point per unique Way pledge (up to 2) + 1 country point ONLY if visitor explicitly selected
 *               a rated country with >= 3 of 5 index checks in place (0 if no country selected or unrated).
 */
export function computeLights(
  wishes: Record<string, CompletedWishEntry>,
  country: SelectedCountryRef | null
): LightsGlowMap {
  const entries = Object.values(wishes);
  const completedCount = entries.length;

  let foresightPts = 0;
  let fairnessPts = 0;
  let wisdomPts = 0;
  let pledgePts = 0;

  for (const w of entries) {
    if (w.guessedWobble || w.weightLight === 'Foresight') foresightPts += 1;
    if (w.weightLight === 'Fairness') fairnessPts += 1;
    if (w.weightLight === 'Wisdom' || w.pledged) wisdomPts += 1;
    if (w.pledged) pledgePts += 1;
  }

  // Country input contributes strictly ONLY when a country has been explicitly selected by the user
  const countryCapPt =
    country && country.kind === 'rated' && (country.checklistCount ?? 0) >= 3 ? 1 : 0;

  return {
    Clarity: clampGlow(completedCount),
    Foresight: clampGlow(foresightPts),
    Fairness: clampGlow(fairnessPts),
    Wisdom: clampGlow(wisdomPts),
    Capability: clampGlow(Math.min(2, pledgePts) + countryCapPt)
  };
}

export function computeShadows(wishes: Record<string, CompletedWishEntry>): ShadowCounts {
  const counts: ShadowCounts = {
    Control: 0,
    Dependence: 0,
    Power: 0,
    Truth: 0,
    Speed: 0
  };
  for (const w of Object.values(wishes)) {
    counts[w.weightShadow] = (counts[w.weightShadow] ?? 0) + 1;
  }
  return counts;
}

export function deriveTrailArchetype(lights: LightsGlowMap, shadows: ShadowCounts): TrailArchetypeKey {
  if (lights.Foresight >= lights.Fairness && (shadows.Truth >= 1 || lights.Foresight >= lights.Wisdom)) {
    return 'Verifier';
  }
  if (lights.Fairness >= lights.Capability || shadows.Power >= 1) {
    return 'Neighbour';
  }
  if (lights.Capability >= lights.Wisdom || shadows.Speed >= 1) {
    return 'Builder';
  }
  return 'Keeper';
}

function readJson<T>(key: string, fallback: T): T {
  if (typeof window === 'undefined') return fallback;
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeJson(key: string, val: unknown) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(key, JSON.stringify(val));
  } catch {
    // Ignore storage quota errors
  }
}

function loadInitialState(): ReadinessState {
  const wishes = readJson<Record<string, CompletedWishEntry>>(KEY_WISHES, {});
  const selectedCountry = readJson<SelectedCountryRef | null>(KEY_COUNTRY, null);
  const lights = computeLights(wishes, selectedCountry);
  return { wishes, lights, selectedCountry };
}

export const readinessStore = writable<ReadinessState>(loadInitialState());

export const completedWishList = derived(readinessStore, ($s) =>
  Object.values($s.wishes).sort((a, b) => a.completedAt.localeCompare(b.completedAt))
);

export const shadowSummary = derived(readinessStore, ($s) => computeShadows($s.wishes));

export function refreshReadinessFromStorage() {
  readinessStore.set(loadInitialState());
}

export function recordWishCompletion(entry: CompletedWishEntry) {
  readinessStore.update((prev) => {
    const nextWishes = { ...prev.wishes, [entry.wishId]: entry };
    const nextLights = computeLights(nextWishes, prev.selectedCountry);
    writeJson(KEY_WISHES, nextWishes);
    writeJson(KEY_LIGHTS, nextLights);

    for (const light of Object.keys(nextLights) as LightKey[]) {
      if (nextLights[light] > prev.lights[light]) {
        trackEvent('light_gained', { light, level: nextLights[light] });
      }
    }
    trackEvent('breakthrough_completed', {
      breakthrough: entry.wishId,
      light: entry.weightLight,
      shadow: entry.weightShadow,
      sec: entry.durationSec
    });
    return { ...prev, wishes: nextWishes, lights: nextLights };
  });
}

export function setSelectedCountryForReadiness(country: SelectedCountryRef | null) {
  readinessStore.update((prev) => {
    const nextLights = computeLights(prev.wishes, country);
    if (country) writeJson(KEY_COUNTRY, country);
    writeJson(KEY_LIGHTS, nextLights);
    return { ...prev, selectedCountry: country, lights: nextLights };
  });
}
