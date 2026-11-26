// Build-time JSON Schema & Scientific Integrity Validator for breakthrough records
// Validates BOTH wishes.json (active 5 breakthroughs) AND wishes.draft15.json (dev-only 15 drafts).
// Fails build on missing fields, invalid SC-xx atlasRefs, missing Reality Meter scale/source/date,
// Section 13 banned jargon, or retired Phase 1-2 terms ("wish", "kalpa", "wishgiver").
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const schemaPath = path.join(root, 'src/data/wishes.schema.json');
const wishesPath = path.join(root, 'src/data/wishes.json');
const draft15Path = path.join(root, 'src/data/wishes.draft15.json');
const atlasPath = path.join(root, 'src/data/asi_scenarios.json');

const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
const coreList = JSON.parse(fs.readFileSync(wishesPath, 'utf8'));
const draft15List = fs.existsSync(draft15Path) ? JSON.parse(fs.readFileSync(draft15Path, 'utf8')) : [];
const allRecords = [
  ...coreList.map((w, i) => ({ w, src: 'wishes.json', idx: i })),
  ...draft15List.map((w, i) => ({ w, src: 'wishes.draft15.json', idx: i }))
];

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

const RETIRED_TERMS =
  /\b(wish|wishes|wished|wishing|wisher|wishers|wishgiver|kalpa)\b|dese(o|os|a|as|ar|aría|arías|ando|ado)|أمني(ة|ات)|متمن|كالبا|تتمن|نتمنا/i;

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
          errors.push(`${p}.${k}: contains banned homepage/breakthrough jargon matching /${pat}/`);
        }
      }
      if (RETIRED_TERMS.test(val[k])) {
        errors.push(`${p}.${k}: contains retired terminology ("wish"/"Kalpa"): ${val[k]}`);
      }
    }
  }
}

if (!Array.isArray(coreList) || coreList.length < schema.minItems) {
  errors.push(`wishes.json must contain at least ${schema.minItems} breakthrough records`);
}

const VALID_DOORS = new Set(schema.items.properties.door.enum);
const VALID_ICONS = new Set(schema.items.properties.icon.enum);
const VALID_STATUS = new Set(schema.items.properties.status.enum); // ['draft', 'owner_approved']
const VALID_HONESTY = new Set(schema.items.properties.honestyLabel.enum);
const VALID_SCALES = new Set(schema.items.properties.realityMeter.properties.scale.enum);
const VALID_SHADOWS = new Set(schema.items.properties.shadowTag.enum);
const VALID_LIGHTS = new Set(['Clarity', 'Foresight', 'Fairness', 'Wisdom', 'Capability']);

const seenIds = new Set();

for (const { w, src, idx } of allRecords) {
  const tag = `${src}[${idx}](${w?.id || 'unknown'})`;
  for (const reqKey of schema.items.required) {
    if (w[reqKey] === undefined || w[reqKey] === null) {
      errors.push(`${tag}: missing required property '${reqKey}'`);
    }
  }
  if (!w.id || !/^[a-z0-9-]+$/.test(w.id)) errors.push(`${tag}: invalid id`);
  if (seenIds.has(w.id)) errors.push(`${tag}: duplicate id '${w.id}'`);
  seenIds.add(w.id);

  if (!VALID_DOORS.has(w.door)) errors.push(`${tag}: invalid domain key '${w.door}'`);
  if (!VALID_ICONS.has(w.icon)) errors.push(`${tag}: invalid icon '${w.icon}'`);
  if (!VALID_STATUS.has(w.status)) errors.push(`${tag}: invalid status '${w.status}' (must be draft or owner_approved)`);
  if (typeof w.devOnly !== 'boolean') errors.push(`${tag}: devOnly must be boolean`);
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
  checkLoc(w.wonder?.totoLine, `${tag}.wonder.totoLine`);
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

  if (w.closingLine !== 'Every great breakthrough needs a ready world.') {
    errors.push(`${tag}.closingLine: must equal 'Every great breakthrough needs a ready world.'`);
  }

  const rm = w.realityMeter;
  if (!rm || !VALID_SCALES.has(rm.scale)) {
    errors.push(`${tag}.realityMeter.scale: must be Imagination, Possible soon, or Real today`);
  }
  checkLoc(rm?.reason, `${tag}.realityMeter.reason`);
  if (rm?.observedMetric !== undefined && rm?.observedMetric !== null) {
    if (!rm.observedMetric.directCapabilityMatch || typeof rm.observedMetric.value !== 'string') {
      errors.push(`${tag}.realityMeter.observedMetric: numeric metric requires directCapabilityMatch === true`);
    }
    checkLoc(rm.observedMetric.label, `${tag}.realityMeter.observedMetric.label`);
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
}

for (const reqId of ['sanjeevani', 'jarvis-for-my-life', 'prove-riemann-hypothesis']) {
  if (!seenIds.has(reqId)) {
    errors.push(`Missing required Phase 2 flagship breakthrough '${reqId}'`);
  }
}

if (errors.length > 0) {
  console.error('BREAKTHROUGH VALIDATION FAILED:\n - ' + errors.join('\n - '));
  process.exit(1);
}

console.log(`validate_wishes: OK (${coreList.length} core + ${draft15List.length} dev-flagged = ${allRecords.length} breakthroughs validated against 3-step Reality Meter schema, ${validAtlasIds.size} Atlas IDs checked, 0 jargon or retired-term violations)`);
