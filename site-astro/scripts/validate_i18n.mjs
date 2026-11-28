import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const ts = require('typescript');

const ROOT = path.resolve(import.meta.dirname, '..');
const I18N_DIR = path.join(ROOT, 'src', 'i18n');
const STORIES_DIR = path.join(I18N_DIR, 'stories');

const NEW_LOCALES = ['zh', 'hi', 'fr', 'pt', 'bn', 'ru', 'id', 'ja', 'de', 'ko', 'sw'];
const ALL_LOCALES = ['en', 'es', 'ar', ...NEW_LOCALES];

const moduleCache = new Map();

function loadTsModule(filePath) {
  const resolved = path.resolve(filePath);
  if (moduleCache.has(resolved)) return moduleCache.get(resolved);

  const source = fs.readFileSync(resolved, 'utf8');
  const transpiled = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
      esModuleInterop: true
    },
    fileName: resolved
  }).outputText;

  const mod = { exports: {} };
  moduleCache.set(resolved, mod.exports);

  const localRequire = (spec) => {
    if (spec.endsWith('.json')) {
      const targetJson = path.resolve(path.dirname(resolved), spec);
      return JSON.parse(fs.readFileSync(targetJson, 'utf8'));
    }
    if (spec.startsWith('.')) {
      const base = path.resolve(path.dirname(resolved), spec);
      const candidates = [base, `${base}.ts`, `${base}.js`, path.join(base, 'index.ts')];
      for (const c of candidates) {
        if (fs.existsSync(c) && fs.statSync(c).isFile()) {
          return loadTsModule(c);
        }
      }
    }
    return require(spec);
  };

  const fn = new vm.Script(
    `(function(exports, require, module, __filename, __dirname) { ${transpiled}\n})`,
    { filename: resolved }
  ).runInThisContext();

  fn(mod.exports, localRequire, mod, resolved, path.dirname(resolved));
  moduleCache.set(resolved, mod.exports);
  return mod.exports;
}

const errors = [];
function fail(msg) {
  errors.push(msg);
}

// 1. Validate locale registry
const localesMod = loadTsModule(path.join(I18N_DIR, 'locales.ts'));
const registeredCodes = localesMod.SUPPORTED_LOCALES.map((l) => l.code);
for (const code of ALL_LOCALES) {
  if (!registeredCodes.includes(code)) {
    fail(`locales.ts missing locale code: ${code}`);
  }
}

// 2. Validate structural & placeholder parity across all 14 dictionaries
const enMod = loadTsModule(path.join(I18N_DIR, 'en.ts'));
const enDict = enMod.en;

function extractPlaceholders(str) {
  const matches = str.match(/\{[a-zA-Z0-9_]+\}/g);
  return matches ? [...new Set(matches)].sort() : [];
}

const BANNED_JARGON = [
  /\bt_half\b/i,
  /\brho_crit\b/i,
  /\br_sys\b/i,
  /\bregime shift\b/i,
  /\bregime flip\b/i,
  /\bphase transition\b/i,
  /\bphase boundary\b/i,
  /\bapocalypse\b/i,
  /\bdoomsday\b/i,
  /\bkill switch\b/i,
  /\bcatastrophic failure\b/i,
  /\bcritical slowing down\b/i,
  /\bearly warning signal\b/i
];

const RETIRED_RE = /\b(wishes?|wishers?|wished|wishing|wishgiver|kalpa)\b/i;
const NON_DANDA_DEVANAGARI = /[\u0900-\u0963\u0966-\u097F]/;

function checkTextClean(str, ctx, loc) {
  for (const rx of BANNED_JARGON) {
    if (rx.test(str)) fail(`${ctx}: contains banned jargon (${rx})`);
  }
  if (RETIRED_RE.test(str) && !ctx.endsWith('.href')) {
    fail(`${ctx}: contains retired term matching ${RETIRED_RE}`);
  }
  if (loc === 'bn' && NON_DANDA_DEVANAGARI.test(str)) {
    fail(`${ctx}: Devanagari glyph leaked into Bengali string`);
  }
}

function compareNode(ref, cur, ctx, loc) {
  if (typeof ref === 'string') {
    if (typeof cur !== 'string' || cur.trim().length === 0) {
      fail(`${ctx}: expected non-empty string`);
      return;
    }
    const expectedVars = extractPlaceholders(ref);
    const actualVars = extractPlaceholders(cur);
    for (const v of expectedVars) {
      if (!actualVars.includes(v)) {
        fail(`${ctx}: missing placeholder ${v}`);
      }
    }
    checkTextClean(cur, ctx, loc);
    return;
  }

  if (typeof ref === 'boolean') {
    if (typeof cur !== 'boolean') fail(`${ctx}: expected boolean`);
    return;
  }

  if (Array.isArray(ref)) {
    if (!Array.isArray(cur)) {
      fail(`${ctx}: expected array`);
      return;
    }
    if (cur.length !== ref.length) {
      fail(`${ctx}: array length ${cur.length} !== ${ref.length}`);
      return;
    }
    for (let i = 0; i < ref.length; i++) {
      compareNode(ref[i], cur[i], `${ctx}[${i}]`, loc);
    }
    return;
  }

  if (ref && typeof ref === 'object') {
    if (!cur || typeof cur !== 'object' || Array.isArray(cur)) {
      fail(`${ctx}: expected object`);
      return;
    }
    for (const key of Object.keys(ref)) {
      if (!(key in cur)) {
        // Optional property handling (e.g., extraLinks on DeeperCard)
        if (ref[key] !== undefined) {
          fail(`${ctx}.${key}: missing key`);
        }
        continue;
      }
      compareNode(ref[key], cur[key], `${ctx}.${key}`, loc);
    }
    for (const key of Object.keys(cur)) {
      if (!(key in ref)) {
        fail(`${ctx}.${key}: unexpected extra key`);
      }
    }
  }
}

