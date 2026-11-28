// Build-time Integrity Validator for Country & Civilizational Heritage Traditions
// Ensures >=2 real sources, valid HSRI metric bindings, zero banned jargon or retired words,
// valid ISO codes matching country_catch_catalog.json, valid SC-xx IDs, and 360px length caps.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const indexPath = path.join(root, 'src/data/heritage/index.json');
const scriptsDir = path.join(root, 'src/data/heritage/scripts');
const atlasPath = path.join(root, 'src/data/asi_scenarios.json');
const catalogPath = path.join(root, 'src/data/country_catch_catalog.json');

const atlasRaw = JSON.parse(fs.readFileSync(atlasPath, 'utf8'));
const atlasList = Array.isArray(atlasRaw) ? atlasRaw : atlasRaw.scenarios || Object.values(atlasRaw);
const validAtlasIds = new Set(atlasList.map((s) => s.id || s.code).filter(Boolean));

const validIsos = new Set(
  JSON.parse(fs.readFileSync(catalogPath, 'utf8')).map((c) => c.iso).filter(Boolean)
);

const VALID_DOORS = new Set(['mysteries', 'gadgets', 'epic', 'movie', 'world']);
const VALID_METRICS = new Set(['t_half', 'infrastructure', 'discernment', 'governance', 'p8_post_labor']);
const VALID_HONESTY = new Set(['Imagination', 'Possible soon', 'Real today']);
const VALID_ERA = new Set(['living', 'historical']);
const VALID_STATUS = new Set(['review_open', 'published']);

const BANNED_JARGON = [
  'leontief',
  'weakest-link floor',
  "rice['’]?s theorem",
  'verification latency wedge',
  'solvency ii',
  'naic rbc',
  'econometric',
  'decoupling half-life',
  'sovereign autarky',
  'telemetry',
  'tripwire',
  'vassal',
  'archetype'
];

const RETIRED_TERMS =
  /\b(wish|wishes|wished|wishing|wisher|wishers|wishgiver|kalpa)\b|dese(o|os|a|as|ar|aría|arías|ando|ado)|أمني(ة|ات)|متمن|كالبا|تتمن|نتمنا/i;

const errors = [];

function checkLoc(val, label, maxLen = 420) {
  if (!val || typeof val !== 'object') {
    errors.push(`${label}: expected localized {en, es, ar} object`);
    return;
  }
  for (const k of ['en', 'es', 'ar']) {
    if (typeof val[k] !== 'string' || val[k].trim().length === 0) {
      errors.push(`${label}.${k}: missing non-empty string`);
      continue;
    }
    if (val[k].length > maxLen) {
      errors.push(`${label}.${k}: exceeds ${maxLen} char budget (${val[k].length} chars)`);
    }
    for (const pat of BANNED_JARGON) {
      if (new RegExp(pat, 'i').test(val[k])) {
        errors.push(`${label}.${k}: contains banned jargon /${pat}/`);
      }
    }
    if (RETIRED_TERMS.test(val[k])) {
      errors.push(`${label}.${k}: contains retired word ("wish"/"Kalpa"): ${val[k]}`);
    }
  }
}

const indexList = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
if (!Array.isArray(indexList) || indexList.length < 5) {
  errors.push('heritage/index.json must contain at least 5 heritage traditions');
}

const seenIds = new Set();
const coveredCountries = new Set();

