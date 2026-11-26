// Build-time server helper (Node only inside Astro frontmatter)
// Produces compact, strictly non-fabricated country summaries from authoritative HSRI data.
// Never imports full sandbox timeseries onto homepage client bundles.
import fs from 'node:fs';
import path from 'node:path';
import countryScores from '../data/country_scores.json';

export interface RatedCountrySummary {
  kind: 'rated';
  iso: string;
  id: string;
  name: string;
  region: string;
  rankL1: number;
  rankL2: number;
  rankDelta: number;
  tHalfH: number;
  cloudDaysText: string;
  batterySegments: number;
  catchStatus: 'Easily' | 'With effort' | 'Struggles';
  plainPattern: string;
  plainPatternTech: string;
  weakestLinkPlain: string;
  weakestLinkTech: string;
  checklistCount: number;
  checklist: Array<{ label: string; pass: boolean; metricNote: string }>;
}

export interface UnratedCountrySummary {
  kind: 'unrated';
  iso: string;
  name: string;
  region: string;
  observedSummary: string;
  missingSummary: string;
  coverageDetail: string;
}

export type CountrySummaryItem = RatedCountrySummary | UnratedCountrySummary;

function parseCsvRow(line: string): string[] {
  const out: string[] = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      inQuotes = !inQuotes;
      continue;
    }
    if (ch === ',' && !inQuotes) {
      out.push(cur.trim());
      cur = '';
      continue;
    }
    cur += ch;
  }
  out.push(cur.trim());
  return out;
}

function formatDaysOffline(hours: number): { text: string; segments: number } {
  if (hours < 24) {
    return { text: `Under 1 day (${hours}h)`, segments: 1 };
  }
  const days = Math.round(hours / 24);
  const segs = hours >= 720 ? 5 : hours >= 336 ? 4 : hours >= 168 ? 3 : hours >= 72 ? 2 : 1;
  return { text: days === 1 ? '1 day' : `${days} days`, segments: segs };
}

function deriveWeakestLinkPlain(bottleneck: string, countryName: string): string {
  const b = (bottleneck || '').toLowerCase();
  if (b.includes('post-labor') || b.includes('p8')) {
    return `Keeping livelihoods and public budgets steady in ${countryName} if office and knowledge roles automate faster than tax rules adapt.`;
  }
  if (b.includes('decoupling') || b.includes('p6')) {
    return `Running hospitals, ports, and daily services in ${countryName} if foreign cloud systems suddenly pause.`;
  }
  if (b.includes('epistemic') || b.includes('p5')) {
    return `Giving people reliable ways in ${countryName} to verify fast automated claims independently.`;
  }
  return `Balancing fast adoption in ${countryName} with manual human fallbacks (${bottleneck}).`;
}

function derivePlainPattern(c: any): { plain: string; tech: string } {
  if (c.H_L2 >= 0.40 && c.rank_delta >= -2) {
    return {
      plain: 'Steady Offline Builder',
      tech: `Strong baseline offline capacity (Tier ${c.band}, Rank #${c.rank_L2} resilience). Full simulation labels live in Open the Lab.`
    };
  }
  if (c.high_compute_trap && c.rank_delta < -5) {
    return {
      plain: 'Fast Digital Adopter',
      tech: `High adoption rank (#${c.rank_L1}) paired with heavy dependence on continuous cloud connectivity (Rank shift ${c.rank_delta}). Full simulation labels live in Open the Lab.`
    };
  }
  return {
    plain: 'Balanced Contender',
    tech: `Mixed adoption and physical reserve buffers (Layer 2 resilience rank #${c.rank_L2}). Full simulation labels live in Open the Lab.`
  };
}