for (const loc of ALL_LOCALES) {
  const dictPath = path.join(I18N_DIR, `${loc}.ts`);
  if (!fs.existsSync(dictPath)) {
    fail(`Missing UI dictionary: ${dictPath}`);
    continue;
  }
  const mod = loadTsModule(dictPath);
  const d = mod[loc];
  if (!d) {
    fail(`${loc}.ts must export const ${loc}`);
    continue;
  }
  const meta = localesMod.getLocaleMeta(loc);
  if (d.lang !== loc) fail(`${loc}.ts lang="${d.lang}" !== "${loc}"`);
  if (d.dir !== meta.dir) fail(`${loc}.ts dir="${d.dir}" !== "${meta.dir}"`);
  compareNode(enDict, d, loc, loc);
}

// 3. Validate all 11 story locale packs against wishes.json and heritage/index.json
const wishesRaw = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'data', 'wishes.json'), 'utf8'));
const coreWishes = Array.isArray(wishesRaw) ? wishesRaw : wishesRaw.wishes;
const heritageIndex = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'data', 'heritage', 'index.json'), 'utf8'));

for (const loc of NEW_LOCALES) {
  const storyPath = path.join(STORIES_DIR, `${loc}.ts`);
  if (!fs.existsSync(storyPath)) {
    fail(`Missing story pack: ${storyPath}`);
    continue;
  }
  const rawSource = fs.readFileSync(storyPath, 'utf8');
  if (/\bas\s+any\b/.test(rawSource)) {
    fail(`stories/${loc}.ts contains disallowed "as any" cast`);
  }

  const mod = loadTsModule(storyPath);
  const pack = mod[`${loc}Stories`];
  if (!pack || !pack.wishes || !pack.heritage) {
    fail(`stories/${loc}.ts must export const ${loc}Stories: StoryLocalePack`);
    continue;
  }

  function validateStoryEntry(ov, topKeys, ctx, extraCheck) {
    if (!ov) {
      fail(`${ctx}: missing`);
      return;
    }
    for (const k of topKeys) {
      if (typeof ov[k] !== 'string' || !ov[k].trim()) fail(`${ctx}.${k}: empty`);
      else checkTextClean(ov[k], `${ctx}.${k}`, loc);
    }
    for (const sub of [
      ['wonder', 'text'],
      ['wonder', 'totoLine'],
      ['wonder', 'transcript'],
      ['wobble', 'text'],
      ['wobble', 'transcript'],
      ['weight', 'question'],
      ['weight', 'transcript'],
      ['way', 'text'],
      ['way', 'actionCardTitle'],
      ['way', 'actionCardStep'],
      ['way', 'pledgeLabel'],
      ['way', 'transcript'],
      ['realityMeter', 'reason']
    ]) {
      const val = ov[sub[0]]?.[sub[1]];
      if (typeof val !== 'string' || !val.trim()) fail(`${ctx}.${sub.join('.')}: empty`);
      else checkTextClean(val, `${ctx}.${sub.join('.')}`, loc);
    }
    extraCheck?.(ov);
    if (!Array.isArray(ov.weight?.options) || ov.weight.options.length !== 3) {
      fail(`${ctx}.weight.options: must have 3 options`);
    } else {
      for (const expectedId of ['a', 'b', 'c']) {
        const opt = ov.weight.options.find((o) => o.id === expectedId);
        if (!opt || typeof opt.text !== 'string' || !opt.text.trim()) {
          fail(`${ctx}.weight.options[${expectedId}]: missing or empty`);
        } else {
          checkTextClean(opt.text, `${ctx}.weight.options[${expectedId}]`, loc);
        }
      }
    }
  }

  for (const w of coreWishes) {
    validateStoryEntry(pack.wishes[w.id], ['title', 'doorTitle', 'honestyNote'], `stories/${loc}.wishes[${w.id}]`, (ov) => {
      if (w.realityMeter?.observedMetric?.directCapabilityMatch) {
        if (typeof ov.realityMeter?.metricLabel !== 'string' || !ov.realityMeter.metricLabel.trim()) {
          fail(`stories/${loc}.wishes[${w.id}].realityMeter.metricLabel: required when directCapabilityMatch is set`);
        } else {
          checkTextClean(ov.realityMeter.metricLabel, `stories/${loc}.wishes[${w.id}].realityMeter.metricLabel`, loc);
        }
      }
    });
  }

  for (const h of heritageIndex) {
    validateStoryEntry(
      pack.heritage[h.id],
      ['originRegion', 'traditionLabel', 'chipTitle', 'title', 'summary', 'honestyNote', 'dependencyLabel', 'doorTitle', 'reviewer'],
      `stories/${loc}.heritage[${h.id}]`
    );
  }
}

if (errors.length > 0) {
  console.error(`\n[validate_i18n] FAILED with ${errors.length} error(s):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log(
  `[validate_i18n] PASS (${ALL_LOCALES.length} UI dictionaries + ${NEW_LOCALES.length} story packs × ${coreWishes.length} core breakthroughs × ${heritageIndex.length} heritage traditions)`
);
