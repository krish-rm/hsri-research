// Structural RTL Preview Stub (Decision #5)
// Tests document dir="rtl", mirrored layouts, and CSS logical properties cleanly
// without shipping partial/unreviewed machine translations.
import { en } from './en';

export const rtlStub = {
  ...en,
  lang: 'en',
  dir: 'rtl' as const,
  label: 'RTL Layout Test (Stub)',
  rtlNotice:
    'RTL preview active (dir="rtl"). Layouts, icons, and reading tracks mirror automatically; full global language translations arrive after Phase 1 sign-off.'
};
