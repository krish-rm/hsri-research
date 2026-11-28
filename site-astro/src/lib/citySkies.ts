export interface CitySky {
  readonly id: 'neutral' | 'mumbai' | 'dubai' | 'berlin' | 'lagos' | 'saopaulo' | 'jakarta' | 'nairobi';
  readonly name: string;
  readonly regionHint: string;
  readonly tzPrefixes: readonly string[];
  readonly imagePath: string;
}

export const HERO_CITIES: readonly CitySky[] = [
  {
    id: 'neutral',
    name: 'Coastal Harbour',
    regionHint: 'Global view',
    tzPrefixes: ['America/Toronto', 'America/New_York', 'America/Chicago', 'America/Los_Angeles'],
    imagePath: '/assets/cities/neutral.webp'
  },
  {
    id: 'mumbai',
    name: 'Mumbai',
    regionHint: 'South Asia',
    tzPrefixes: ['Asia/Kolkata', 'Asia/Calcutta'],
    imagePath: '/assets/cities/mumbai.webp'
  },
  {
    id: 'dubai',
    name: 'Dubai',
    regionHint: 'Middle East',
    tzPrefixes: ['Asia/Dubai'],
    imagePath: '/assets/cities/dubai.webp'
  },
  {
    id: 'berlin',
    name: 'Berlin',
    regionHint: 'Europe',
    tzPrefixes: ['Europe/Berlin'],
    imagePath: '/assets/cities/berlin.webp'
  },
  {
    id: 'lagos',
    name: 'Lagos',
    regionHint: 'West Africa',
    tzPrefixes: ['Africa/Lagos'],
    imagePath: '/assets/cities/lagos.webp'
  },
  {
    id: 'saopaulo',
    name: 'São Paulo',
    regionHint: 'South America',
    tzPrefixes: ['America/Sao_Paulo'],
    imagePath: '/assets/cities/saopaulo.webp'
  },
  {
    id: 'jakarta',
    name: 'Jakarta',
    regionHint: 'Southeast Asia',
    tzPrefixes: ['Asia/Jakarta'],
    imagePath: '/assets/cities/jakarta.webp'
  },
  {
    id: 'nairobi',
    name: 'Nairobi',
    regionHint: 'East Africa',
    tzPrefixes: ['Africa/Nairobi'],
    imagePath: '/assets/cities/nairobi.webp'
  }
];

export function findCityById(id: string | null | undefined): CitySky {
  return HERO_CITIES.find((c) => c.id === id) ?? HERO_CITIES[0];
}