export function buildCountryWidgetCatalog(): CountrySummaryItem[] {
  const rated: RatedCountrySummary[] = countryScores.countries.map((c: any) => {
    const cleanName = c.code === 'MKD' ? 'North Macedonia' : c.name;
    const { text: cloudDaysText, segments: batterySegments } = formatDaysOffline(c.T_half_h);

    const catchStatus: RatedCountrySummary['catchStatus'] =
      c.H_L2 >= 0.40 && c.rank_delta >= -2
        ? 'Easily'
        : c.rank_delta >= -5
          ? 'With effort'
          : 'Struggles';

    const pattern = derivePlainPattern(c);

    // Decision #2: Strict 5-check binary checklist using 72h analog override & editorial 70-pt thresholds
    const pInfra = Number(c.pillars?.digital_infrastructure ?? 0);
    const pDiscern = Number(c.pillars?.critical_discernment ?? 0);
    const pGov = Number(c.pillars?.institutional_governance ?? 0);
    const p8 = Number(c.layer2_pillars?.p8_post_labor ?? 0);

    const checklist = [
      {
        label: 'At least 72 hours of offline backup capacity',
        pass: c.T_half_h >= 72,
        metricNote: `Observed window: ${c.T_half_h} hours (threshold: 72h)`
      },
      {
        label: 'Everyday digital & grid foundation',
        pass: pInfra >= 70,
        metricNote: `Infrastructure score: ${pInfra.toFixed(1)} / 100 (editorial cutoff: 70)`
      },
      {
        label: 'Public skill at double-checking AI claims',
        pass: pDiscern >= 70,
        metricNote: `Public discernment score: ${pDiscern.toFixed(1)} / 100 (editorial cutoff: 70)`
      },
      {
        label: 'Clear public rules & oversight bodies',
        pass: pGov >= 70,
        metricNote: `Governance score: ${pGov.toFixed(1)} / 100 (editorial cutoff: 70)`
      },
      {
        label: 'Livelihood & public budget cushion',
        pass: p8 >= 0.25,
        metricNote: `Economic shock cushion: ${(p8 * 100).toFixed(0)} / 100 (editorial cutoff: 25)`
      }
    ];

    return {
      kind: 'rated',
      iso: c.code,
      id: c.id,
      name: cleanName,
      region: c.region,
      rankL1: c.rank_L1,
      rankL2: c.rank_L2,
      rankDelta: c.rank_delta,
      tHalfH: c.T_half_h,
      cloudDaysText,
      batterySegments,
      catchStatus,
      plainPattern: pattern.plain,
      plainPatternTech: pattern.tech,
      weakestLinkPlain: deriveWeakestLinkPlain(c.bottleneck_pillar, cleanName),
      weakestLinkTech: c.bottleneck_pillar,
      checklistCount: checklist.filter((i) => i.pass).length,
      checklist
    };
  });

  // Merge unrated + context-only countries strictly equally without fabricating any metric
  const ratedIsos = new Set(rated.map((r) => r.iso));
  const seenNames = new Set(rated.map((r) => r.name.toLowerCase()));
  const unrated: UnratedCountrySummary[] = [];

  const dataRoot = fs.existsSync(path.resolve(process.cwd(), '../data'))
    ? path.resolve(process.cwd(), '../data')
    : path.resolve(process.cwd(), 'data');
  const unratedCsvPath = path.join(dataRoot, 'unrated-nations.csv');
  const coverageCsvPath = path.join(dataRoot, 'coverage-by-country.csv');

  if (fs.existsSync(unratedCsvPath)) {
    const lines = fs.readFileSync(unratedCsvPath, 'utf-8').trim().split(/\r?\n/).slice(1);
    for (const line of lines) {
      if (!line.trim()) continue;
      const [iso, name, region, _sub, availStr, missingPillars, _gap, notes] = parseCsvRow(line);
      if (!ratedIsos.has(iso) && !seenNames.has(name.toLowerCase())) {
        ratedIsos.add(iso);
        seenNames.add(name.toLowerCase());
        const avail = Number(availStr) || 0;
        unrated.push({
          kind: 'unrated',
          iso,
          name,
          region,
          observedSummary:
            avail === 0
              ? 'No core pillar microdata collected yet.'
              : `${avail} of 4 baseline pillars have partial international tracking.`,
          missingSummary: missingPillars
            ? `Missing international surveys for: ${missingPillars.replace(/;/g, ',')}.`
            : 'Missing comparable cross-national survey data.',
          coverageDetail: (notes || 'Insufficient verified survey data for full scoring.').replace(/\btelemetry\b/gi, 'survey tracking')
        });
      }
    }
  }

  if (fs.existsSync(coverageCsvPath)) {
    const lines = fs.readFileSync(coverageCsvPath, 'utf-8').trim().split(/\r?\n/).slice(1);
    for (const line of lines) {
      if (!line.trim()) continue;
      const cols = parseCsvRow(line);
      const [iso, name, litC, litX, trust, metaC, metaX, dec, att, val, enab, totStr, status] = cols;
      if (!ratedIsos.has(iso) && !seenNames.has(name.toLowerCase())) {
        ratedIsos.add(iso);
        seenNames.add(name.toLowerCase());
        const fields: Array<[string, string]> = [
          [litC, 'AI Literacy (Core)'],
          [litX, 'AI Literacy (Context)'],
          [trust, 'Calibrated Trust'],
          [metaC, 'Critical Discernment (Core)'],
          [metaX, 'Critical Discernment (Context)'],
          [dec, 'Decision Agency'],
          [att, 'Attentional Context'],
          [val, 'Value Clarity'],
          [enab, 'Enabling Infrastructure']
        ];
        const observedDomains = fields.filter(([v]) => v === '1').map(([, label]) => label);
        const missingDomains = fields.filter(([v]) => v !== '1').map(([, label]) => label);

        unrated.push({
          kind: 'unrated',
          iso,
          name,
          region: status === 'Partial rating' ? 'Partial Rating (Non-Benchmark)' : status === 'Context-only' ? 'Context-Only Coverage' : status || 'Not Rated',
          observedSummary:
            observedDomains.length > 0
              ? `${observedDomains.length}/9 coverage flags observed: ${observedDomains.join(', ')}.`
              : 'Minimal contextual data recorded.',
          missingSummary:
            missingDomains.length > 0
              ? `Missing coverage indicators (${missingDomains.length}/9): ${missingDomains.join(', ')}.`
              : 'None of the 9 coverage indicators are missing.',
          coverageDetail: `Source coverage-by-country.csv status "${status || 'Context-only'}": excluded from the 39-nation benchmark until comparable cross-pillar microdata exists.`
        });
      }
    }
  }

  const all = [...rated, ...unrated];
  all.sort((a, b) => a.name.localeCompare(b.name));
  return all;
}
