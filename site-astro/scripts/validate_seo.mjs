import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const distDir = path.join(rootDir, 'dist');
const catalogPath = path.join(rootDir, 'src/data/country_catch_catalog.json');

const LOCALES = ['en', 'es', 'ar', 'zh', 'hi', 'fr', 'pt', 'bn', 'ru', 'id', 'ja', 'de', 'ko', 'sw'];
const EXPECTED_DIR = { ar: 'rtl' };
const ORIGIN = 'https://humanityreadiness.org';

const NON_EN_MARKERS = {
  hi: 'मानवता',
  ar: 'البشرية',
  ja: '人類',
  zh: '人类',
  es: 'humanidad',
  fr: 'humanité',
  de: 'Menschheit',
  ko: '인류'
};

function assert(cond, msg) {
  if (!cond) {
    throw new Error(`SEO Validation Failed: ${msg}`);
  }
}

function extractJsonLdBlocks(html) {
  const blocks = [];
  const re = /<script\s+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    blocks.push(JSON.parse(m[1]));
  }
  return blocks;
}

function main() {
  assert(fs.existsSync(distDir), `dist directory missing at ${distDir}`);

  const rawCatalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  const allCountries = Array.isArray(rawCatalog) ? rawCatalog : rawCatalog.countries || [];
  assert(allCountries.length === 148, `Expected 148 catalog countries, found ${allCountries.length}`);

  const sitemapPath = path.join(distDir, 'sitemap-0.xml');
  assert(fs.existsSync(sitemapPath), 'dist/sitemap-0.xml missing');
  const sitemapXml = fs.readFileSync(sitemapPath, 'utf8');

  // 1. Verify all 14 homepages in dist + sitemap + hreflang + JSON-LD + SSR copy
  for (const loc of LOCALES) {
    const pagePath = loc === 'en' ? path.join(distDir, 'index.html') : path.join(distDir, loc, 'index.html');
    const canonical = loc === 'en' ? `${ORIGIN}/` : `${ORIGIN}/${loc}/`;
    assert(fs.existsSync(pagePath), `Missing built homepage: ${pagePath}`);
    assert(sitemapXml.includes(`<loc>${canonical}</loc>`), `Sitemap missing homepage URL: ${canonical}`);

    const html = fs.readFileSync(pagePath, 'utf8');
    const expectedDir = EXPECTED_DIR[loc] || 'ltr';
    assert(html.includes(`lang="${loc}"`), `Homepage ${loc} missing lang="${loc}"`);
    assert(html.includes(`dir="${expectedDir}"`), `Homepage ${loc} missing dir="${expectedDir}"`);
    assert(
      html.includes(`<link rel="canonical" href="${canonical}"`),
      `Homepage ${loc} missing canonical ${canonical}`
    );

    for (const altLoc of LOCALES) {
      const altHref = altLoc === 'en' ? `${ORIGIN}/` : `${ORIGIN}/${altLoc}/`;
      assert(
        html.includes(`hreflang="${altLoc}" href="${altHref}"`),
        `Homepage ${loc} missing hreflang="${altLoc}" -> ${altHref}`
      );
      assert(
        html.includes(altLoc === 'en' ? 'href="/"' : `href="/${altLoc}/"`),
        `Homepage ${loc} missing footer crawl link for ${altLoc}`
      );
    }
    assert(
      html.includes(`hreflang="x-default" href="${ORIGIN}/"`),
      `Homepage ${loc} missing hreflang="x-default"`
    );

    const jsonLdBlocks = extractJsonLdBlocks(html);
    assert(jsonLdBlocks.length >= 2, `Homepage ${loc} expected >=2 JSON-LD blocks, found ${jsonLdBlocks.length}`);
    const serialized = JSON.stringify(jsonLdBlocks);
    assert(!serialized.includes('github.com'), `Homepage ${loc} JSON-LD leaked github.com`);
    assert(
      serialized.includes('WebSite') && serialized.includes('ResearchOrganization') && serialized.includes('Dataset'),
      `Homepage ${loc} JSON-LD missing expected Schema.org types`
    );

    if (NON_EN_MARKERS[loc]) {
      assert(html.includes(NON_EN_MARKERS[loc]), `Homepage ${loc} SSR HTML missing native text "${NON_EN_MARKERS[loc]}"`);
    }
  }

  // 2. Verify all 148 countries exist in dist, sitemap-0.xml, /countries/ directory, and pass R6 / JSON-LD rules
  const dirPagePath = path.join(distDir, 'countries', 'index.html');
  assert(fs.existsSync(dirPagePath), 'Missing built /countries/index.html');
  const dirHtml = fs.readFileSync(dirPagePath, 'utf8');

  const ratedCount = allCountries.filter((c) => c.kind === 'rated').length;
  const unratedCount = allCountries.filter((c) => c.kind === 'unrated').length;

  for (const c of allCountries) {
    const slug = (c.id || c.iso).toLowerCase();
    const cPath = path.join(distDir, 'countries', slug, 'index.html');
    const cUrl = `${ORIGIN}/countries/${slug}/`;
    assert(fs.existsSync(cPath), `Missing built country page: ${cPath}`);
    assert(sitemapXml.includes(`<loc>${cUrl}</loc>`), `Sitemap missing country URL: ${cUrl}`);
    assert(dirHtml.includes(`/countries/${slug}/`), `/countries/index.html missing link to /countries/${slug}/`);

    const cHtml = fs.readFileSync(cPath, 'utf8');
    assert(cHtml.includes(`<link rel="canonical" href="${cUrl}"`), `Country ${slug} missing canonical`);
    assert(cHtml.includes(`/?c=${c.iso}`), `Country ${slug} missing 60s Explorer CTA (?c=${c.iso})`);

    const blocks = extractJsonLdBlocks(cHtml);
    assert(blocks.length >= 2, `Country ${slug} missing Schema.org JSON-LD blocks`);
    const flat = JSON.stringify(blocks);
    assert(flat.includes('BreadcrumbList') && flat.includes('Dataset'), `Country ${slug} missing BreadcrumbList/Dataset JSON-LD`);
    assert(flat.includes(c.name) && flat.includes(c.iso), `Country ${slug} JSON-LD missing identity`);
    assert(!flat.includes('undefined') && !flat.includes('NaN') && !cHtml.includes('N/Ah'), `Country ${slug} contains unformatted placeholder in SEO metadata`);

    if (c.kind === 'unrated') {
      assert(cHtml.includes('Not Yet Rated'), `Coverage audit country ${slug} missing "Not Yet Rated" badge`);
      assert(!cHtml.includes('Benchmark Rank'), `Coverage audit country ${slug} must NOT display a benchmark rank`);
    } else {
      assert(cHtml.includes('Benchmark Rank'), `Rated country ${slug} missing Benchmark Rank section`);
    }
  }

  console.log(
    `SEO Validation Passed: ${LOCALES.length} multilingual homepages + ${allCountries.length} country pages (${ratedCount} rated, ${unratedCount} coverage audits) verified across dist/, sitemap-0.xml, hreflang, and JSON-LD.`
  );
}

main();
