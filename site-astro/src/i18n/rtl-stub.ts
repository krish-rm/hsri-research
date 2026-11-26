// Backwards-compatible RTL stub preserving Decision #5 tests
import { en, type TranslationDict } from './en';

export const rtlStub: TranslationDict = {
  ...en,
  lang: 'en',
  dir: 'rtl',
  label: 'RTL Layout Test (Stub)'
};
