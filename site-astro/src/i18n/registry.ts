// Build-time server registry of all 14 UI dictionaries & 11 dynamic story packs.
// Imported ONLY inside Astro SSR pages (.astro frontmatter) so client bundles stay code-split.
import type { LocaleCode } from './locales';
import type { TranslationDict } from './en';
import type { StoryLocalePack } from './storyTypes';

import { en } from './en';
import { es } from './es';
import { ar } from './ar';
import { zh } from './zh';
import { hi } from './hi';
import { fr } from './fr';
import { pt } from './pt';
import { bn } from './bn';
import { ru } from './ru';
import { id } from './id';
import { ja } from './ja';
import { de } from './de';
import { ko } from './ko';
import { sw } from './sw';

import { zhStories } from './stories/zh';
import { hiStories } from './stories/hi';
import { frStories } from './stories/fr';
import { ptStories } from './stories/pt';
import { bnStories } from './stories/bn';
import { ruStories } from './stories/ru';
import { idStories } from './stories/id';
import { jaStories } from './stories/ja';
import { deStories } from './stories/de';
import { koStories } from './stories/ko';
import { swStories } from './stories/sw';

export const SERVER_DICTS: Record<LocaleCode, TranslationDict> = {
  en,
  es,
  ar,
  zh,
  hi,
  fr,
  pt,
  bn,
  ru,
  id,
  ja,
  de,
  ko,
  sw
};

export const SERVER_STORIES: Partial<Record<LocaleCode, StoryLocalePack>> = {
  zh: zhStories,
  hi: hiStories,
  fr: frStories,
  pt: ptStories,
  bn: bnStories,
  ru: ruStories,
  id: idStories,
  ja: jaStories,
  de: deStories,
  ko: koStories,
  sw: swStories
};
