// Central registry of all supported languages (3 launch + 11 major global languages = 14 total).
// Keeps single-source-of-truth metadata, normalization, and browser-native region display names.

export type LocaleCode =
  | 'en'
  | 'es'
  | 'ar'
  | 'zh'
  | 'hi'
  | 'fr'
  | 'pt'
  | 'bn'
  | 'ru'
  | 'id'
  | 'ja'
  | 'de'
  | 'ko'
  | 'sw';

export type LocaleKey = LocaleCode | 'rtl-stub';

export interface LocaleMeta {
  readonly code: LocaleCode;
  readonly label: string;
  readonly short: string;
  readonly englishName: string;
  readonly dir: 'ltr' | 'rtl';
  readonly reviewed: boolean;
}

export const SUPPORTED_LOCALES: readonly LocaleMeta[] = [
  { code: 'en', label: 'English', short: 'EN', englishName: 'English', dir: 'ltr', reviewed: true },
  { code: 'es', label: 'Español', short: 'ES', englishName: 'Spanish', dir: 'ltr', reviewed: false },
  { code: 'ar', label: 'العربية (RTL)', short: 'AR', englishName: 'Arabic', dir: 'rtl', reviewed: false },
  { code: 'zh', label: '中文 (简体)', short: '中文', englishName: 'Chinese (Simplified)', dir: 'ltr', reviewed: false },
  { code: 'hi', label: 'हिन्दी', short: 'हिन्दी', englishName: 'Hindi', dir: 'ltr', reviewed: false },
  { code: 'fr', label: 'Français', short: 'FR', englishName: 'French', dir: 'ltr', reviewed: false },
  { code: 'pt', label: 'Português', short: 'PT', englishName: 'Portuguese', dir: 'ltr', reviewed: false },
  { code: 'bn', label: 'বাংলা', short: 'বাংলা', englishName: 'Bengali', dir: 'ltr', reviewed: false },
  { code: 'ru', label: 'Русский', short: 'RU', englishName: 'Russian', dir: 'ltr', reviewed: false },
  { code: 'id', label: 'Bahasa Indonesia', short: 'ID', englishName: 'Indonesian', dir: 'ltr', reviewed: false },
  { code: 'ja', label: '日本語', short: '日本語', englishName: 'Japanese', dir: 'ltr', reviewed: false },
  { code: 'de', label: 'Deutsch', short: 'DE', englishName: 'German', dir: 'ltr', reviewed: false },
  { code: 'ko', label: '한국어', short: '한국어', englishName: 'Korean', dir: 'ltr', reviewed: false },
  { code: 'sw', label: 'Kiswahili', short: 'SW', englishName: 'Swahili', dir: 'ltr', reviewed: false }
];

export const LOCALE_CODES: readonly LocaleCode[] = SUPPORTED_LOCALES.map((l) => l.code);
const LOCALE_CODE_SET = new Set<string>(LOCALE_CODES);
const META_BY_CODE = new Map<LocaleCode, LocaleMeta>(SUPPORTED_LOCALES.map((l) => [l.code, l]));

export const RTL_LOCALE_KEYS = new Set<string>(['ar', 'rtl-stub']);

export function normalizeLocale(val: string | null | undefined): LocaleKey {
  if (!val) return 'en';
  const cleaned = val.trim().toLowerCase();
  if (cleaned === 'rtl-stub') return 'rtl-stub';
  if (LOCALE_CODE_SET.has(cleaned)) return cleaned as LocaleCode;
  const primary = cleaned.split(/[-_]/)[0];
  if (primary === 'tl' || primary === 'fil') return 'en';
  if (primary === 'in') return 'id';
  if (LOCALE_CODE_SET.has(primary)) return primary as LocaleCode;
  return 'en';
}

export function getLocaleMeta(key: LocaleKey): LocaleMeta {
  if (key === 'rtl-stub') {
    return { code: 'en', label: 'RTL Layout Test', short: 'RTL', englishName: 'RTL Stub', dir: 'rtl', reviewed: true };
  }
  return META_BY_CODE.get(key) ?? SUPPORTED_LOCALES[0];
}

