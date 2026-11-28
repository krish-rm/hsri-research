import type { LightKey, ShadowKey } from './readinessState';
import type { WishItem } from '../components/WishPlayer.svelte';

export type LangCode = 'en' | 'es' | 'ar';
export type LText = { en: string; es: string; ar: string };

export type HeritageMetricKey =
  | 't_half'
  | 'infrastructure'
  | 'discernment'
  | 'governance'
  | 'p8_post_labor';

export interface HeritageBinding {
  primary: HeritageMetricKey;
  secondary?: HeritageMetricKey;
  dependencyLabel: LText;
  safeguardChecklistIdx: number; // 0..4 index inside CountryCatchWidget checklist
}

export interface HeritageSource {
  title: string;
  url: string;
  note: string;
}

export interface HeritageIndexEntry {
  id: string;
  slug: string;
  door: 'mysteries' | 'gadgets' | 'epic' | 'movie' | 'world';
  icon: 'chalkboard' | 'pocket' | 'eye' | 'frame' | 'lamp';
  era: 'living' | 'historical';
  originRegion: LText;
  traditionLabel: LText;
  chipTitle: LText;
  summary: LText;
  countries: string[];
  honestyLabel: 'Imagination' | 'Possible soon' | 'Real today';
  binding: HeritageBinding;
  atlasRefs: string[];
  status: 'review_open' | 'published';
  sourceCount: number;
}

export interface HeritageFullRecord extends HeritageIndexEntry {
  title: LText;
  doorTitle: LText;
  honestyNote: LText;
  shadowTag: ShadowKey;
  wonder: { text: LText; totoLine: LText; transcript: LText; draft: boolean };
  wobble: { text: LText; transcript: LText; draft: boolean };
  weight: {
    question: LText;
    transcript: LText;
    draft: boolean;
    options: Array<{ id: 'a' | 'b' | 'c'; text: LText; light: LightKey; shadow: ShadowKey }>;
  };
  way: {
    text: LText;
    actionCardTitle: LText;
    actionCardStep: LText;
    pledgeLabel: LText;
    transcript: LText;
    draft: boolean;
  };
  closingLine: string;
  realityMeter: {
    scale: 'Imagination' | 'Possible soon' | 'Real today';
    reason: LText;
    observedMetric?: { value: string; label: LText; directCapabilityMatch: true } | null;
    source: string;
    sourceUrl: string;
    lastReviewed: string;
  };
  sources: HeritageSource[];
  reviewers: { en: string; es: string; ar: string };
}

export type PlayableHeritageWish = WishItem & {
  isHeritage: true;
  slug: string;
  traditionLabel: LText;
  originRegion: LText;
  era: 'living' | 'historical';
  countries: string[];
  binding: HeritageBinding;
  sources: HeritageSource[];
  reviewers: { en: string; es: string; ar: string };
  heritageStatus: 'review_open' | 'published';
};

export function toPlayableHeritageWish(rec: HeritageFullRecord): PlayableHeritageWish {
  return {
    id: `heritage-${rec.id}`,
    door: rec.door,
    order: 0,
    icon: rec.icon,
    status: rec.status === 'published' ? 'owner_approved' : 'draft',
    devOnly: false,
    title: rec.title,
    doorTitle: rec.doorTitle,
    honestyLabel: rec.honestyLabel,
    honestyNote: rec.honestyNote,
    verbatimFromBrief: false,
    shadowTag: rec.shadowTag,
    atlasRefs: rec.atlasRefs,
    wonder: rec.wonder,
    wobble: rec.wobble,
    weight: rec.weight,
    way: rec.way,
    closingLine: rec.closingLine,
    realityMeter: rec.realityMeter,
    isHeritage: true,
    slug: rec.slug,
    traditionLabel: rec.traditionLabel,
    originRegion: rec.originRegion,
    era: rec.era,
    countries: rec.countries,
    binding: rec.binding,
    sources: rec.sources,
    reviewers: rec.reviewers,
    heritageStatus: rec.status
  };
}
