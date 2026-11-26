// Breakthrough catalog loader with compile-time Vite virtual module & define gating.
// - Production build (`npm run build`): SHOW_DRAFT_BADGE === false and virtual:hsri-dev15 resolves to []
//   so neither DRAFT badges nor wishes.draft15.json ever enter dist/.
// - Preview build (`npm run build:preview`): SHOW_DRAFT_BADGE === true, virtual:hsri-dev15 === [].
// - Dev / `npm run build:dev`: both true (all 20 breakthroughs active).
import coreRaw from '../data/wishes.json';
import dev15Raw from 'virtual:hsri-dev15';
import type { WishItem } from '../components/WishPlayer.svelte';

export const SHOW_DRAFT_BADGE: boolean = __HSRI_SHOW_DRAFTS__;
export const INCLUDE_DEV_BREAKTHROUGHS: boolean = __HSRI_INCLUDE_DEV15__;

export const CORE_BREAKTHROUGHS: WishItem[] = coreRaw as unknown as WishItem[];

export async function loadAllBreakthroughs(): Promise<WishItem[]> {
  if (!INCLUDE_DEV_BREAKTHROUGHS) {
    return CORE_BREAKTHROUGHS;
  }
  return [...CORE_BREAKTHROUGHS, ...(dev15Raw as unknown as WishItem[])];
}
