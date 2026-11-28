import { ISO3_TO_ISO2, LOCALE_CODES, SUPPORTED_LOCALES, type LocaleCode } from '../i18n/locales';

export const SITE_ORIGIN = 'https://humanityreadiness.org';
export const ZENODO_DOI_URL = 'https://doi.org/10.5281/zenodo.23441742';

export interface HreflangAlternate {
  readonly hreflang: string;
  readonly href: string;
}

export const OG_LOCALE_BY_LANG: Record<LocaleCode, string> = {
  en: 'en_US',
  es: 'es_ES',
  ar: 'ar_AE',
  zh: 'zh_CN',
  hi: 'hi_IN',
  fr: 'fr_FR',
  pt: 'pt_BR',
  bn: 'bn_BD',
  ru: 'ru_RU',
  id: 'id_ID',
  ja: 'ja_JP',
  de: 'de_DE',
  ko: 'ko_KR',
  sw: 'sw_KE'
};

export const SEO_KEYWORDS_BY_LANG: Record<LocaleCode, string> = {
  en: 'Humanity Superintelligence Readiness Index, Humanity Readiness Index, HSRI, superintelligence readiness, AI readiness by country, country preparedness index',
  es: 'Índice de Preparación para la Superinteligencia Humana, índice de preparación IA, superinteligencia, preparación por país, HSRI',
  ar: 'مؤشر جاهزية البشرية للذكاء الفائق، مؤشر جاهزية الذكاء الاصطناعي، الذكاء الفائق، جاهزية الدول، HSRI',
  zh: '人类超级智能准备度指数, 超级智能准备指数, 人工智能准备度, 国家准备度排名, HSRI',
  hi: 'मानवता सुपरइंटेलिजेंस तैयारी सूचकांक, सुपरइंटेलिजेंस तैयारी सूचकांक, एआई तैयारी भारत, देश तैयारी डेटा, HSRI',
  fr: 'Indice de Préparation à la Superintelligence Humaine, indice de préparation IA, superintelligence, préparation nationale, HSRI',
  pt: 'Índice de Preparação para a Superinteligência Humana, índice de preparação IA, superinteligência, prontidão por país, HSRI',
  bn: 'মানবতার সুপারইন্টেলিজেন্স প্রস্তুতি সূচক, সুপারইন্টেলিজেন্স প্রস্তুতি সূচক, এআই প্রস্তুতি, দেশভিত্তিক প্রস্তুতি, HSRI',
  ru: 'Индекс готовности человечества к сверхинтеллекту, готовность стран к сверхинтеллекту, индекс готовности к ИИ, HSRI',
  id: 'Indeks Kesiapan Umat Manusia untuk Superinteligensi, indeks kesiapan AI, kesiapan negara, HSRI',
  ja: '人類超知能準備指数, スーパーインテリジェンス準備指数, AI準備度ランキング, 国別準備データ, HSRI',
  de: 'Humanity Superintelligence Readiness Index, Superintelligenz Bereitschaftsindex, KI-Bereitschaft nach Land, HSRI',
  ko: '인류 초지능 준비 지수, 초지능 대비 지수, 국가별 AI 준비도, HSRI',
  sw: 'Faharasa ya Utayari wa Binadamu kwa Akili Kuu, utayari wa akili bandia kwa nchi, HSRI'
};

const dnCache = new Map<string, Intl.DisplayNames | null>();

export function getCountryNameInLocale(iso3: string, fallback: string, loc: LocaleCode): string {
  if (!iso3 || loc === 'en') return fallback;
  const alpha2 = ISO3_TO_ISO2[iso3.toUpperCase()];
  if (!alpha2 || typeof Intl === 'undefined' || typeof Intl.DisplayNames !== 'function') {
    return fallback;
  }
  try {
    let dn = dnCache.get(loc);
    if (dn === undefined) {
      dn = new Intl.DisplayNames([loc], { type: 'region' });
      dnCache.set(loc, dn);
    }
    return dn?.of(alpha2) || fallback;
  } catch {
    return fallback;
  }
}

export function getLocalizedCountryNamesAll(
  iso3: string,
  englishFallback: string
): { byLocale: Array<{ loc: LocaleCode; label: string; name: string }>; uniqueNames: string[] } {
  const byLocale = SUPPORTED_LOCALES.map((meta) => ({
    loc: meta.code,
    label: meta.label,
    name: meta.code === 'en' ? englishFallback : getCountryNameInLocale(iso3, englishFallback, meta.code)
  }));
  const seen = new Set<string>();
  const uniqueNames: string[] = [];
  for (const item of byLocale) {
    if (item.name && !seen.has(item.name)) {
      seen.add(item.name);
      uniqueNames.push(item.name);
    }
  }
  return { byLocale, uniqueNames };
}

export function getHomepageAlternates(): HreflangAlternate[] {
  const list: HreflangAlternate[] = LOCALE_CODES.map((code) => ({
    hreflang: code,
    href: code === 'en' ? `${SITE_ORIGIN}/` : `${SITE_ORIGIN}/${code}/`
  }));
  list.push({ hreflang: 'x-default', href: `${SITE_ORIGIN}/` });
  return list;
}

