// Build-time JSON Schema & Scientific Integrity Validator for wishes.json
// Fails Astro build on any missing field, invalid SC-xx atlasRef, missing source/lastReviewed, or banned jargon.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const schemaPath = path.join(root, 'src/data/wishes.schema.json');
const wishesPath = path.join(root, 'src/data/wishes.json');
const atlasPath = path.join(root, 'src/data/asi_scenarios.json');

const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
const wishes = JSON.parse(fs.readFileSync(wishesPath, 'utf8'));
const atlasRaw = JSON.parse(fs.readFileSync(atlasPath, 'utf8'));

const atlasList = Array.isArray(atlasRaw) ? atlasRaw : atlasRaw.scenarios || Object.values(atlasRaw);
const validAtlasIds = new Set(atlasList.map((s) => s.id || s.code).filter(Boolean));

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

const errors = [];

function checkLoc(val, p) {
  if (!val || typeof val !== 'object') {
    errors.push(`${p}: expected localized {en, es, ar} object`);
    return;
  }
  for (const k of ['en', 'es', 'ar']) {
    if (typeof val[k] !== 'string' || val[k].trim().length === 0) {
      errors.push(`${p}.${k}: missing non-empty string`);
    } else {
      for (const pat of BANNED_JARGON) {
        if (new RegExp(pat, 'i').test(val[k])) {
          errors.push(`${p}.${k}: contains banned homepage/wish jargon matching /${pat}/`);
        }
      }
    }
  }
}

if (!Array.isArray(wishes) || wishes.length < schema.minItems) {
  errors.push(`wishes.json must contain at least ${schema.minItems} wishes`);
}

const VALID_DOORS = new Set(schema.items.properties.door.enum);
const VALID_ICONS = new Set(schema.items.properties.icon.enum);
const VALID_HONESTY = new Set(schema.items.properties.honestyLabel.enum);
const VALID_SHADOWS = new Set(schema.items.properties.shadowTag.enum);
const VALID_LIGHTS = new Set(['Clarity', 'Foresight', 'Fairness', 'Wisdom', 'Capability']);

const seenIds = new Set();

for (const [idx, w] of (Array.isArray(wishes) ? wishes : []).entries()) {
  const tag = `wish[${idx}](${w?.id || 'unknown'})`;
  for (const reqKey of schema.items.required) {
    if (w[reqKey] === undefined || w[reqKey] === null) {
      errors.push(`${tag}: missing required property '${reqKey}'`);
    }
  }
  if (!w.id || !/^[a-z0-9-]+$/.test(w.id)) errors.push(`${tag}: invalid id`);
  if (seenIds.has(w.id)) errors.push(`${tag}: duplicate wish id '${w.id}'`);
  seenIds.add(w.id);

  if (!VALID_DOORS.has(w.door)) errors.push(`${tag}: invalid door '${w.door}'`);
  if (!VALID_ICONS.has(w.icon)) errors.push(`${tag}: invalid icon '${w.icon}'`);
  if (!VALID_HONESTY.has(w.honestyLabel)) errors.push(`${tag}: invalid honestyLabel '${w.honestyLabel}'`);
  if (!VALID_SHADOWS.has(w.shadowTag)) errors.push(`${tag}: invalid shadowTag '${w.shadowTag}'`);

  checkLoc(w.title, `${tag}.title`);
  checkLoc(w.doorTitle, `${tag}.doorTitle`);
  checkLoc(w.honestyNote, `${tag}.honestyNote`);

  if (!Array.isArray(w.atlasRefs) || w.atlasRefs.length === 0) {
    errors.push(`${tag}: atlasRefs must contain at least 1 valid SC-xx ID`);
  } else {
    for (const ref of w.atlasRefs) {
      if (!validAtlasIds.has(ref)) {
        errors.push(`${tag}: unknown atlasRef '${ref}' not found in asi_scenarios.json`);
      }
    }
  }

  checkLoc(w.wonder?.text, `${tag}.wonder.text`);
  checkLoc(w.wonder?.kalpaLine, `${tag}.wonder.kalpaLine`);
  checkLoc(w.wonder?.transcript, `${tag}.wonder.transcript`);

  checkLoc(w.wobble?.text, `${tag}.wobble.text`);
  checkLoc(w.wobble?.transcript, `${tag}.wobble.transcript`);

  checkLoc(w.weight?.question, `${tag}.weight.question`);
  checkLoc(w.weight?.transcript, `${tag}.weight.transcript`);
  if (!Array.isArray(w.weight?.options) || w.weight.options.length !== 3) {
    errors.push(`${tag}.weight.options: must contain exactly 3 choices`);
  } else {
    for (const opt of w.weight.options) {
      checkLoc(opt.text, `${tag}.weight.options[${opt.id}].text`);
      if (!VALID_LIGHTS.has(opt.light)) errors.push(`${tag}.weight.options[${opt.id}]: invalid light '${opt.light}'`);
      if (!VALID_SHADOWS.has(opt.shadow)) errors.push(`${tag}.weight.options[${opt.id}]: invalid shadow '${opt.shadow}'`);
    }
  }

  checkLoc(w.way?.text, `${tag}.way.text`);
  checkLoc(w.way?.actionCardTitle, `${tag}.way.actionCardTitle`);
  checkLoc(w.way?.actionCardStep, `${tag}.way.actionCardStep`);
  checkLoc(w.way?.pledgeLabel, `${tag}.way.pledgeLabel`);
  checkLoc(w.way?.transcript, `${tag}.way.transcript`);

  if (w.closingLine !== 'Every great wish needs a good wisher.') {
    errors.push(`${tag}.closingLine: must equal 'Every great wish needs a good wisher.'`);
  }

  const rm = w.realityMeter;
  if (!rm || typeof rm.score !== 'number' || rm.score < 0 || rm.score > 100) {
    errors.push(`${tag}.realityMeter.score: must be integer 0..100`);
  }
  if (!rm?.source || typeof rm.source !== 'string' || rm.source.trim().length < 5) {
    errors.push(`${tag}.realityMeter.source: required source string missing`);
  }
  if (!rm?.sourceUrl || typeof rm.sourceUrl !== 'string') {
    errors.push(`${tag}.realityMeter.sourceUrl: required URL or route missing`);
  }
  if (!rm?.lastReviewed || !/^\d{4}-\d{2}-\d{2}$/.test(rm.lastReviewed)) {
    errors.push(`${tag}.realityMeter.lastReviewed: must be YYYY-MM-DD`);
  }
  checkLoc(rm?.statusLabel, `${tag}.realityMeter.statusLabel`);
  checkLoc(rm?.note, `${tag}.realityMeter.note`);
}

// Verify all 3 required Phase 2 wishes exist
for (const reqWish of ['sanjeevani', 'jarvis-for-my-life', 'prove-riemann-hypothesis']) {
  if (!seenIds.has(reqWish)) {
    errors.push(`Missing required Phase 2 flagship wish '${reqWish}'`);
  }
}

if (errors.length > 0) {
  console.error('WISH VALIDATION FAILED:\n - ' + errors.join('\n - '));
  process.exit(1);
}

console.log(`validate_wishes: OK (${wishes.length} wishes validated against schema, ${validAtlasIds.size} Atlas IDs checked, 0 jargon violations)`);
