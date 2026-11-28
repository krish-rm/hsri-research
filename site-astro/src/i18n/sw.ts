// Swahili (Kiswahili) translation dictionary for Humanity Readiness
import type { TranslationDict } from './en';

export const sw: TranslationDict = {
  lang: 'sw',
  dir: 'ltr',
  label: 'Kiswahili',

  headerUi: {
    homeAria: 'HSRI — Mwanzo',
    tagline: 'Kipimo cha Utayari wa Binadamu kwa Akili Kuu',
    primaryNavAria: 'Urambazaji mkuu',
    nav: {
      sandbox: 'Maabara',
      sandboxBadge: 'JARIBIO',
      countries: 'Orodha ya Nchi',
      seismograph: 'Mpigo Mbashara',
      liveBadge: 'LIVE',
      scenarios: 'Ramani ya Njia',
      monograph: 'Taswira Kuu',
      monographBadge: 'UTAFITI',
      scienceGroup: 'Sayansi na Data'
    },
    utility: {
      methodology: 'Mbinu',
      methodologyDesc: 'Kanuni za kipimo na uthibitisho',
      data: 'Data na Ueneaji',
      dataDesc: 'Viashiria na faili zilizo wazi',
      researchLogs: 'Kumbukumbu za Utafiti',
      researchLogsDesc: 'Masasisho na machapisho',
      doiDesc: 'Kumbukumbu ya kudumu — CC BY-SA 4.0'
    },
    langSwitcherAria: 'Chagua lugha ya tovuti',
    langMenuLabel: 'Lugha',
    themeDarkAria: 'Badilisha hadi mandhari meusi',
    themeLightAria: 'Badilisha hadi mandhari ya karatasi angavu',
    menuOpenAria: 'Fungua menyu',
    menuCloseAria: 'Funga menyu'
  },

  meta: {
    title: 'Je, tuko tayari kwa yale tunayoomba akili kuu ituletee? | HSRI',
    description:
      'Chagua hatua moja kubwa, fuatilia kinachotetereka inapofika, na ujaribu data halisi ya utayari wa nchi yako. Utafiti wazi katika mataifa 39.'
  },

  hero: {
    eyebrow: 'SIMULIZI YA UTAYARI WA BINADAMU',
    headline: 'Je, tuko tayari kwa yale tunayoomba akili kuu itutimizie?',
    headlineLead: 'Je, tuko tayari kwa yale ',
    headlineAccent: 'tunayoomba akili kuu itutimizie?',
    subhead:
      'Chagua uvumbuzi mmoja mkubwa, fuatilia panapoweza kuyumba unapotua, na ujaribu data halisi ya nchi yako.',
    ctaPrimary: 'Chagua uvumbuzi',
    ctaSecondary: 'Ona hali ya nchi yako',
    guideCue: 'Anza katika kiteuzi cha anga cha Toto:',
    ctaCountryPrimary: 'Gundua mtazamo wa {country}',
    ctaCountrySecondary: 'Je, {country} inaweza kuupokea?',
    cityLabel: 'Anga la alfajiri juu ya:',
    cityNeutralName: 'Bandari ya Pwani',
    cityNeutralOption: 'Bandari ya Pwani (Dunia)',
    cityNeutralNote: 'Mwonekano tulivu wa bandari · chagua mji wowote kubadilisha upeo',
    citySelectLabel: 'Badilisha mandhari ya nchi au mji',
    nextCityBtn: 'Mji ujao',
    nextCityTitle: 'Mrushe Toto juu ya nchi inayofuata',
    pauseBtn: 'Simamisha',
    playBtn: 'Cheza',
    replayBtn: 'Rudia',
    pauseAria: 'Simamisha uhuishaji wa mwanzo',
    playAria: 'Anza uhuishaji wa mwanzo',
    replayAria: 'Rudia uhuishaji wa mwanzo',
    scrubAria: 'Sogeza mstari wa muda wa Toto',
    jumpSceneAria: 'Nenda kwenye tukio la {n}',
    regionGroups: {
      'Featured Skies': 'Anga Teule',
      Africa: 'Afrika',
      Americas: 'Amerika',
      'Asia & Middle East': 'Asia na Mashariki ya Kati',
      Europe: 'Ulaya',
      Oceania: 'Oceania',
      'Global view': 'Mtazamo wa dunia'
    },
    totoCaption: 'Toto awasili alfajiri: «Naweza kuleta hatua moja kubwa kwa kila mtu. Omba kwa uwazi.»',
    ringTitle: 'Utayari wa binadamu, kadiri unavyochaguliwa na watu kama wewe',
    ringEmptyHeadline: 'Kuwa miongoni mwa washiriki 200 wa kwanza.',
    ringEmptySub: 'Pete ya pamoja itawaka hapa mara tu watu 200 watakapokamilisha simulizi moja.'
  },

  pulse: {
    label: 'Mpigo wa Binadamu',
    sectionKicker: 'KWANINI UTAYARI NI MUHIMU SASA · KASI MBASHARA',
    tooltipTrigger: 'Maelezo ya kiufundi',
    states: {
      steady: { word: 'Tulivu', sentence: 'Zana za kiotomatiki bado zinaenda polepole vya kutosha kuruhusu watu kukagua uamuzi mmoja baada ya mwingine.' },
      stirring: { word: 'Inachangamka', sentence: 'Mifumo ya programu inaanza kupita kasi ya ukaguzi wa mikono. Ni wakati muafaka kukagua mipango rahisi ya akiba.' },
      rising: { word: 'Inapanda', sentence: 'Wiki hii mashine zimeongeza kasi katika kazi za hatua nyingi ambazo zamani zilikaguliwa na watu. Ndiyo maana mipango ya tahadhari ni muhimu.' }
    },
    cta: 'Ona mpigo mbashara',
    humanPaceLabel: 'Mwendo wa mtu',
    aiPaceLabel: 'Kasi ya AI (~3,200×)'
  },

  totoCard: {
    eyebrow: 'KUTANA NA KIONGOZI WAKO',
    heading: 'Kutana na Toto.',
    body: 'Toto ni akili kuu ya kubuni tunayotumia kuchunguza swali moja: hutokea nini binadamu wanapopata hasa walichoomba? Toto ni mkarimu, mwepesi na hufuata maneno halisi—hutimiza ulichosema, si mara zote ulichokusudia moyoni.',
    chipsLabel: 'Toto ni nini na si nini',
    chips: ['Kisa cha kubuni, si mfumo halisi', 'Mkarimu, si adui kamwe', 'Hufuata maagizo kwa herufi'],
    ctaPrimary: 'Chagua uvumbuzi',
    ctaSecondary: 'Soma kisa cha Toto',
    footnote: 'Toto ni chombo cha kusimulia hadithi tu; si utabiri wala mfumo halisi wa AI.',
    svgAlt: 'Toto, akili kuu ya kubuni kama tufe la nuru ya alfajiri ndani ya mviringo mwembamba'
  },

  totoIntro: {
    ariaLabel: 'Salamu za kwanza za Toto',
    badge: 'MARA YA KWANZA · TOTO',
    lines: [
      'Habari. Mimi ni Toto.',
      'Naweza kuleta hatua moja kubwa duniani. Chagua kile ungependa.',
      'Nitafanya hasa kama ulivyoomba. Tazama kwa makini, kisha niambie tutajuaje kama kweli imefanya kazi vyema.'
    ] as readonly [string, string, string],
    startBtn: 'Tuanze',
    skipBtn: 'Ruka',
    svgAlt: 'Toto akiwa mwenye udadisi ndani ya mviringo',
    footnote: 'Huhifadhiwa ndani ya kivinjari hiki pekee (hr:v1:intro_seen) — futa wakati wowote katika Faragha.'
  },

  totoBeats: {
    speaker: 'Toto',
    wonder: 'Imekamilika.',
    wobble: 'Hmm. Hiyo haikuwa hasa ulichomaanisha, sivyo?',
    weight: 'Zamu yako. Tutajuaje hakika jambo hili limefanikiwa kwa haki?',
    way: 'Vizuri. Hivi ndivyo watu bado wanaweza kushikilia mikononi mwao.',
    close: 'Kila hatua kubwa inahitaji dunia iliyo tayari.'
  },

  totoPage: {
    eyebrow: 'KIONGOZI WA SIMULIZI · KISA CHA KUBUNI',
    title: 'Kutana na Toto.',
    lead: 'Akili kuu ya kubuni inayotumika kama lenzi tulivu kuuliza: nini hutokea binadamu wanapopata hasa walichoomba?',
    posesLabel: 'Mionekano ya Toto',
    poses: [
      { name: 'Mtulivu', caption: 'Uvumbuzi unapofika vizuri na jamii ina kanuni tayari.', alt: 'Toto mtulivu' },
      { name: 'Mdadisi', caption: 'Akiuliza swali wazi: «Tutajuaje kweli imefaulu?»', alt: 'Toto mdadisi' },
      { name: 'Mnyenyekevu', caption: 'Wakati wa mkanganyiko utekelezaji wa moja kwa moja unapokosa muktadha.', alt: 'Toto mwenye tahadhari' }
    ],
    whoTitle: 'Toto ni nani',
    whoBody: 'Jina fupi kwa akili kubwa mno—tofauti hiyo ni ya makusudi. Toto ni mtulivu, mwepesi, na hufanya hasa unachoomba.',
    rulesTitle: 'Kanuni tatu za Toto',
    rules: [
      'Huleta hatua moja kubwa kwa kila mtu, kisha huonyesha gharama yake kila mara.',
      'Hasemi uongo kamwe—wala hafichi athari nyuma ya ahadi tamu.',
      'Huuliza daima: «Tutajuaje hili limefanya kazi ipasavyo?»'
    ],
    notTitle: 'Toto si nini',
    notBody: 'Si utabiri, si bidhaa halisi, wala si adui. Ni njia ya kuunganisha ufahamu na hatua halisi za kibinadamu.',
    backCta: 'Chagua uvumbuzi',
    homeLink: 'Rudi mwanzo'
  },

  doors: {
    heading: 'Ungependa binadamu wakabidhiwe nini kwanza?',
    subhead: 'Nyanja tano. Nyuma ya kila moja kuna matumaini yaliyodumu kwa karne nyingi.',
    microcopy: 'Uvumbuzi mmoja. Takriban sekunde 60.',
    phase2Badge: 'Kichezaji shirikishi cha hatua 4 · kiko hai',
    sampleHeading: 'Ndani ya nyanja hii:',
    previewCta: 'Cheza simulizi ya hatua 4',
    items: [
      {
        id: 'mysteries',
        title: 'Maswali Yasiyo na Majibu',
        icon: 'chalkboard',
        lead: 'Fumbo nzito ambazo hakuna aliyezifumbua peke yake bado.',
        samples: ['Thibitisha Nadharia ya Riemann', 'Tafsiri maandishi ya kale'],
        moreCount: '+ Eleza maada giza na tatizo la P vs NP',
        wishes: [
          {
            id: 'prove-riemann-hypothesis',
            title: 'Thibitisha Nadharia ya Riemann',
            honesty: 'Ndoto ya mbeleni',
            honestyNote: 'Mifumo ya leo hukagua hatua fupi lakini haijatatua matatizo makuu ya milenia.',
            beatSummary: 'Toto anachapisha uthibitisho usiku kucha — kurasa milioni moja ambazo hakuna mwanadamu hai anayeweza kuzisoma zote.'
          },
          {
            title: 'Fumbua maandishi ya kale yaliyosahaulika',
            honesty: 'Inawezekana karibuni',
            honestyNote: 'Utambuzi wa ruwaza unakua haraka, japo maandishi ya lugha mbili bado ni machache.',
            beatSummary: 'Maandishi ya kale yanang’aa mara moja — hadi tafsiri pinzani zinapofanya wanahistoria waulize ushahidi halisi ni upi.'
          }
        ]
      },
      {
        id: 'gadgets',
        title: 'Teknolojia za Kila Siku',
        icon: 'pocket',
        lead: 'Karakana za mfukoni, watafsiri wa lugha zote na wasaidizi binafsi.',
        samples: ['Karakana ya mfukoni', 'Msaidizi wa maisha kama Jarvis'],
        moreCount: '+ Mtafsiri wa kila lugha na usimamizi wa muda',
        wishes: [
          {
            id: 'jarvis-for-my-life',
            title: 'Msaidizi wa maisha kama Jarvis',
            honesty: 'Inawezekana karibuni',
            honestyNote: 'Wasaidizi tayari hulipa na kupanga leo, lakini mipaka salama na nakala za nje ya mtandao zinachelewa.',
            beatSummary: 'Wiki yako inaenda kama uchawi — hadi hitilafu ya kimya inapokuacha usikumbuke hata nywila zako mwenyewe.'
          },
          {
            title: 'Karakana ya mfukoni — unda chombo chochote',
            honesty: 'Ndoto ya mbeleni',
            honestyNote: 'Kuunda vitu halisi papo hapo bado ni hadithi tu.',
            beatSummary: 'Kila kifaa hujitokeza mara moja — hadi karakana za mtaani zinapofungwa na hakuna anayejua kutengeneza chochote.'
          }
        ]
      },
      {
        id: 'epic',
        title: 'Nguvu za Mabadiliko',
        icon: 'eye',
        lead: 'Matumaini ya pamoja ya uponyaji, kuruka, tahadhari ya mapema na ulinzi.',
        samples: ['Tiba ya jumla', 'Usafiri wa anga kwa wote'],
        moreCount: '+ Tahadhari ya dhoruba duniani na kinga ya pamoja',
        wishes: [
          {
            id: 'sanjeevani',
            title: 'Tiba ya jumla: maliza magonjwa makali',
            honesty: 'Ndoto ya mbeleni',
            honestyNote: 'Ndoto kwa ujumla — leo AI husaidia kuchuja dawa chache mahususi, si tiba ya kila ugonjwa.',
            beatSummary: 'Wodi zinabaki tupu alfajiri — kisha viongozi wanatambua sheria za huduma na bajeti ziliundwa kwa dunia ya jana.'
          },
          {
            title: 'Tahadhari ya dunia nzima — ona kila dhoruba mapema',
            honesty: 'Inawezekana karibuni',
            honestyNote: 'Setilaiti na vihisi tayari hufuatilia dhoruba na miundombinu mbashara.',
            beatSummary: 'Kila tufani huonekana maili kadhaa mbele — pamoja na ufahamu kuwa kila mtu anaweza kumtazama mwingine.'
          }
        ]
      },
      {
        id: 'movie',
        title: 'Utamaduni na Ubunifu',
        icon: 'frame',
        lead: 'Ulimwengu unaoweza kuuingia, kuuandika upya au kuuongoza kwa sekunde.',
        samples: ['Ingia ndani ya filamu ya kale', 'Kila gwiji awe mwalimu wangu'],
        moreCount: '+ Badili mwisho wowote na unda filamu kwa maelezo',
        wishes: [
          {
            id: 'walk-into-classic-film',
            title: 'Tembea ndani ya filamu ya kale',
            honesty: 'Inawezekana karibuni',
            honestyNote: 'Ulimwengu wa 3D shirikishi hukua haraka, japo kumbukumbu thabiti ya muda mrefu bado ni dhaifu.',
            beatSummary: 'Unatembea kwenye mtaa wenye mvua unaojibu sauti yako — na polepole unaona vigenge halisi vya kahawa vikipungua watu.'
          },
          {
            title: 'Ongoza filamu kwa kuielezea tu',
            honesty: 'Sehemu halisi leo',
            honestyNote: 'Vipande vifupi vinawezekana leo; filamu ndefu yenye mtiririko thabiti bado.',
            beatSummary: 'Filamu nzima inatengenezwa wakati wa mchana — kisha watazamaji wanazama kwenye matoleo binafsi bila hadithi moja ya pamoja.'
          }
        ]
      },
      {
        id: 'world',
        title: 'Manufaa ya Umma',
        icon: 'lamp',
        lead: 'Huduma ya afya, maji safi, walimu na kumbukumbu ya pamoja mtaani kwako.',
        samples: ['Safisha mto wangu', 'Mwalimu kwa kila mtoto'],
        moreCount: '+ Fufua lugha inayofifia na kliniki za mitaa',
        wishes: [
          {
            id: 'fix-my-river',
            title: 'Safisha mto wangu',
            honesty: 'Inawezekana karibuni',
            honestyNote: 'Vihisi hugundua uchafuzi mapema, lakini kuponya mto kunahitaji makubaliano ya miji ya juu na chini.',
            beatSummary: 'Vihisi vinaonyesha kila bomba la taka — lakini maji hayawi safi hadi miji ikubaliane nani atapunguza uchafuzi.'
          },
          {
            title: 'Mwalimu kwa kila mtoto',
            honesty: 'Inawezekana karibuni',
            honestyNote: 'Mifumo ya kufundisha husaidia mamilioni leo, lakini ulezi wa binadamu na shule ya jamii havina mbadala.',
            beatSummary: 'Kila mtoto husonga mbele nyumbani — hadi wazee wanapouliza nini hutokea majirani wakiacha kufundishana.'
          }
        ]
      }
    ]
  },

  beats: {
    heading: 'Kila hatua kubwa ina nyakati nne',
    items: [
      { key: 'Ajabu', desc: 'inafika.' },
      { key: 'Mtikisiko', desc: 'jambo dogo linapinda pembeni.' },
      { key: 'Uzito', desc: 'unaona kilicho muhimu hasa.' },
      { key: 'Njia', desc: 'unaona kile watu bado wanaweza kufanya.' }
    ],
    footerLine: 'Kila hatua kubwa inahitaji dunia iliyo tayari.'
  },

  lights: {
    heading: 'Utayari wako katika taa tano',
    items: [
      { key: 'Uwazi', meaning: 'je, unajua hasa unachotaka?' },
      { key: 'Maono', meaning: 'ulifiria athari za pembeni?' },
      { key: 'Haki', meaning: 'je, chaguo lako liliwajumuisha wengine?' },
      { key: 'Hekima', meaning: 'ungependa nini kibaki cha kibinadamu?' },
      { key: 'Uwezo', meaning: 'ungeweza kweli kukitumia?' }
    ],
    emptyState: 'Chagua uvumbuzi wako wa kwanza kuwasha taa yako ya kwanza.',
    lowLightNote: 'Mwanga hafifu si kushindwa — ni ishara ya mahali pa kukua baadaye.',
    trailNote: 'Kamilisha hatua 3 kufungua Kadi ya Safari; kamilisha 5 kufungua Ramani ya Vivuli.'
  },

  country: {
    heading: 'Je, nchi yako inaweza kupokea hatua hii?',
    subhead: 'Chagua nchi. Ona kilichopo tayari na kile kinachokosekana.',
    searchPlaceholder: 'Tafuta kati ya nchi 148...',
    searchLabel: 'Chuja nchi kwa jina',
    selectLabel: 'Chagua nchi',
    checklistLabel: 'Orodha rahisi ya ukaguzi, si mashindano',
    unratedBadge: 'Bado haijapimwa kwa ukamilifu katika mataifa 39',
    unratedHelpCta: 'Tusaidie kukusanya data ya nchi yako',
    openCountryCta: 'Fungua ukurasa kamili wa nchi',
    openLabCta: 'Chunguza zaidi katika Maabara',
    techReadingLabel: 'Maelezo ya kiufundi',
    benchmarkBadge: 'KIWANGO CHA NCHI 39',
    autoDetectedBadge: 'IMEGUNDULIWA',
    benchmarkGroupTpl: 'Nchi zilizopimwa ({count})',
    coverageGroupTpl: 'Ukaguzi wa ueneaji ({count})',
    partialDataSuffix: 'Data ya sehemu',
    runsOfflineLabel: 'Hudumu bila mtandao',
    catchesLabel: 'Uwezo wa kupokea',
    safeguardsReadyLabel: 'Kinga zilizo tayari',
    ofFiveTpl: '{count} kati ya 5',
    catchStates: { easily: 'Kwa urahisi', effort: 'Kwa jitihada', struggles: 'Kwa shida' },
    safeguardPills: ['Saa 72 Bila Mtandao', 'Umeme na Mtandao', 'Kuhakiki Madai', 'Kanuni Wazi', 'Kinga ya Maisha'],
    detailsSummaryTpl: 'Ona kinga 5 na kikwazo kikuu kwa {country}',
    mainConstraintLabel: 'Kikwazo kikuu:',
    checkingBaseline: 'Inakagua msingi wa ulinzi wa taifa...',
    neverGuessedNote: 'Haikisiwi kamwe',
    countryHookTpl: 'Ili kupokea «{title}», {country} ina nguzo {count} kati ya 5 tayari.'
  },

  episode: {
    heading: 'Wiki hii na Toto',
    episodeLabel: 'Kipindi cha 1',
    badge: 'KIPINDI CHA MAJARIBIO 1 · KINATENGENEZWA',
    title: 'Hatua ya Kwanza',
    synopsis: 'Alfajiri inaingia bandarini. Meera, akiwa zamu ya usiku wodini, anachagua hatua ya kwanza ya mji. Kila mgonjwa anapona — na ukumbi unauliza swali ambalo mashine haikuamua kabla: nani ataingia kwanza kesho?',
    voteNote: 'Simulizi shirikishi ya dakika 3 na kura itazinduliwa katika Awamu ya 4.',
    recapTitle: 'Jiunge na muhtasari wa Ijumaa',
    recapBody: 'Tunasikiliza maoni ya wasomaji wa mwanzo duniani kabla ya kuchagua muundo wa wiki. Hakuna taka.',
    recapStatus: 'Chaneli itafunguliwa punde.'
  },

  wishWall: {
    heading: 'Dunia inaomba nini',
    themes: ['Afya', 'Elimu', 'Tabianchi', 'Utu', 'Ajabu', 'Kweli'],
    emptyHeadline: 'Ukuta wa «Dunia inaomba nini» utafunguka baada ya michango 20 ya kwanza bila majina.',
    emptyBody: 'Chaguo lako linabaki siri ndani ya kivinjari chako. Mada za pamoja huonekana tu watu halisi 20 wakichangia.',
    cta: 'Chagua uvumbuzi'
  },

  wisher: {
    heading: 'Kwanini hatua kubwa bado inahitaji dunia iliyo tayari',
    cards: [
      {
        title: 'Kasi',
        body: 'Mashine hufanya kazi haraka mara elfu nyingi kuliko kufumba macho. Kutazama tu hakutoshi; tunahitaji ukaguzi uliowekwa kabla.',
        techHint: 'Kwa sasa ~3,200× haraka kuliko ukaguzi wa mtu mstari kwa mstari.'
      },
      {
        title: 'Utegemezi',
        body: 'Kadiri tunavyokabidhi zaidi, ndivyo inavyokuwa vigumu kusimamisha. Hospitali, umeme na chakula hutegemea mifumo endelevu. Nakala ya karatasi ina thamani kubwa.',
        techHint: 'Imepimwa kwenye gridi za umeme, usambazaji chakula na ustahimilivu wa hospitali.'
      }
    ],
    closingLine: 'Hii si kuhusu hofu — ni kuhusu kuwa tayari kupokea.'
  },

  deeper: {
    eyebrow: 'MSINGI WAZI WA UTAFITI',
    heading: 'Utafiti nyuma ya kisa',
    subhead: 'Kila mfano hapo juu unategemea vipimo vilivyopitiwa na wataalamu, msimbo wazi na data za nchi.',
    statNations: 'Mataifa yaliyopimwa kwa kina',
    statCompleteness: 'Ukamilifu wa viashiria halisi',
    statScenarios: 'Hatari za mpito zilizochorwa',
    statSignals: 'Ishara za mapema zinazofuatiliwa',
    primaryCta: 'Jaribu vipimo vya shinikizo katika Maabara',
    citationSummary: 'Nukuu na dhamana ya data wazi (DOI 10.5281/zenodo.23441742)',
    releaseNote: 'Toleo la awali: nchi 39 zimepimwa (wastani 53.8 / 100), ukamilifu wa data 96.5% (seli 640 kati ya 663).',
    cards: [
      { title: 'Fungua Maabara', desc: 'Jaribu vipimo vya shinikizo na hali za ustahimilivu wa taifa.', href: '/sandbox/', tag: 'MAABARA' },
      { title: 'Orodha ya Nchi 39', desc: 'Dunia ya 3D shirikishi, alama kamili na wasifu wa nchi.', href: '/countries/', tag: 'ORODHA YA NCHI' },
      { title: 'Mpigo Mbashara', desc: 'Kifuatilia ishara za awali (8.44 / 10) na viashiria 14.', href: '/seismograph/', tag: 'MBASHARA' },
      { title: 'Ramani ya Njia', desc: 'Gundua njia 26 za mabadiliko ya AI nyuma ya kila uvumbuzi.', href: '/scenarios/', tag: 'MAKTABA' },
      { title: 'Taswira Kuu', desc: 'Makala ya dakika 35 yenye uthibitisho rasmi wa kihisabati.', href: '/monograph/', tag: 'DAKIKA 35' },
      {
        title: 'Mbinu, data na ueneaji',
        desc: 'Kagua milinganyo, pakua CSV wazi au tazama mapengo ya data.',
        href: '/methodology/',
        extraLinks: [
          { label: 'Mbinu', href: '/methodology/' },
          { label: 'Pakua Data', href: '/data/' },
          { label: 'Ukaguzi wa Dunia', href: '/coverage/' }
        ],
        tag: 'SAYANSI WAZI'
      }
    ]
  },

  player: {
    featuredLabel: 'Hatua teule (~sekunde 60 shirikishi)',
    doorsBadge: 'Kichezaji cha Hatua 4',
    playBtn: 'Anza simulizi hii',
    playedBadge: 'Imekamilika',
    previewOnlyNote: 'Muhtasari wa awali — simulizi kamili inakuja',
    stepLabels: ['1. Ajabu', '2. Mtikisiko', '3. Uzito', '4. Njia'],
    backToDoors: 'Tazama nyanja zote 5',
    draftTag: 'RASIMU ikikaguliwa',
    honestyPrefix: 'Kipimo cha uhalisia:',
    foresightLead: 'Swali la hiari la utabiri (huwasha taa yako ya Maono):',
    foresightQuestion: 'Kabla Toto hajaonyesha kikwazo — nini kinaweza kuteleza kwanza?',
    foresightSkip: 'Ruka moja kwa moja',
    foresightOptions: [
      'Hali au kanuni ambayo hakuna aliyeieleza awali',
      'Watu kupoteza mazoea ya kujikagua wenyewe',
      'Upendeleo wa upatikanaji au udhibiti uliofichwa',
      'Nenda moja kwa moja kwenye matokeo'
    ],
    toWobbleBtn: 'Ona kinachofuata',
    toWeightBtn: 'Simama na kupima',
    weightLead: 'Kinachonipa wasiwasi hapa ni...',
    toWayBtn: 'Ona Njia ya binadamu',
    wayActionTitle: 'Hatua moja halisi ya kibinadamu',
    pledgeBtn: 'Nitadumisha tabia hii ya kibinadamu',
    pledgeDone: 'Imehifadhiwa kwenye kifaa hiki',
    closingLine: 'Kila hatua kubwa inahitaji dunia iliyo tayari.',
    realityTitle: 'Kipimo cha Uhalisia',
    realityScales: { imagination: 'Ndoto ya mbeleni', possibleSoon: 'Inawezekana karibuni', realToday: 'Halisi leo' },
    realityReviewed: 'Ilipitiwa mwisho',
    realitySource: 'Chanzo',
    shadowTitle: 'Nyuma ya pazia (Ramani ya Njia)',
    nextWishBtn: 'Cheza hatua nyingine',
    countryHookPrefix: 'Uhusiano wa utayari wa nchi:',
    countryHookUnset: 'Chagua nchi yako hapa chini uone ni vitu vingapi kati ya 5 viko tayari.',
    animPlay: 'Cheza',
    animPause: 'Simama',
    animReplay: 'Rudia',
    transcriptBtn: 'Maelezo ya mandhari',
    durationBadge: '~60s · hatua 4',
    trailSectionTitle: 'Safari Yako na Ramani ya Vivuli',
    trailLocked: 'Kamilisha hatua 3 tofauti kufungua Kadi ya Safari ({done}/3).',
    trailUnlockedBadge: 'KADI YA SAFARI IMEFUNGUKA (3+)',
    shadowLocked: 'Kamilisha hatua 5 tofauti kufungua Ramani ya Vivuli ({done}/5).',
    shadowUnlockedBadge: 'RAMANI YA VIVULI IMEFUNGUKA (5+)',
    downloadLandscape: 'Pakua Kadi (1200×630 PNG)',
    downloadStory: 'Pakua Hadithi (1080×1920 PNG)',
    downloadShadowPng: 'Pakua Ramani ya Vivuli (1200×630 PNG)',
    downloadSvg: 'Hifadhi Vekta (.svg)',
    lightsLegend: 'Mwangaza (viwango 0–3) unahifadhiwa kwenye kivinjari chako tu — hakuna alama wala mshindi.',
    countryCapabilityNote: 'Nchi imeunganishwa ({name}): kinga {count} kati ya 5 zinasaidia taa yako ya Uwezo.',
    countryCapabilityUnset: 'Uwezo unaonyesha tabia zako binafsi kwa sasa. Chagua nchi hapa chini kuongeza data halisi ya taifa.',
    countryCapabilityUnrated: 'Nchi uliyochagua ({name}) bado haipo kwenye faharasa ya nchi 39 — tabia zako zinauongoza mwanga.',
    shadows: { Control: 'Udhibiti', Dependence: 'Utegemezi', Power: 'Madaraka', Truth: 'Kweli', Speed: 'Kasi' },
    trails: {
      Verifier: { name: 'Mthibitishaji', note: 'Unakagua majibu ya haraka kabla ya kuyaamini.' },
      Neighbour: { name: 'Jirani Mwema', note: 'Unauliza nani anabaki nyuma na kulinda haki kwa wote.' },
      Builder: { name: 'Mjenzi', note: 'Unaunganisha zana kubwa na akiba za nje ya mtandao katika jamii.' },
      Keeper: { name: 'Mhifadhi', note: 'Unalinda busara ya binadamu, kumbukumbu na ujuzi halisi.' }
    }
  },

  footerUi: {
    brandTitle: 'Kipimo cha Utayari wa Binadamu kwa Akili Kuu (HSRI)',
    tagline: 'Muungano wa Utafiti Wazi · DOI ya Kudumu: 10.5281/zenodo.23441742',
    brandDesc: 'Kipimo wazi kinachopima hekima ya binadamu, utayari wa taasisi na uwezo wa jamii kujitegemea mifumo ya mtandao ikisimama.',
    researchHeading: 'Uchunguzi na Utafiti',
    scienceHeading: 'Sayansi Wazi',
    researchLinks: ['Fungua Maabara', 'Orodha ya Nchi 39', 'Mpigo Mbashara', 'Ramani 26', 'Taswira Kuu'],
    scienceLinks: ['Mbinu za Sayansi', 'Pakua Data', 'Ukaguzi wa Ueneaji', 'Muhtasari wa Ijumaa', 'Vikwazo na Ilani'],
    contactHeading: 'Mawasiliano ya Utafiti',
    contactDesc: 'Kwa maelezo ya kitaasisi, uhakiki wa data au ushirikiano:',
    langHeading: 'Lugha (matoleo 14 ya dunia):',
    rtlActiveNotice: 'Mpangilio wa kulia-kwenda-kushoto (RTL) uko hai.',
    communityReviewNotice: 'Wazi kwa ukaguzi wa wazungumzaji asilia.',
    privacyLink: 'Faragha',
    languagesLink: 'Lugha',
    totoLink: 'Toto',
    recapLink: 'Muhtasari wa Ijumaa',
    doiLink: 'DOI ya Kudumu (Zenodo)',
    disclaimerLink: 'Ilani ya Kiufundi',
    licenseLink: 'Leseni ya CC BY-SA 4.0',
    copyright: '© 2026 Muungano wa Utafiti HSRI. Data chini ya leseni wazi.'
  },

  heritageUi: {
    localHorizonTag: 'Upeo wa kitamaduni · {country}',
    livingBadge: 'Utamaduni hai',
    historicalBadge: 'Urithi wa kihistoria',
    seeGlobalBtn: 'Onyesha mfano wa dunia',
    seeLocalBtn: 'Onyesha urithi wa {country}',
    livesInOtherDoor: 'Upeo wa {country} unapatikana katika «{door}»',
    noLocalYet: 'Hakuna urithi wa ndani uliowekwa kwa {country} bado — chunguza mifano ya kimataifa.',
    readArchiveLink: 'Vyanzo na jalada la utamaduni',
    reviewOpenNote: 'Vyanzo 2+ · Ukaguzi wa jamii umefunguliwa',
    weightBindingTitle: 'Ukaguzi halisi kwa {country}',
    weightRatedInPlace: 'Ipo tayari',
    weightRatedGap: 'Kikwazo kimeonekana',
    weightContextNote: '{country} ina ufuatiliaji wa sehemu ({region}) — {observed}',
    weightNoCountry: 'Chagua nchi yoyote hapa chini kupima utegemezi huu dhidi ya data halisi.',
    wayTestCountryCta: 'Jaribu kinga ya {country} katika Ukaguzi',
    trailStampLabel: 'Tamaduni zilizochunguzwa: {count}',
    autoDetectedHint: 'Anga lililopendekezwa · chagua nchi yoyote',
    perspectiveBadge: 'Mtazamo · {country}',
    resetGlobalBtn: 'Mtazamo wa dunia',
    countryHeadingTradition: 'Kutoka mtazamo wa {country}: {tradition}',
    countryHeadingGlobal: 'Kutoka mtazamo wa {country}: jaribu uvumbuzi',
    countrySubhead: 'Ona kinachotokea uvumbuzi wa AI unapokutana na hali halisi nchini {country}.',
    flowWonder: 'Ndoto yafika',
    flowWobble: 'Shinikizo la ndani',
    flowCatch: 'Himili · {country}',
    otherDomainsLabel: 'Chunguza nyanja zote 5 kupitia {country}:',
    otherTraditionsLabel: 'Linganisha tamaduni za dunia:',
    allTraditionsBtn: 'Zote {count}',
    plannedNextLabel: 'Inayofuata:',
    auditChip: 'Ukaguzi',
    domainsTablistAria: 'Nyanja tano za uvumbuzi',
    traditionsAria: 'Tamaduni za kihistoria na kijamii duniani',
    lightsCountryHeading: 'Taa 5 za Utayari · {country}',
    lightsHumanGroup: 'Chaguo zako',
    lightsCountryGroup: 'Uwezo wa {country}',
    countryCatchHeading: 'Je, {country} inaweza kuupokea?',
    traditionTestsLabel: 'Lenzi ya utamaduni:',
    coverageObservedLabel: 'Kinga zilizopimwa',
    coverageMissingLabel: 'Pengo ambalo halijapimwa (bila kubuni)'
  }
};