for (const idxItem of indexList) {
  const filePath = path.join(scriptsDir, `${idxItem.id}.json`);
  if (!fs.existsSync(filePath)) {
    errors.push(`Missing script file for ${idxItem.id}: ${filePath}`);
    continue;
  }
  const rec = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const tag = `heritage(${rec.id})`;

  if (!rec.id || !/^[a-z0-9-]+$/.test(rec.id)) errors.push(`${tag}: invalid id`);
  if (seenIds.has(rec.id)) errors.push(`${tag}: duplicate id`);
  seenIds.add(rec.id);

  if (!VALID_DOORS.has(rec.door)) errors.push(`${tag}: invalid door ${rec.door}`);
  if (!VALID_ERA.has(rec.era)) errors.push(`${tag}: invalid era ${rec.era}`);
  if (!VALID_STATUS.has(rec.status)) errors.push(`${tag}: invalid status ${rec.status}`);
  if (!VALID_HONESTY.has(rec.honestyLabel)) errors.push(`${tag}: invalid honestyLabel ${rec.honestyLabel}`);

  if (!rec.binding || !VALID_METRICS.has(rec.binding.primary)) {
    errors.push(`${tag}: invalid primary binding metric '${rec.binding?.primary}'`);
  }
  if (rec.binding?.secondary && !VALID_METRICS.has(rec.binding.secondary)) {
    errors.push(`${tag}: invalid secondary binding metric '${rec.binding.secondary}'`);
  }
  checkLoc(rec.binding?.dependencyLabel, `${tag}.binding.dependencyLabel`, 140);

  if (!Array.isArray(rec.countries) || rec.countries.length === 0) {
    errors.push(`${tag}: must list at least 1 valid country ISO`);
  } else {
    for (const iso of rec.countries) {
      if (!validIsos.has(iso)) errors.push(`${tag}: unknown ISO code '${iso}'`);
      coveredCountries.add(iso);
    }
  }

  if (!Array.isArray(rec.atlasRefs) || rec.atlasRefs.length === 0) {
    errors.push(`${tag}: must reference at least 1 SC-xx Atlas pathway`);
  } else {
    for (const sc of rec.atlasRefs) {
      if (!validAtlasIds.has(sc)) errors.push(`${tag}: unknown atlasRef '${sc}'`);
    }
  }

  if (!Array.isArray(rec.sources) || rec.sources.length < 2) {
    errors.push(`${tag}: requires >= 2 cited sources`);
  } else {
    for (const src of rec.sources) {
      if (!src.title || !src.url || (!src.url.startsWith('https://') && !src.url.startsWith('/'))) {
        errors.push(`${tag}: invalid source entry ${JSON.stringify(src)}`);
      }
    }
  }

  if (!rec.reviewers || !rec.reviewers.en || !rec.reviewers.es || !rec.reviewers.ar) {
    errors.push(`${tag}: missing per-locale reviewers metadata`);
  }

  checkLoc(rec.traditionLabel, `${tag}.traditionLabel`, 56);
  checkLoc(rec.chipTitle, `${tag}.chipTitle`, 72);
  checkLoc(rec.title, `${tag}.title`, 96);
  checkLoc(rec.summary, `${tag}.summary`, 180);
  checkLoc(rec.honestyNote, `${tag}.honestyNote`, 220);
  checkLoc(rec.wonder?.text, `${tag}.wonder.text`, 360);
  checkLoc(rec.wonder?.totoLine, `${tag}.wonder.totoLine`, 90);
  checkLoc(rec.wobble?.text, `${tag}.wobble.text`, 360);
  checkLoc(rec.weight?.question, `${tag}.weight.question`, 160);
  checkLoc(rec.way?.text, `${tag}.way.text`, 360);
  checkLoc(rec.way?.actionCardTitle, `${tag}.way.actionCardTitle`, 90);
  checkLoc(rec.way?.actionCardStep, `${tag}.way.actionCardStep`, 220);
  checkLoc(rec.way?.pledgeLabel, `${tag}.way.pledgeLabel`, 80);

  if (!Array.isArray(rec.weight?.options) || rec.weight.options.length !== 3) {
    errors.push(`${tag}: weight.options must have 3 choices`);
  } else {
    for (const opt of rec.weight.options) {
      checkLoc(opt.text, `${tag}.weight.options[${opt.id}]`, 140);
    }
  }

  if (rec.closingLine !== 'Every great breakthrough needs a ready world.') {
    errors.push(`${tag}: invalid closingLine`);
  }
}

if (errors.length > 0) {
  console.error('HERITAGE VALIDATION FAILED:');
  for (const e of errors) console.error(' -', e);
  process.exit(1);
}

console.log(
  `validate_heritage: OK (${indexList.length} cited traditions validated across ${coveredCountries.size} countries, EN/ES/AR checked, 0 banned terms)`
);