export function normalizeCanonicalUrl(rawUrl: string | undefined, pathname: string): string {
  if (rawUrl) {
    try {
      const u = new URL(rawUrl, SITE_ORIGIN);
      return `${SITE_ORIGIN}${u.pathname}`;
    } catch {
      return `${SITE_ORIGIN}${rawUrl.startsWith('/') ? rawUrl : `/${rawUrl}`}`;
    }
  }
  const cleanPath = pathname.startsWith('/') ? pathname : `/${pathname}`;
  return `${SITE_ORIGIN}${cleanPath}`;
}

export function buildSiteGraphJsonLd(): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'ResearchOrganization',
        '@id': `${SITE_ORIGIN}/#organization`,
        name: 'HSRI Research Consortium',
        alternateName: [
          'Humanity Superintelligence Readiness Index',
          'Humanity Readiness Index',
          'HSRI 2.0'
        ],
        url: `${SITE_ORIGIN}/`,
        sameAs: [ZENODO_DOI_URL, 'https://twitter.com/hsri_research']
      },
      {
        '@type': 'WebSite',
        '@id': `${SITE_ORIGIN}/#website`,
        url: `${SITE_ORIGIN}/`,
        name: 'Humanity Superintelligence Readiness Index (HSRI)',
        alternateName: ['Humanity Readiness', 'HSRI'],
        publisher: { '@id': `${SITE_ORIGIN}/#organization` },
        inLanguage: [...LOCALE_CODES]
      }
    ]
  };
}

export function buildHomeJsonLd(
  loc: LocaleCode,
  title: string,
  description: string,
  canonicalUrl: string
): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        '@id': `${canonicalUrl}#webpage`,
        url: canonicalUrl,
        name: title,
        description,
        inLanguage: loc,
        isPartOf: { '@id': `${SITE_ORIGIN}/#website` },
        about: { '@id': `${SITE_ORIGIN}/#dataset` }
      },
      {
        '@type': 'Dataset',
        '@id': `${SITE_ORIGIN}/#dataset`,
        name: title,
        alternateName: [
          'Humanity Superintelligence Readiness Index',
          'Humanity Readiness Index',
          'HSRI 2.0'
        ],
        description,
        url: canonicalUrl,
        sameAs: ZENODO_DOI_URL,
        identifier: 'doi:10.5281/zenodo.23441742',
        license: 'https://creativecommons.org/licenses/by-sa/4.0/',
        inLanguage: [...LOCALE_CODES],
        creator: { '@id': `${SITE_ORIGIN}/#organization` },
        keywords: SEO_KEYWORDS_BY_LANG[loc].split(',').map((s) => s.trim())
      }
    ]
  };
}

export interface CountryJsonLdInput {
  id: string;
  iso: string;
  name: string;
  region: string;
  canonicalUrl: string;
  title: string;
  description: string;
  isRated: boolean;
  rank?: number;
  score?: number;
  band?: string;
  tHalfH?: number;
  alternateNames: string[];
}

export function buildCountryPageJsonLd(c: CountryJsonLdInput): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE_ORIGIN}/` },
          { '@type': 'ListItem', position: 2, name: 'Country Index', item: `${SITE_ORIGIN}/countries/` },
          { '@type': 'ListItem', position: 3, name: c.name, item: c.canonicalUrl }
        ]
      },
      {
        '@type': 'WebPage',
        '@id': `${c.canonicalUrl}#webpage`,
        url: c.canonicalUrl,
        name: c.title,
        description: c.description,
        inLanguage: 'en',
        isPartOf: { '@id': `${SITE_ORIGIN}/#website` },
        mainEntity: { '@id': `${c.canonicalUrl}#dataset` }
      },
      {
        '@type': 'Dataset',
        '@id': `${c.canonicalUrl}#dataset`,
        name: `${c.name} (${c.iso}) — Humanity Superintelligence Readiness Index`,
        description: c.description,
        url: c.canonicalUrl,
        sameAs: ZENODO_DOI_URL,
        license: 'https://creativecommons.org/licenses/by-sa/4.0/',
        creator: { '@id': `${SITE_ORIGIN}/#organization` },
        spatialCoverage: {
          '@type': 'Country',
          name: c.name,
          alternateName: c.alternateNames,
          identifier: c.iso
        },
        variableMeasured: c.isRated
          ? [
              `HSRI Score: ${c.score}/100 (Rank #${c.rank}/39, Band ${c.band})`,
              ...(typeof c.tHalfH === 'number' && Number.isFinite(c.tHalfH)
                ? [`Offline Decoupling Half-Life: ${c.tHalfH} hours`]
                : []),
              'AI Literacy',
              'Critical Discernment',
              'Institutional Governance',
              'Digital Infrastructure'
            ]
          : ['Empirical Survey Coverage Audit (Non-Benchmark)', c.region]
      }
    ]
  };
}