// Common ISO-3166 alpha-3 -> alpha-2 lookup for localized Intl.DisplayNames country names (zero bundle table bloat).
const ISO3_TO_ISO2: Record<string, string> = {
  AFG: 'AF', ALB: 'AL', DZA: 'DZ', AGO: 'AO', ARG: 'AR', ARM: 'AM', AUS: 'AU', AUT: 'AT', AZE: 'AZ',
  BGD: 'BD', BEL: 'BE', BEN: 'BJ', BRA: 'BR', BGR: 'BG', BFA: 'BF', BDI: 'BI', CMR: 'CM', CAN: 'CA',
  CAF: 'CF', TCD: 'TD', CHL: 'CL', CHN: 'CN', COL: 'CO', COM: 'KM', COG: 'CG', CRI: 'CR', CYP: 'CY',
  CZE: 'CZ', COD: 'CD', DNK: 'DK', DJI: 'DJ', DOM: 'DO', ECU: 'EC', EGY: 'EG', SLV: 'SV', GNQ: 'GQ',
  ERI: 'ER', EST: 'EE', SWZ: 'SZ', ETH: 'ET', FJI: 'FJ', FIN: 'FI', FRA: 'FR', GAB: 'GA', GEO: 'GE',
  DEU: 'DE', GHA: 'GH', GRC: 'GR', GTM: 'GT', GIN: 'GN', GNB: 'GW', GUY: 'GY', HTI: 'HT', HND: 'HN',
  HKG: 'HK', HUN: 'HU', ISL: 'IS', IND: 'IN', IDN: 'ID', IRN: 'IR', IRQ: 'IQ', IRL: 'IE', ISR: 'IL',
  ITA: 'IT', CIV: 'CI', JAM: 'JM', JPN: 'JP', JOR: 'JO', KAZ: 'KZ', KEN: 'KE', KWT: 'KW', KGZ: 'KG',
  LAO: 'LA', LVA: 'LV', LBN: 'LB', LSO: 'LS', LBY: 'LY', LTU: 'LT', LUX: 'LU', MAC: 'MO', MDG: 'MG',
  MWI: 'MW', MYS: 'MY', MLI: 'ML', MLT: 'MT', MRT: 'MR', MUS: 'MU', MEX: 'MX', MDA: 'MD', MNG: 'MN',
  MAR: 'MA', MOZ: 'MZ', MMR: 'MM', NAM: 'NA', NPL: 'NP', NLD: 'NL', NZL: 'NZ', NIC: 'NI', NER: 'NE',
  NGA: 'NG', MKD: 'MK', NOR: 'NO', OMN: 'OM', PAK: 'PK', PAN: 'PA', PNG: 'PG', PRY: 'PY', PER: 'PE',
  PHL: 'PH', POL: 'PL', PRT: 'PT', QAT: 'QA', ROU: 'RO', RUS: 'RU', RWA: 'RW', SAU: 'SA', SEN: 'SN',
  SRB: 'RS', SLE: 'SL', SGP: 'SG', SVK: 'SK', SVN: 'SI', SOM: 'SO', ZAF: 'ZA', KOR: 'KR', ESP: 'ES',
  LKA: 'LK', SDN: 'SD', SUR: 'SR', SWE: 'SE', CHE: 'CH', SYR: 'SY', TWN: 'TW', TJK: 'TJ', TZA: 'TZ',
  THA: 'TH', TGO: 'TG', TTO: 'TT', TUN: 'TN', TUR: 'TR', UGA: 'UG', UKR: 'UA', ARE: 'AE', GBR: 'GB',
  USA: 'US', URY: 'UY', UZB: 'UZ', VEN: 'VE', VNM: 'VN', YEM: 'YE', ZMB: 'ZM', ZWE: 'ZW'
};

const displayNameCache = new Map<string, Intl.DisplayNames | null>();

export function getCountryDisplayName(
  iso3: string | null | undefined,
  fallbackName: string,
  locale: LocaleKey
): string {
  if (!iso3 || iso3 === 'GLOBAL' || locale === 'en' || locale === 'rtl-stub') {
    return fallbackName;
  }
  const alpha2 = ISO3_TO_ISO2[iso3.toUpperCase()];
  if (!alpha2 || typeof Intl === 'undefined' || typeof Intl.DisplayNames !== 'function') {
    return fallbackName;
  }
  try {
    let dn = displayNameCache.get(locale);
    if (dn === undefined) {
      dn = new Intl.DisplayNames([locale], { type: 'region' });
      displayNameCache.set(locale, dn);
    }
    return dn?.of(alpha2) || fallbackName;
  } catch {
    return fallbackName;
  }
}
