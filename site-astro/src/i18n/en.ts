// Structured translation dictionary for Humanity Readiness (Phase 1+ global i18n)
// All homepage & interactive copy lives here cleanly without Section 12 jargon.

export const en = {
  lang: 'en',
  dir: 'ltr' as const,
  label: 'English',

  meta: {
    title: "Humanity Readiness: are we ready to receive what we're wishing for? | Humanity Superintelligence Readiness Index",
    description:
      "Imagine a superintelligence offers you one wish. Pick it, watch it come true, and see what humans can still do. Backed by open research across 39 benchmark nations."
  },

  hero: {
    eyebrow: 'A HUMANITY READINESS STORY',
    headline: "Humanity Readiness: are we ready to receive what we're wishing for?",
    subhead:
      'Imagine a superintelligence offers you one wish. Pick it. Watch it come true. Then see what it would really take.',
    ctaPrimary: 'Make your wish',
    ctaSecondary: 'See how your country does',
    cityLabel: 'Arrival sky over:',
    cityNeutralName: 'Coastal Harbour',
    cityNeutralNote: 'Default neutral port view · pick any city to shift the horizon',
    kalpaCaption: 'Kalpa arrives at dawn: "I can offer one wish per person. Ask clearly."',
    ringTitle: "Humanity's readiness, as chosen by people like you",
    ringEmptyHeadline: 'Be one of the first 200 wishers.',
    ringEmptySub: 'Crowd readiness lights up here once 200 people have completed a wish.'
  },

  pulse: {
    label: "Humanity's Pulse",
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

  doors: {
    heading: 'What would you wish for?',
    subhead: 'Five doors. Behind each, things people have dreamed of for centuries.',
    microcopy: 'One wish. About 60 seconds.',
    phase2Badge: 'Interactive wish player opens in Phase 2 — preview the 4 moments below',
    sampleHeading: 'Inside this door:',
    previewCta: 'Preview these 4 moments',
    items: [
      {
        id: 'mysteries',
        title: 'Unsolved Mysteries',
        icon: 'chalkboard',
        lead: 'Deep questions nobody has cracked alone yet.',
        samples: ['Prove the Riemann Hypothesis', 'Read the Indus script'],
        moreCount: '+ Explain dark matter & P vs NP',
        wishes: [
          {
            title: 'Prove the Riemann Hypothesis',
            honesty: 'Imagination',
            honestyNote: 'Frontier AI can verify short formal lemmas, not crack open Millennium Prize proofs.',
            beatSummary: 'Kalpa publishes a proof overnight — then humans discover a million pages nobody alive can check.'
          },
          {
            title: 'Read the Indus script',
            honesty: 'Possible soon',
            honestyNote: 'Pattern-matching across short seal fragments is advancing quickly, though ground truth stays scarce.',
            beatSummary: 'Lost inscriptions light up cleanly — until competing readings force historians to ask what counts as proof.'
          }
        ]
      },
      {
        id: 'gadgets',
        title: 'Gadgets of Imagination',
        icon: 'pocket',
        lead: 'Impossible pockets, translators, and personal aides.',
        samples: ["Doraemon's pocket", 'Jarvis for my life'],
        moreCount: '+ Universal translator & Time-Turner',
        wishes: [
          {
            title: 'Jarvis for my life',
            honesty: 'Possible soon',
            honestyNote: 'Tool-using assistants already book, pay, and reply today, though reliable boundaries lag.',
            beatSummary: 'Your week runs like magic — until a quiet outage leaves you unable to remember your own passwords.'
          },
          {
            title: "Doraemon's pocket",
            honesty: 'Imagination',
            honestyNote: 'On-demand matter creation remains pure fiction; only digital fabrication hints at the edge.',
            beatSummary: 'Any tool appears on request — until local repair shops disappear and nobody knows how anything is fixed.'
          }
        ]
      },
      {
        id: 'epic',
        title: 'Epic Powers',
        icon: 'eye',
        lead: 'Ancient stories of sight, flight, healing, and shields.',
        samples: ['Sanjeevani (cure anything)', 'Pushpaka Vimana (flight for all)'],
        moreCount: '+ Divya drishti & Brahmastra protector',
        wishes: [
          {
            title: 'Sanjeevani — cure anything',
            honesty: 'Imagination → Possible soon for narrow diseases',
            honestyNote: 'Targeted drug discovery is advancing today; universal cures remain far out.',
            beatSummary: 'Wards empty at dawn — then hospital leaders realise every rule on care and funding assumed yesterday’s world.'
          },
          {
            title: 'Divya drishti — far-seeing sight',
            honesty: 'Possible soon',
            honestyNote: 'Global satellite and sensor streams can already track storms and infrastructure live.',
            beatSummary: 'Every storm is visible miles ahead — alongside the realisation that everyone can watch everyone else.'
          }
        ]
      },
      {
        id: 'movie',
        title: 'Live a Movie',
        icon: 'frame',
        lead: 'Worlds you can step inside, rewrite, or direct in seconds.',
        samples: ['Walk into a classic film', 'Every master as my mentor'],
        moreCount: '+ Rewrite any ending & direct from text',
        wishes: [
          {
            title: 'Walk into a classic film',
            honesty: 'Possible soon',
            honestyNote: 'Interactive 3D worlds are emerging fast, though believable long-form memory stays fragile.',
            beatSummary: 'You step onto a rainy street that answers back — and gradually notice fewer people hanging around real cafés.'
          },
          {
            title: 'Direct a film by describing it',
            honesty: 'Partly real today',
            honestyNote: 'Short generated scenes already work; coherent multi-hour cinema control does not yet.',
            beatSummary: 'A feature film renders over lunch — then audiences drown in endless custom cuts with no shared story left.'
          }
        ]
      },
      {
        id: 'world',
        title: 'Wishes for My World',
        icon: 'lamp',
        lead: 'Care, clean water, teachers, and shared memory where you live.',
        samples: ['Fix my river', 'A teacher for every child'],
        moreCount: '+ Revive a dying language & local clinics',
        wishes: [
          {
            title: 'Fix my river',
            honesty: 'Possible soon',
            honestyNote: 'Sensor monitoring helps spot leaks early; physical watershed restoration still takes human action.',
            beatSummary: 'Sensors pinpoint every runoff pipe — yet nothing changes until towns agree who sacrifices profit upstream.'
          },
          {
            title: 'A teacher for every child',
            honesty: 'Possible soon',
            honestyNote: 'Personal tutoring systems already help millions study; human mentorship and community remain irreplaceable.',
            beatSummary: 'Every child advances smoothly at home — until elders ask what happens when neighbours stop teaching each other.'
          }
        ]
      }
    ]
  },

  beats: {
    heading: 'Every wish has four moments',
    items: [
      { key: 'Wonder', desc: 'Your wish comes true.' },
      { key: 'Wobble', desc: 'Something small goes sideways.' },
      { key: 'Weight', desc: 'You spot what matters.' },
      { key: 'Way', desc: 'You see what humans can still do.' }
    ],
    footerLine: 'Every great wish needs a good wisher.'
  },

  lights: {
    heading: 'Your readiness, in five lights',
    items: [
      { key: 'Clarity', meaning: 'do you know what you want?' },
      { key: 'Foresight', meaning: 'did you think about side effects?' },
      { key: 'Fairness', meaning: 'did your wish include others?' },
      { key: 'Wisdom', meaning: 'what would you keep human?' },
      { key: 'Capability', meaning: 'could you actually use the gift?' }
    ],
    emptyState: 'Make your first wish to light your first light.',
    lowLightNote: "A dim light isn't failure. It's where to grow next.",
    trailNote: 'Finish 3 wishes to unlock your shareable Trail card (coming in the wish player).'
  },

  country: {
    heading: 'Can your country catch the gift?',
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
    heading: "This week in Kalpa's city",
    badge: 'PILOT EPISODE 1 · IN PRODUCTION',
    title: 'The First Wish',
    synopsis:
      'Dawn breaks over the harbour. Meera, working the night ward shift, makes the city’s very first wish. Every bed heals — and the corridor asks a question no machine settled beforehand: who goes first tomorrow?',
    voteNote: 'Interactive 3-minute story & live vote launch alongside Phase 4.',
    recapTitle: "Join Friday's recap",
    recapBody: 'We are listening to early visitors worldwide before picking our weekly digest format. No spam, ever.',
    recapStatus: 'Recap channel opens after subscriber preferences settle.'
  },

  wishWall: {
    heading: 'What the world is wishing for',
    themes: ['Health', 'Learning', 'Climate', 'Dignity', 'Wonder', 'Truth'],
    emptyHeadline: 'The global Wish Wall opens after the first 20 anonymous shared wishes.',
    emptyBody:
      'Every wish stays private in your browser by default. Crowd themes only appear once a threshold of at least 20 real people choose to contribute.',
    cta: 'Make a wish of your own'
  },

  wisher: {
    heading: 'Why a good wish still needs a good wisher',
    cards: [
      {
        title: 'Speed',
        body: "Machines can act thousands of times faster than we can blink. So we can't just watch. We need checks built in before the gift arrives.",
        techHint: 'Currently ~3,200× faster than line-by-line human review.'
      },
      {
        title: 'Dependence',
        body: "The more we hand over, the harder it is to pause. Hospitals, power, food all run on systems we can't just switch off. A small paper backup is worth a lot.",
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
        desc: 'Explore the 26 AI transition pathways linking behind every wish.',
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
    ]
  }
} as const;

export type LocaleKey = 'en' | 'rtl-stub';
