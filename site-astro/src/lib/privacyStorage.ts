// Anonymous local-first browser state helper (prefix: hr:v1:*)
// Zero PII, zero cookies, zero external telemetry transmission in Phases 1-2.

export const HR_STORAGE_PREFIX = 'hr:v1:';

export type FunnelEventName =
  | 'hero_cta_click'
  | 'hero_city_switch'
  | 'door_preview_select'
  | 'toto_intro_seen'
  | 'breakthrough_started'
  | 'foresight_guess'
  | 'weight_choice'
  | 'way_pledge'
  | 'breakthrough_completed'
  | 'light_gained'
  | 'share_clicked'
  | 'country_selected'
  | 'locale_switched';

export interface LocalEventRecord {
  event: FunnelEventName;
  meta?: Record<string, string | number>;
  ts: string;
}

export function trackEvent(event: FunnelEventName, meta?: Record<string, string | number>) {
  if (typeof window === 'undefined') return;
  try {
    const key = `${HR_STORAGE_PREFIX}events`;
    const raw = localStorage.getItem(key);
    const list: LocalEventRecord[] = raw ? JSON.parse(raw) : [];
    const next: LocalEventRecord[] = [
      ...list.slice(-49),
      { event, meta, ts: new Date().toISOString() }
    ];
    localStorage.setItem(key, JSON.stringify(next));
  } catch {
    // Gracefully skip if storage is unavailable
  }
}

export function readAllLocalData(): Record<string, unknown> {
  if (typeof window === 'undefined') return {};
  const out: Record<string, unknown> = {};
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(HR_STORAGE_PREFIX)) {
        const val = localStorage.getItem(key);
        try {
          out[key] = val ? JSON.parse(val) : null;
        } catch {
          out[key] = val;
        }
      }
    }
  } catch {
    return {};
  }
  return out;
}

export function clearAllLocalData(): number {
  if (typeof window === 'undefined') return 0;
  let removed = 0;
  try {
    const keys: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(HR_STORAGE_PREFIX)) keys.push(key);
    }
    keys.forEach((k) => {
      localStorage.removeItem(k);
      removed += 1;
    });
  } catch {
    return 0;
  }
  return removed;
}
