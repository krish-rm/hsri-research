// Structured translation dictionary for Humanity Readiness (Phase 2.5: Breakthrough & Toto pass)
// All homepage & interactive Breakthrough Player copy lives here cleanly without Section 13 jargon.

export interface DeeperCard {
  readonly title: string;
  readonly desc: string;
  readonly href: string;
  readonly tag: string;
  readonly extraLinks?: readonly { readonly label: string; readonly href: string }[];
}

export const en = {
  lang: 'en',
  dir: 'ltr' as 'ltr' | 'rtl',
  label: 'English',

  meta: {
    title:
      "Are we ready for what we're asking superintelligence to deliver? | Humanity Superintelligence Readiness Index",
    description:
      "Choose one breakthrough, trace what breaks when it arrives, and test your country's real readiness data. Open research across 39 benchmark nations."
  },

  hero: {
    eyebrow: 'A HUMANITY READINESS STORY',
    headline: "Are we ready for what we're asking superintelligence to deliver?",
    headlineLead: "Are we ready for what we're asking ",
    headlineAccent: 'superintelligence to deliver?',
    subhead:
      "Choose one breakthrough, trace what breaks when it arrives, and test your country's real readiness data.",
    ctaPrimary: 'Choose a breakthrough',
    ctaSecondary: 'See how your country does',
    guideCue: 'Start in Toto’s sky chooser:',
    ctaCountryPrimary: "Explore {country}'s breakthrough",
    ctaCountrySecondary: 'Can {country} catch it?',
    cityLabel: 'Arrival sky over:',
    cityNeutralName: 'Coastal Harbour',
    cityNeutralNote: 'Default neutral port view · pick any city to shift the horizon',
    totoCaption: 'Toto arrives at dawn: "I can deliver one breakthrough per person. Ask clearly."',
    ringTitle: "Humanity's readiness, as chosen by people like you",
    ringEmptyHeadline: 'Be one of the first 200 participants.',
    ringEmptySub: 'Crowd readiness lights up here once 200 people have completed a breakthrough.'
  },

  pulse: {
    label: "Humanity's Pulse",
    sectionKicker: 'WHY READINESS MATTERS NOW · LIVE PACE MONITOR',
    tooltipTrigger: 'Technical reading',
    states: {
      steady: {
        word: 'Steady',
        sentence:
          'Automated tools still move slowly enough for people to review decisions one by one.'
      },
      stirring: {
        word: 'Stirring',
        sentence:
          'Software systems are beginning to move faster than manual reviews. Simple backup plans are worth checking now.'
      },
      rising: {
        word: 'Rising',
        sentence:
          "This week machines got faster at multi-step tasks people used to check by hand. That's why checking plans matter."
      }
    },
    cta: 'See the live pulse'
  },

  totoCard: {
    eyebrow: 'MEET YOUR GUIDE',
    heading: 'Meet Toto.',
    body: "Toto is a fictional superintelligence we use to explore one question: what happens when humanity gets exactly what it asks for? Toto is helpful, fast, and very literal. It delivers what you ask, not always what you meant. Together you'll test each breakthrough and see how ready the world is to receive it.",
    chipsLabel: 'What Toto is and is not',
    chips: ['Fictional, not a real system', 'Helpful, never hostile', 'Literal by design'],
    ctaPrimary: 'Choose a breakthrough',
    ctaSecondary: "Read Toto's story",
    footnote:
      'Toto is a storytelling device. It is not a forecast and does not represent any real AI system.',
    svgAlt:
      'Toto, a fictional superintelligence depicted as a soft glowing dawn orb inside a thin ring'
  },

  totoIntro: {
    ariaLabel: 'First-time greeting from Toto',
    badge: 'FIRST TIME · MEET TOTO',
    lines: [
      "Hello. I'm Toto.",
      "I can deliver one breakthrough to the world. Pick what you'd like.",
      "I'll do exactly what you ask. Watch closely, then tell me how we'd know it worked."
    ] as readonly [string, string, string],
    startBtn: "Let's begin",
    skipBtn: 'Skip',
    svgAlt: 'Toto in curious pose: a warm glowing orb inside an orbital ring',
    footnote: 'Remembered quietly on this browser only (hr:v1:intro_seen) — clear anytime in Privacy.'
  },

  totoBeats: {
    speaker: 'Toto',
    wonder: 'Done.',
    wobble: "Hm. That's not quite what you meant, is it?",
    weight: 'Your turn. How would we know this worked correctly?',
    way: "Good. Here's what people can still do.",
    close: 'Every great breakthrough needs a ready world.'
  },

  totoPage: {
    eyebrow: 'STORYTELLING GUIDE · FICTION',
    title: 'Meet Toto.',
    lead: 'A fictional superintelligence used as a calm lens for exploring one question: what happens when humanity gets exactly what it asks for?',
    posesLabel: 'Toto visual poses',
    poses: [
      {
        name: 'Calm',
        caption: 'When a breakthrough arrives cleanly and people are ready to steer it.',
        alt: 'Toto in calm pose: warm dawn orb centred inside a steady orbital ring'
      },
      {
        name: 'Curious',
        caption: 'Asking the open question: "How would we know this worked?"',
        alt: 'Toto in curious pose: tilted orbital ring and attentive gaze'
      },
      {
        name: 'Apologetic',
        caption: 'Used in the Wobble when a literal delivery misses unstated context.',
        alt: 'Toto in apologetic pose: gentle amber glow signalling an unexpected catch'
      }
    ] as readonly [
      { readonly name: string; readonly caption: string; readonly alt: string },
      { readonly name: string; readonly caption: string; readonly alt: string },
      { readonly name: string; readonly caption: string; readonly alt: string }
    ],
    whoTitle: 'Who Toto is',
    whoBody:
      'A small name for a very large intelligence. The contrast is the point. Toto is helpful, fast, calm, curious, and very literal: it delivers what is asked, not always what was meant.',
    rulesTitle: "Toto's three rules",
    rules: [
      'It delivers one breakthrough per person, then always shows the cost afterwards.',
      'It never lies — and it never hides tradeoffs behind comfort.',
      'It always asks: "How would we know this worked?"'
    ],
    notTitle: 'What Toto is not',
    notBody:
      'Toto is not a forecast, not a real AI system or product, and never a villain. It is a fictional storytelling device created to pair awareness with practical human agency.',
    backCta: 'Choose a breakthrough',
    homeLink: 'Back to homepage'
  },

  doors: {
    heading: 'What would you like humanity to be handed?',
    subhead: 'Five domains. Behind each, things people have dreamed of for centuries.',
    microcopy: 'One breakthrough. About 60 seconds.',
    phase2Badge: 'Interactive 4-beat breakthrough player · live',
    sampleHeading: 'Inside this domain:',
    previewCta: 'Play a 4-beat breakthrough',
    items: [
      {
        id: 'mysteries',
        title: 'Open Problems',
        icon: 'chalkboard',
        lead: 'Deep questions nobody has cracked alone yet.',
        samples: ['Prove the Riemann Hypothesis', 'Decode ancient scripts'],
        moreCount: '+ Explain dark matter & settle P vs NP',
        wishes: [
          {
            id: 'prove-riemann-hypothesis',
            title: 'Prove the Riemann Hypothesis',
            honesty: 'Imagination',
            honestyNote:
              'Frontier AI can verify short formal lemmas, not crack open Millennium Prize proofs.',
            beatSummary:
              'Toto publishes a proof overnight — then humans discover a million pages nobody alive can check.'
          },
          {
            title: 'Decode forgotten ancient scripts',
            honesty: 'Possible soon',
            honestyNote:
              'Pattern-matching across short fragments is advancing quickly, though ground truth stays scarce.',
            beatSummary:
              'Lost inscriptions light up cleanly — until competing readings force historians to ask what counts as proof.'
          }
        ]
      },
      {
        id: 'gadgets',
        title: 'Everyday Technologies',
        icon: 'pocket',
        lead: 'Modular fabrication, universal translators, and personal life aides.',
        samples: ['Pocket workshop', 'Jarvis-style life assistant'],
        moreCount: '+ Universal translator & Time-Turner',
        wishes: [
          {
            id: 'jarvis-for-my-life',
            title: 'Jarvis-style life assistant',
            honesty: 'Possible soon',
            honestyNote:
              'Tool-using assistants already book, pay, and reply today, though reliable boundaries lag.',
            beatSummary:
              'Your week runs like magic — until a quiet outage leaves you unable to remember your own passwords.'
          },
          {
            title: 'Pocket workshop — make any tool',
            honesty: 'Imagination',
            honestyNote:
              'On-demand matter creation remains pure fiction; only digital fabrication hints at the edge.',
            beatSummary:
              'Any tool appears on request — until local repair shops disappear and nobody knows how anything is fixed.'
          }
        ]
      },
      {
        id: 'epic',
        title: 'Transformative Powers',
        icon: 'eye',
        lead: 'Shared human hopes of healing, flight, far sight, and resilience.',
        samples: ['Universal Cure (end acute illness)', 'Flight for all'],
        moreCount: '+ Planetary early warning & shared shield',
        wishes: [
          {
            id: 'sanjeevani',
            title: 'Universal Cure: end acute illness',
            honesty: 'Imagination',
            honestyNote:
              'Imagination overall — AI assists narrow molecule screening today (Possible soon for specific diseases), not universal cures.',
            beatSummary:
              'Wards empty at dawn — then hospital leaders realise every rule on care and funding assumed yesterday’s world.'
          },
          {
            title: 'Planetary early warning — spot every storm',
            honesty: 'Possible soon',
            honestyNote:
              'Global satellite and sensor streams can already track storms and infrastructure live.',
            beatSummary:
              'Every storm is visible miles ahead — alongside the realisation that everyone can watch everyone else.'
          }
        ]
      },
      {
        id: 'movie',
        title: 'Culture & Creativity',
        icon: 'frame',
        lead: 'Worlds you can step inside, rewrite, or direct in seconds.',
        samples: ['Walk into a classic film', 'Every master as my mentor'],
        moreCount: '+ Rewrite any ending & direct from text',
        wishes: [
          {
            id: 'walk-into-classic-film',
            title: 'Walk into a classic film',
            honesty: 'Possible soon',
            honestyNote:
              'Interactive 3D worlds are emerging fast, though believable long-form memory stays fragile.',
            beatSummary:
              'You step onto a rainy street that answers back — and gradually notice fewer people hanging around real cafés.'
          },
          {
            title: 'Direct a film by describing it',
            honesty: 'Real today',
            honestyNote:
              'Short generated scenes work partly today; coherent multi-hour cinema control does not yet.',
            beatSummary:
              'A feature film renders over lunch — then audiences drown in endless custom cuts with no shared story left.'
          }
        ]
      },
      {
        id: 'world',
        title: 'Public Good',
        icon: 'lamp',
        lead: 'Care, clean water, teachers, and shared memory where you live.',
        samples: ['Fix my river', 'A teacher for every child'],
        moreCount: '+ Revive a dying language & local clinics',
        wishes: [
          {
            id: 'fix-my-river',
            title: 'Fix my river',
            honesty: 'Possible soon',
            honestyNote:
              'Sensor monitoring helps spot leaks early; physical watershed restoration still takes human action.',
            beatSummary:
              'Sensors pinpoint every runoff pipe — yet nothing changes until towns agree who sacrifices profit upstream.'
          },
          {
            title: 'A teacher for every child',
            honesty: 'Possible soon',
            honestyNote:
              'Personal tutoring systems already help millions study; human mentorship and community remain irreplaceable.',
            beatSummary:
              'Every child advances smoothly at home — until elders ask what happens when neighbours stop teaching each other.'
          }
        ]
      }
    ]
  },

  beats: {
    heading: 'Every breakthrough has four moments',
    items: [
      { key: 'Wonder', desc: 'it arrives.' },
      { key: 'Wobble', desc: 'something small goes sideways.' },
      { key: 'Weight', desc: 'you spot what matters.' },
      { key: 'Way', desc: 'you see what humans can still do.' }
    ],
    footerLine: 'Every great breakthrough needs a ready world.'
  },

  lights: {
    heading: 'Your readiness, in five lights',
    items: [
      { key: 'Clarity', meaning: 'do you know what you want?' },
      { key: 'Foresight', meaning: 'did you think about side effects?' },
      { key: 'Fairness', meaning: 'did your choice include others?' },
      { key: 'Wisdom', meaning: 'what would you keep human?' },
      { key: 'Capability', meaning: 'could you actually use it?' }
    ],
    emptyState: 'Choose your first breakthrough to light your first light.',
    lowLightNote: "A dim light isn't failure. It's where to grow next.",
    trailNote:
      'Finish 3 breakthroughs to unlock your shareable Trail card; finish 5 to unlock your Shadow Map.'
  },

  country: {
    heading: 'Can your country catch the breakthrough?',
    subhead: "Pick a country. See what's already in place, and what's missing.",
    searchPlaceholder: 'Search 148 countries...',
    checklistLabel: 'A simple checklist, not a ranking',
    unratedBadge: 'Not yet rated in the full 39-nation index',
    unratedHelpCta: 'Help us rate your country',
    openCountryCta: 'Open the full country page',
    openLabCta: 'Explore deeper transitions in Open the Lab',
    techReadingLabel: 'Technical reading'
  },

  episode: {
    heading: 'This week with Toto',
    badge: 'PILOT EPISODE 1 · IN PRODUCTION',
    title: 'The First Breakthrough',
    synopsis:
      'Dawn breaks over the harbour. Meera, working the night ward shift, chooses the city’s first breakthrough. Every bed heals — and the corridor asks a question no machine settled beforehand: who goes first tomorrow?',
    voteNote: 'Interactive 3-minute story & live vote launch alongside Phase 4.',
    recapTitle: "Join Friday's recap",
    recapBody:
      'We are listening to early visitors worldwide before picking our weekly digest format. No spam, ever.',
    recapStatus: 'Recap channel opens after subscriber preferences settle.'
  },

  wishWall: {
    heading: 'What the world is asking for',
    themes: ['Health', 'Learning', 'Climate', 'Dignity', 'Wonder', 'Truth'],
    emptyHeadline: 'The "What the world is asking for" wall opens after the first 20 anonymous contributions.',
    emptyBody:
      'Every choice stays private in your browser by default. Crowd themes only appear once a threshold of at least 20 real people choose to contribute.',
    cta: 'Choose a breakthrough'
  },

  wisher: {
    heading: 'Why a great breakthrough still needs a ready world',
    cards: [
      {
        title: 'Speed',
        body: "Machines can act thousands of times faster than we can blink. So we can't just watch. We need checks built in before the breakthrough arrives.",
        techHint: 'Currently ~3,200× faster than line-by-line human review.'
      },
      {
        title: 'Dependence',
        body: "The more we hand over, the harder it is to pause. Hospitals, power, and food all run on systems we can't simply switch off. A small paper backup is worth a lot.",
        techHint: 'Measured across national grids, food logistics, and hospital triage tolerances.'
      }
    ],
    closingLine: "This is not about fear. It's about being ready to receive."
  },

  deeper: {
    heading: 'The research behind the story',
    subhead:
      'Every metaphor above rests on peer-reviewed measurements, open code, and country datasets one tap away.',
    releaseNote:
      'Preview release: 39 countries rated (mean baseline score 53.8 / 100), 96.5% data completeness (share of retained indicators observed across 39 benchmark countries — 640 of 663 cells).',
    cards: [
      {
        title: 'Open the Lab',
        desc: 'Run custom stress tests, timeline sliders, and national resilience scenarios.',
        href: '/sandbox/',
        tag: 'INTERACTIVE LAB'
      },
      {
        title: '39-country index',
        desc: 'Interactive 3D globe, full scoreboards, and detailed national dossiers.',
        href: '/countries/',
        tag: 'COUNTRY INDEX'
      },
      {
        title: 'Live Pulse',
        desc: 'Full precursor monitor (8.44 / 10), speed gap tracking, and 14 live indicators.',
        href: '/seismograph/',
        tag: 'LIVE TRACKER'
      },
      {
        title: 'Scenario Atlas',
        desc: 'Explore the 26 AI transition pathways linking behind every breakthrough.',
        href: '/scenarios/',
        tag: 'SHADOW LIBRARY'
      },
      {
        title: 'The Monograph',
        desc: '35-minute peer-reviewed paper with formal mathematical proofs (DOI 10.5281/zenodo.23441742).',
        href: '/monograph/',
        tag: '35-MIN READ'
      },
      {
        title: 'Methodology, data & coverage',
        desc: 'Inspect equations, download open CSV datasets, or see unrated country gaps.',
        href: '/methodology/',
        extraLinks: [
          { label: 'Methodology', href: '/methodology/' },
          { label: 'Data & Downloads', href: '/data/' },
          { label: 'Global Coverage Audit', href: '/coverage/' }
        ],
        tag: 'OPEN SCIENCE'
      }
    ] as readonly DeeperCard[]
  },

  player: {
    featuredLabel: 'Featured flagship breakthroughs (~60s interactive)',
    doorsBadge: 'Interactive 4-Beat Player',
    playBtn: 'Play this breakthrough',
    playedBadge: 'Played',
    previewOnlyNote: 'Preview sketch — full script opens in Phase 6',
    stepLabels: ['1. Wonder', '2. Wobble', '3. Weight', '4. Way'],
    backToDoors: 'Browse all 5 domains',
    draftTag: 'DRAFT copy awaiting owner review',
    honestyPrefix: 'Reality check:',
    foresightLead: 'Optional foresight check (lights your Foresight lamp):',
    foresightQuestion: 'Before Toto shows the catch — what could slip first?',
    foresightSkip: 'Skip straight to Wobble',
    foresightOptions: [
      'A rule or edge case nobody specified',
      'People losing the habit of checking for themselves',
      'Unfair access or hidden control',
      'Skip straight to Wobble'
    ],
    toWobbleBtn: 'See what happens next',
    toWeightBtn: 'Pause and weigh it',
    weightLead: 'What bothers me here is...',
    toWayBtn: 'See the human Way',
    wayActionTitle: 'One concrete human step',
    pledgeBtn: "I'll keep this human habit",
    pledgeDone: 'Habit pledged on this device',
    closingLine: 'Every great breakthrough needs a ready world.',
    realityTitle: 'Reality Meter',
    realityScales: {
      imagination: 'Imagination',
      possibleSoon: 'Possible soon',
      realToday: 'Real today'
    },
    realityReviewed: 'Last reviewed',
    realitySource: 'Source',
    shadowTitle: 'Behind this breakthrough (Scenario Atlas)',
    nextWishBtn: 'Play another breakthrough',
    countryHookPrefix: 'Country readiness link:',
    countryHookUnset:
      'Select your country below to see how many of 5 things it has in place for this breakthrough.',
    animPlay: 'Play animation',
    animPause: 'Pause animation',
    animReplay: 'Replay',
    transcriptBtn: 'Scene transcript',
    durationBadge: '~60s · 4 beats',
    trailSectionTitle: 'Your Readiness Trail & Shadow Map',
    trailLocked:
      'Complete 3 distinct breakthroughs to unlock your shareable Trail Card ({done}/3 done).',
    trailUnlockedBadge: 'TRAIL CARD UNLOCKED (3+ BREAKTHROUGHS)',
    shadowLocked:
      'Complete 5 distinct breakthroughs to unlock your personal Shadow Map ({done}/5 done).',
    shadowUnlockedBadge: 'SHADOW MAP UNLOCKED (5+ BREAKTHROUGHS)',
    downloadLandscape: 'Download Trail Card (1200×630 PNG)',
    downloadStory: 'Download Phone Story (1080×1920 PNG)',
    downloadShadowPng: 'Download Shadow Map (1200×630 PNG)',
    downloadSvg: 'Save Vector (.svg)',
    lightsLegend: 'Light brightness shows glow levels 0–3 locally on this browser only (no numeric rank).',
    countryCapabilityNote:
      'Country connected ({name}): {count} of 5 safeguards count toward your Capability light.',
    countryCapabilityUnset:
      'Capability currently reflects your personal Way habits only. Pick a country below to include real national data.',
    countryCapabilityUnrated:
      'Selected country ({name}) is not yet rated in the 39-nation index — your personal Way habits lead your Capability light.',
    shadows: {
      Control: 'Control',
      Dependence: 'Dependence',
      Power: 'Power',
      Truth: 'Truth',
      Speed: 'Speed'
    },
    trails: {
      Verifier: {
        name: 'The Verifier',
        note: 'You check fast answers before trusting them — asking who verifies the verifier.'
      },
      Neighbour: {
        name: 'The Neighbour',
        note: 'You ask who goes first and keep fairness and shared human dignity at the centre.'
      },
      Builder: {
        name: 'The Builder',
        note: 'You pair bold capabilities with offline fallbacks, backups, and practical community resilience.'
      },
      Keeper: {
        name: 'The Keeper',
        note: 'You hold onto human judgment, memory, and lived craft alongside superhuman speed.'
      }
    }
  },

  footerUi: {
    brandTitle: 'Humanity Superintelligence Readiness Index',
    brandDesc:
      'An open empirical benchmark measuring human judgment, institutional preparedness, and how well societies can stand on their own feet if automated cloud systems pause.',
    langHeading: 'Languages:',
    rtlActiveNotice: 'Arabic live RTL active (dir="rtl"). Layouts and reading tracks mirror automatically.',
    privacyLink: 'Privacy',
    languagesLink: 'Languages',
    totoLink: 'Toto',
    recapLink: "Join Friday's recap"
  },

  heritageUi: {
    localHorizonTag: 'Cultural horizon · {country}',
    livingBadge: 'Living tradition',
    historicalBadge: 'Historical lineage',
    seeGlobalBtn: 'Show global breakthrough',
    seeLocalBtn: 'Show {country} heritage',
    livesInOtherDoor: '{country} cultural horizon lives in {door}',
    noLocalYet: 'No local horizon added for {country} yet — explore global breakthroughs.',
    readArchiveLink: 'Sources & cultural dossier',
    reviewOpenNote: '2+ cited sources · Native review welcome',
    weightBindingTitle: 'Real delivery check for {country}',
    weightRatedInPlace: 'In place',
    weightRatedGap: 'Bottleneck observed',
    weightContextNote: '{country} has partial data tracking ({region}) — {observed}',
    weightNoCountry: 'Pick any country below to check this delivery dependency against real national data.',
    wayTestCountryCta: "Test {country}'s safeguard in Country Check",
    trailStampLabel: 'Cultural horizons explored: {count}',
    autoDetectedHint: 'Auto sky · pick any country',
    perspectiveBadge: 'Perspective · {country}',
    resetGlobalBtn: 'Global view',
    countryHeadingTradition: "From {country}'s perspective: {tradition}",
    countryHeadingGlobal: "From {country}'s perspective: Test a breakthrough",
    countrySubhead: 'See what happens when an AI breakthrough meets local reality in {country}.',
    flowWonder: 'Dream arrives',
    flowWobble: 'Local strain',
    flowCatch: '{country} catch',
    otherDomainsLabel: "Explore all 5 domains from {country}'s perspective:",
    otherTraditionsLabel: 'Compare world traditions:',
    lightsCountryHeading: "{country}'s 5 Readiness Lights",
    lightsHumanGroup: 'Your human choices',
    lightsCountryGroup: '{country} capacity',
    countryCatchHeading: 'Can {country} catch it?',
    traditionTestsLabel: 'Tradition lens:',
    coverageObservedLabel: 'Observed safeguards',
    coverageMissingLabel: 'Unmeasured gaps (never guessed)'
  }
};

type DeepStringWiden<T> = T extends string
  ? string
  : T extends boolean
  ? boolean
  : T extends readonly (infer U)[]
  ? readonly DeepStringWiden<U>[]
  : T extends object
  ? { readonly [K in keyof T]: DeepStringWiden<T[K]> }
  : T;

export type TranslationDict = DeepStringWiden<typeof en>;
export type LocaleKey = 'en' | 'es' | 'ar' | 'rtl-stub';
