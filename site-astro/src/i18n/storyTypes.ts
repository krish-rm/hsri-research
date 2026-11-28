import type { TranslationDict } from './en';
import type { HeritageIndexEntry, PlayableHeritageWish } from '../lib/heritageTypes';
import type { WishItem } from '../components/WishPlayer.svelte';
import type { LocaleKey } from './locales';

export interface LocalizedWishOverlay {
  readonly title: string;
  readonly doorTitle: string;
  readonly honestyNote: string;
  readonly wonder: { readonly text: string; readonly totoLine: string; readonly transcript: string };
  readonly wobble: { readonly text: string; readonly transcript: string };
  readonly weight: {
    readonly question: string;
    readonly transcript: string;
    readonly options: readonly { readonly id: 'a' | 'b' | 'c'; readonly text: string }[];
  };
  readonly way: {
    readonly text: string;
    readonly actionCardTitle: string;
    readonly actionCardStep: string;
    readonly pledgeLabel: string;
    readonly transcript: string;
  };
  readonly realityMeter: { readonly reason: string; readonly metricLabel?: string };
}

export interface LocalizedHeritageOverlay {
  readonly originRegion: string;
  readonly traditionLabel: string;
  readonly chipTitle: string;
  readonly title: string;
  readonly summary: string;
  readonly honestyNote: string;
  readonly dependencyLabel: string;
  readonly doorTitle: string;
  readonly reviewer: string;
  readonly wonder: { readonly text: string; readonly totoLine: string; readonly transcript: string };
  readonly wobble: { readonly text: string; readonly transcript: string };
  readonly weight: {
    readonly question: string;
    readonly transcript: string;
    readonly options: readonly { readonly id: 'a' | 'b' | 'c'; readonly text: string }[];
  };
  readonly way: {
    readonly text: string;
    readonly actionCardTitle: string;
    readonly actionCardStep: string;
    readonly pledgeLabel: string;
    readonly transcript: string;
  };
  readonly realityMeter: { readonly reason: string };
}

export interface StoryLocalePack {
  readonly wishes: Record<string, LocalizedWishOverlay>;
  readonly heritage: Record<string, LocalizedHeritageOverlay>;
}

type LText3 = { readonly en: string; readonly es?: string; readonly ar?: string };

export function pickBaseLText(t: LText3 | undefined | null, loc: LocaleKey): string {
  if (!t) return '';
  if (loc === 'es' && t.es) return t.es;
  if (loc === 'ar' && t.ar) return t.ar;
  return t.en;
}

export function pickHonestyScale(
  scale: 'Imagination' | 'Possible soon' | 'Real today',
  d: TranslationDict
): string {
  if (scale === 'Real today') return d.player.realityScales.realToday;
  if (scale === 'Possible soon') return d.player.realityScales.possibleSoon;
  return d.player.realityScales.imagination;
}

const LIGHT_ORDER = ['Clarity', 'Foresight', 'Fairness', 'Wisdom', 'Capability'] as const;

export function pickLightLabel(lightKey: string, d: TranslationDict): string {
  const idx = LIGHT_ORDER.indexOf(lightKey as (typeof LIGHT_ORDER)[number]);
  return idx >= 0 && d.lights.items[idx] ? d.lights.items[idx].key : lightKey;
}

export function resolveHeritageMeta(
  entry: HeritageIndexEntry,
  loc: LocaleKey,
  pack: StoryLocalePack | null
) {
  const ov = pack?.heritage?.[entry.id];
  return {
    originRegion: ov?.originRegion ?? pickBaseLText(entry.originRegion, loc),
    traditionLabel: ov?.traditionLabel ?? pickBaseLText(entry.traditionLabel, loc),
    chipTitle: ov?.chipTitle ?? pickBaseLText(entry.chipTitle, loc),
    summary: ov?.summary ?? pickBaseLText(entry.summary, loc),
    dependencyLabel: ov?.dependencyLabel ?? pickBaseLText(entry.binding?.dependencyLabel, loc)
  };
}

export function resolvePlayableWishCopy(
  wish: WishItem | PlayableHeritageWish,
  loc: LocaleKey,
  pack: StoryLocalePack | null
) {
  const isHeritage = 'isHeritage' in wish && wish.isHeritage;
  const rawId = isHeritage ? wish.id.replace(/^heritage-/, '') : wish.id;
  const hOv = isHeritage ? pack?.heritage?.[rawId] : undefined;
  const wOv = !isHeritage ? pack?.wishes?.[rawId] : undefined;
  const ov = hOv ?? wOv;

  return {
    title: ov?.title ?? pickBaseLText(wish.title, loc),
    doorTitle: ov?.doorTitle ?? pickBaseLText(wish.doorTitle, loc),
    honestyNote: ov?.honestyNote ?? pickBaseLText(wish.honestyNote, loc),
    traditionLabel: isHeritage
      ? (hOv?.traditionLabel ?? pickBaseLText((wish as PlayableHeritageWish).traditionLabel, loc))
      : '',
    dependencyLabel: isHeritage
      ? (hOv?.dependencyLabel ?? pickBaseLText((wish as PlayableHeritageWish).binding?.dependencyLabel, loc))
      : '',
    wonder: {
      text: ov?.wonder.text ?? pickBaseLText(wish.wonder.text, loc),
      totoLine: ov?.wonder.totoLine ?? pickBaseLText(wish.wonder.totoLine, loc),
      transcript: ov?.wonder.transcript ?? pickBaseLText(wish.wonder.transcript, loc)
    },
    wobble: {
      text: ov?.wobble.text ?? pickBaseLText(wish.wobble.text, loc),
      transcript: ov?.wobble.transcript ?? pickBaseLText(wish.wobble.transcript, loc)
    },
    weight: {
      question: ov?.weight.question ?? pickBaseLText(wish.weight.question, loc),
      transcript: ov?.weight.transcript ?? pickBaseLText(wish.weight.transcript, loc),
      optionText: (optId: 'a' | 'b' | 'c', fallbackObj: LText3) =>
        ov?.weight.options.find((o) => o.id === optId)?.text ?? pickBaseLText(fallbackObj, loc)
    },
    way: {
      text: ov?.way.text ?? pickBaseLText(wish.way.text, loc),
      actionCardTitle: ov?.way.actionCardTitle ?? pickBaseLText(wish.way.actionCardTitle, loc),
      actionCardStep: ov?.way.actionCardStep ?? pickBaseLText(wish.way.actionCardStep, loc),
      pledgeLabel: ov?.way.pledgeLabel ?? pickBaseLText(wish.way.pledgeLabel, loc),
      transcript: ov?.way.transcript ?? pickBaseLText(wish.way.transcript, loc)
    },
    realityReason: ov?.realityMeter.reason ?? pickBaseLText(wish.realityMeter.reason, loc),
    metricLabel: (wOv?.realityMeter.metricLabel ?? pickBaseLText(wish.realityMeter.observedMetric?.label, loc))
  };
}
