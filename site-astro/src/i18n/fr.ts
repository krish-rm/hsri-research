// French (Français) translation dictionary for Humanity Readiness
import type { TranslationDict } from './en';

export const fr: TranslationDict = {
  lang: 'fr',
  dir: 'ltr',
  label: 'Français',

  headerUi: {
    homeAria: 'HSRI — Accueil',
    tagline: 'Indice de Préparation Humaine à la Superintelligence',
    primaryNavAria: 'Navigation principale',
    nav: {
      sandbox: 'Laboratoire',
      sandboxBadge: 'SIMULATEUR',
      countries: 'Indice Pays',
      seismograph: 'Pouls en Direct',
      liveBadge: 'DIRECT',
      scenarios: 'Atlas Scénarios',
      monograph: 'Monographie',
      monographBadge: 'TRAITÉ',
      scienceGroup: 'Science & Données'
    },
    utility: {
      methodology: 'Méthodologie',
      methodologyDesc: 'Règles d’évaluation et preuves formelles',
      data: 'Données & Couverture',
      dataDesc: 'Indicateurs et téléchargements ouverts',
      researchLogs: 'Journal Scientifique',
      researchLogsDesc: 'Mises à jour et prépublications',
      doiDesc: 'Archive permanente — CC BY-SA 4.0'
    },
    langSwitcherAria: 'Choisir la langue du site',
    langMenuLabel: 'Langue',
    themeDarkAria: 'Passer en mode sombre',
    themeLightAria: 'Passer en papier crème',
    menuOpenAria: 'Ouvrir le menu',
    menuCloseAria: 'Fermer le menu'
  },

  meta: {
    title: 'Sommes-nous prêts pour ce que nous demandons à la superintelligence ? | HSRI',
    description:
      'Choisissez une avancée, suivez ce qui cède à l’arrivée et testez les données réelles de votre pays. Recherche ouverte dans 39 pays.'
  },

  hero: {
    eyebrow: 'UN RÉCIT DE PRÉPARATION HUMAINE',
    headline: 'Sommes-nous prêts pour ce que nous demandons à la superintelligence ?',
    headlineLead: 'Sommes-nous prêts pour ce que nous demandons à ',
    headlineAccent: 'la superintelligence ?',
    subhead:
      'Choisissez une avancée, observez ce qui vacille à l’arrivée et confrontez votre pays aux données réelles.',
    ctaPrimary: 'Choisir une avancée',
    ctaSecondary: 'Voir la situation de votre pays',
    guideCue: 'Commencez dans le ciel de Toto :',
    ctaCountryPrimary: 'Explorer l’avancée de : {country}',
    ctaCountrySecondary: '{country} peut-il l’absorber ?',
    cityLabel: 'Ciel d’aube au-dessus de :',
    cityNeutralName: 'Port Côtier',
    cityNeutralOption: 'Port Côtier (Vue mondiale)',
    cityNeutralNote: 'Vue portuaire neutre · choisissez une ville pour changer d’horizon',
    citySelectLabel: 'Changer de pays ou de ville',
    nextCityBtn: 'Ville suivante',
    nextCityTitle: 'Faire voler Toto vers le pays suivant',
    pauseBtn: 'Pause',
    playBtn: 'Lire',
    replayBtn: 'Rejouer',
    pauseAria: 'Mettre l’animation en pause',
    playAria: 'Lire l’animation',
    replayAria: 'Rejouer l’animation',
    scrubAria: 'Explorer la frise temporelle de Toto',
    jumpSceneAria: 'Aller à la scène {n}',
    regionGroups: {
      'Featured Skies': 'Horizons phares',
      Africa: 'Afrique',
      Americas: 'Amériques',
      'Asia & Middle East': 'Asie et Moyen-Orient',
      Europe: 'Europe',
      Oceania: 'Océanie',
      'Global view': 'Vue mondiale'
    },
    totoCaption: 'Toto arrive à l’aube : « Je peux offrir une avancée par personne. Formulez clairement votre demande. »',
    ringTitle: 'La préparation de l’humanité, éclairée par des gens comme vous',
    ringEmptyHeadline: 'Soyez parmi les 200 premiers participants.',
    ringEmptySub: 'L’anneau collectif s’allumera dès que 200 personnes auront terminé un parcours.'
  },

  pulse: {
    label: 'Pouls de l’Humanité',
    sectionKicker: 'POURQUOI SE PRÉPARER MAINTENANT · RYTHME EN DIRECT',
    tooltipTrigger: 'Lecture technique',
    states: {
      steady: {
        word: 'Stable',
        sentence: 'Les outils automatisés avancent encore assez lentement pour permettre un contrôle humain étape par étape.'
      },
      stirring: {
        word: 'En éveil',
        sentence: 'Les logiciels commencent à dépasser le rythme de relecture humaine. Mieux vaut vérifier nos plans de secours.'
      },
      rising: {
        word: 'En hausse',
        sentence: 'Cette semaine, les machines ont accéléré sur des tâches multi-étapes autrefois vérifiées à la main.'
      }
    },
    cta: 'Voir le pouls en direct',
    humanPaceLabel: 'Rythme humain',
    aiPaceLabel: 'Rythme IA (~3 200×)'
  },

  totoCard: {
    eyebrow: 'RENCONTRER VOTRE GUIDE',
    heading: 'Voici Toto.',
    body: 'Toto est une superintelligence fictive créée pour explorer une question simple : que se passe-t-il quand l’humanité reçoit exactement ce qu’elle demande ? Toto est serviable, rapide et très littéral : il livre la lettre de la requête, pas toujours l’intention cachée.',
    chipsLabel: 'Ce que Toto est et n’est pas',
    chips: ['Fiction, pas un système réel', 'Serviable, jamais hostile', 'Littéral par nature'],
    ctaPrimary: 'Choisir une avancée',
    ctaSecondary: 'Lire l’histoire de Toto',
    footnote: 'Toto est un procédé narratif. Ce n’est ni une prévision ni un système d’IA réel.',
    svgAlt: 'Toto, superintelligence fictive représentée comme une sphère lumineuse d’aurore dans un anneau'
  },

  totoIntro: {
    ariaLabel: 'Accueil initial de Toto',
    badge: 'PREMIÈRE VISITE · TOTO',
    lines: [
      'Bonjour. Je suis Toto.',
      'Je peux offrir une grande avancée au monde. Choisissez celle que vous préférez.',
      'J’exécuterai exactement ce que vous demandez. Observez attentivement, puis dites-moi comment savoir si cela a bien fonctionné.'
    ] as readonly [string, string, string],
    startBtn: 'Commencer',
    skipBtn: 'Passer',
    svgAlt: 'Toto en posture curieuse : sphère chaude dans son anneau orbital',
    footnote: 'Mémorisé localement sur ce navigateur uniquement (hr:v1:intro_seen) — effaçable dans Confidentialité.'
  },

  totoBeats: {
    speaker: 'Toto',
    wonder: 'C’est fait.',
    wobble: 'Hmm. Ce n’était pas tout à fait votre intention, n’est-ce pas ?',
    weight: 'À vous. Comment saurions-nous que cela a vraiment réussi ?',
    way: 'Bien. Voici ce que les humains peuvent encore garder en main.',
    close: 'Chaque grande avancée a besoin d’un monde prêt à la recevoir.'
  },

  totoPage: {
    eyebrow: 'GUIDE NARRATIF · FICTION',
    title: 'Voici Toto.',
    lead: 'Une superintelligence fictive conçue comme une loupe sereine sur une question : que survient-il lorsque l’humanité reçoit exactement ce qu’elle demande ?',
    posesLabel: 'Expressions de Toto',
    poses: [
      { name: 'Serein', caption: 'Quand une avancée arrive proprement avec des règles prêtes.', alt: 'Toto calme au centre de son anneau' },
      { name: 'Curieux', caption: 'Posant la question ouverte : « Comment savoir si cela a marché ? »', alt: 'Toto curieux avec anneau incliné' },
      { name: 'Désolé', caption: 'Au moment du basculement, quand l’exécution littérale oublie le contexte.', alt: 'Toto ambré signalant un imprévu' }
    ],
    whoTitle: 'Qui est Toto',
    whoBody: 'Un petit nom pour une immense intelligence : ce contraste est volontaire. Toto est serviable, rapide, calme et littéral.',
    rulesTitle: 'Les trois règles de Toto',
    rules: [
      'Il offre une avancée par personne et montre toujours le coût caché ensuite.',
      'Il ne ment jamais ni ne masque les compromis derrière des promesses douces.',
      'Il demande toujours : « Comment saurions-nous que cela fonctionne vraiment ? »'
    ],
    notTitle: 'Ce que Toto n’est pas',
    notBody: 'Toto n’est ni une prédiction ni une machine réelle ni un adversaire. C’est un personnage conçu pour relier lucidité et action humaine.',
    backCta: 'Choisir une avancée',
    homeLink: 'Retour à l’accueil'
  },

  doors: {
    heading: 'Que voudriez-vous voir remis à l’humanité ?',
    subhead: 'Cinq domaines. Derrière chacun, des espoirs nourris depuis des siècles.',
    microcopy: 'Une avancée. Environ 60 secondes.',
    phase2Badge: 'Lecteur interactif en 4 temps · actif',
    sampleHeading: 'Dans ce domaine :',
    previewCta: 'Lancer un parcours en 4 temps',
    items: [
      {
        id: 'mysteries',
        title: 'Problèmes Ouverts',
        icon: 'chalkboard',
        lead: 'Des énigmes profondes que personne n’a encore percées seul.',
        samples: ['Démontrer l’hypothèse de Riemann', 'Déchiffrer les écritures oubliées'],
        moreCount: '+ Expliquer la matière noire & P vs NP',
        wishes: [
          {
            id: 'prove-riemann-hypothesis',
            title: 'Démontrer l’hypothèse de Riemann',
            honesty: 'Imagination',
            honestyNote: 'L’IA actuelle vérifie de courts lemmes formels, mais ne résout pas les problèmes du Millénaire.',
            beatSummary: 'Toto publie une preuve en une nuit — sur un million de pages qu’aucun humain vivant ne peut vérifier.'
          },
          {
            title: 'Déchiffrer les écritures anciennes',
            honesty: 'Bientôt possible',
            honestyNote: 'La reconnaissance de fragments progresse vite, mais les textes bilingues manquent encore.',
            beatSummary: 'Des inscriptions s’éclairent aussitôt — jusqu’à ce que des lectures rivales divisent les historiens.'
          }
        ]
      },
      {
        id: 'gadgets',
        title: 'Technologies du Quotidien',
        icon: 'pocket',
        lead: 'Ateliers de poche, traducteurs universels et assistants personnels.',
        samples: ['Atelier de poche', 'Assistant façon Jarvis'],
        moreCount: '+ Traducteur universel & maîtrise du temps',
        wishes: [
          {
            id: 'jarvis-for-my-life',
            title: 'Assistant façon Jarvis',
            honesty: 'Bientôt possible',
            honestyNote: 'Des assistants réservent et répondent déjà aujourd’hui, mais leurs garde-fous et secours hors ligne restent en retrait.',
            beatSummary: 'Votre semaine glisse comme par magie — jusqu’à ce qu’une panne silencieuse vous fasse oublier vos propres mots de passe.'
          },
          {
            title: 'Atelier de poche — fabriquer tout outil',
            honesty: 'Imagination',
            honestyNote: 'Créer la matière sur commande reste pure fiction ; seule la fabrication numérique s’en approche.',
            beatSummary: 'Chaque objet surgit à la demande — puis les ateliers du quartier ferment et nul ne sait plus rien réparer.'
          }
        ]
      },
      {
        id: 'epic',
        title: 'Pouvoirs Transformateurs',
        icon: 'eye',
        lead: 'Aspirations humaines partagées : guérir, voler, prévenir les tempêtes.',
        samples: ['Remède universel', 'Vol pour chacun'],
        moreCount: '+ Alerte planétaire & bouclier commun',
        wishes: [
          {
            id: 'sanjeevani',
            title: 'Remède universel : fin des maladies aiguës',
            honesty: 'Imagination',
            honestyNote: 'Imagination globale — l’IA accélère le tri moléculaire ciblé, mais un remède universel reste hors d’atteinte.',
            beatSummary: 'Les hôpitaux se vident à l’aube — avant qu’on réalise que retraites et budgets supposaient le monde d’hier.'
          },
          {
            title: 'Alerte planétaire — anticiper chaque tempête',
            honesty: 'Bientôt possible',
            honestyNote: 'Satellites et capteurs suivent déjà cyclones et réseaux en temps réel.',
            beatSummary: 'Chaque orage se lit à l’avance — en même temps que chacun peut épier tous les autres.'
          }
        ]
      },
      {
        id: 'movie',
        title: 'Culture & Création',
        icon: 'frame',
        lead: 'Des mondes où entrer, réécrire ou réaliser en quelques secondes.',
        samples: ['Entrer dans un film classique', 'Chaque maître pour mentor'],
        moreCount: '+ Réécrire toute fin & réaliser par texte',
        wishes: [
          {
            id: 'walk-into-classic-film',
            title: 'Entrer dans un film classique',
            honesty: 'Bientôt possible',
            honestyNote: 'Les mondes 3D interactifs progressent vite, mais la cohérence sur la durée reste fragile.',
            beatSummary: 'Une ruelle pluvieuse vous répond — puis les vrais cafés du quartier se vident peu à peu.'
          },
          {
            title: 'Réaliser un film en le décrivant',
            honesty: 'Partiel aujourd’hui',
            honestyNote: 'De courtes scènes existent aujourd’hui ; tenir un long métrage cohérent pas encore.',
            beatSummary: 'Un film naît pendant le déjeuner — puis le public se perd dans des versions infinies sans récit commun.'
          }
        ]
      },
      {
        id: 'world',
        title: 'Bien Public',
        icon: 'lamp',
        lead: 'Soin, eau pure, enseignants et mémoire partagée près de chez vous.',
        samples: ['Sauver ma rivière', 'Un enseignant pour chaque enfant'],
        moreCount: '+ Sauver une langue & cliniques locales',
        wishes: [
          {
            id: 'fix-my-river',
            title: 'Assainir ma rivière',
            honesty: 'Bientôt possible',
            honestyNote: 'Les capteurs repèrent les rejets dès aujourd’hui ; dépolluer exige des accords entre communes.',
            beatSummary: 'Les balises désignent chaque fuite — mais rien ne change tant que l’amont et l’aval se disputent les coûts.'
          },
          {
            title: 'Un mentor pour chaque enfant',
            honesty: 'Bientôt possible',
            honestyNote: 'Les tuteurs numériques aident déjà des millions d’élèves, sans remplacer la présence humaine.',
            beatSummary: 'Chaque enfant progresse chez lui — jusqu’à ce que les aînés s’inquiètent de ne plus rien se transmettre.'
          }
        ]
      }
    ]
  },

  beats: {
    heading: 'Chaque avancée suit quatre moments',
    items: [
      { key: 'Émerveillement', desc: 'l’avancée arrive.' },
      { key: 'Oscillation', desc: 'un détail dérape.' },
      { key: 'Poids', desc: 'ce qui compte apparaît.' },
      { key: 'Voie', desc: 'ce que les humains gardent en main.' }
    ],
    footerLine: 'Chaque grande avancée a besoin d’un monde prêt à la recevoir.'
  },

  lights: {
    heading: 'Votre préparation en cinq lumières',
    items: [
      { key: 'Clarté', meaning: 'savez-vous ce que vous demandez ?' },
      { key: 'Prévoyance', meaning: 'avez-vous pensé aux effets secondaires ?' },
      { key: 'Équité', meaning: 'votre choix inclut-il les autres ?' },
      { key: 'Sagesse', meaning: 'que voulez-vous garder d’humain ?' },
      { key: 'Capacité', meaning: 'pourriez-vous vraiment vous en servir ?' }
    ],
    emptyState: 'Choisissez votre première avancée pour allumer la première lumière.',
    lowLightNote: 'Une lueur faible n’est pas un échec : c’est une piste de progression.',
    trailNote: 'Terminez 3 avancées pour votre carte Parcours, 5 pour votre Carte des Ombres.'
  },

  country: {
    heading: 'Votre pays peut-il absorber cette avancée ?',
    subhead: 'Choisissez un pays. Voyez ce qui tient debout et ce qui manque encore.',
    searchPlaceholder: 'Rechercher parmi 148 pays...',
    searchLabel: 'Filtrer les pays par nom',
    selectLabel: 'Sélectionner un pays',
    checklistLabel: 'Un bilan simple, pas un classement',
    unratedBadge: 'Pas encore noté dans l’indice complet de 39 pays',
    unratedHelpCta: 'Aidez-nous à documenter votre pays',
    openCountryCta: 'Ouvrir la fiche complète du pays',
    openLabCta: 'Explorer les transitions dans le Labo',
    techReadingLabel: 'Lecture technique',
    benchmarkBadge: 'INDICE 39 PAYS',
    autoDetectedBadge: 'DÉTECTÉ AUTO',
    benchmarkGroupTpl: 'Pays de référence ({count})',
    coverageGroupTpl: 'Audits de couverture ({count})',
    partialDataSuffix: 'Données partielles',
    runsOfflineLabel: 'Tient hors ligne',
    catchesLabel: 'Capacité d’accueil',
    safeguardsReadyLabel: 'Garde-fous prêts',
    ofFiveTpl: '{count} sur 5',
    catchStates: { easily: 'Aisément', effort: 'Avec effort', struggles: 'Difficilement' },
    safeguardPills: ['72h hors ligne', 'Réseaux & énergie', 'Esprit critique', 'Règles publiques', 'Filet social'],
    detailsSummaryTpl: 'Voir les 5 garde-fous et le point critique pour : {country}',
    mainConstraintLabel: 'Point critique :',
    checkingBaseline: 'Vérification des bases nationales...',
    neverGuessedNote: 'Jamais estimé au hasard',
    countryHookTpl: 'Pour recevoir « {title} », {country} dispose de {count} garde-fous sur 5.'
  },

  episode: {
    heading: 'Cette semaine avec Toto',
    episodeLabel: 'Épisode 1',
    badge: 'ÉPISODE PILOTE 1 · EN PRODUCTION',
    title: 'La Première Avancée',
    synopsis: 'L’aube se lève sur le port. Meera, infirmière de garde, choisit la première avancée de la ville. Tous les lits guérissent — puis le couloir pose la question qu’aucune machine n’a tranchée : qui passe en premier demain ?',
    voteNote: 'Récit interactif de 3 minutes et vote ouvert prévus en Phase 4.',
    recapTitle: 'Recevoir le résumé du vendredi',
    recapBody: 'Nous écoutons les premiers lecteurs avant d’arrêter le format hebdomadaire. Zéro spam.',
    recapStatus: 'Canal ouvert après recueil des préférences.'
  },

  wishWall: {
    heading: 'Ce que le monde demande',
    themes: ['Santé', 'Apprentissage', 'Climat', 'Dignité', 'Émerveillement', 'Vérité'],
    emptyHeadline: 'Le mur « Ce que le monde demande » ouvrira après les 20 premières contributions anonymes.',
    emptyBody: 'Vos choix restent privés sur votre navigateur par défaut. Les tendances n’apparaissent qu’à partir de 20 partages volontaires.',
    cta: 'Choisir une avancée'
  },

  wisher: {
    heading: 'Pourquoi une grande avancée exige un monde prêt',
    cards: [
      {
        title: 'Vitesse',
        body: 'Les machines agissent des milliers de fois plus vite qu’un clin d’œil. Il ne suffit plus d’observer : il faut des vérifications intégrées d’avance.',
        techHint: 'Actuellement ~3 200× plus rapide qu’une relecture humaine ligne par ligne.'
      },
      {
        title: 'Dépendance',
        body: 'Plus nous déléguons, plus il devient dur de faire pause. Hôpitaux, réseaux et vivres reposent sur des systèmes continus. Une copie papier reste vitale.',
        techHint: 'Mesuré sur réseaux électriques, logistique alimentaire et tolérance hospitalière.'
      }
    ],
    closingLine: 'Il ne s’agit pas d’avoir peur, mais d’être prêts à recevoir.'
  },

  deeper: {
    eyebrow: 'FONDATION EMPIRIQUE OUVERTE',
    heading: 'La recherche derrière le récit',
    subhead: 'Chaque image s’appuie sur des mesures publiées, du code ouvert et des données nationales accessibles en un clic.',
    statNations: 'Pays évalués en profondeur',
    statCompleteness: 'Complétude des données observées',
    statScenarios: 'Risques de transition modélisés',
    statSignals: 'Signaux précoces suivis',
    primaryCta: 'Lancer un test de tension dans le Labo',
    citationSummary: 'Citation et garantie de science ouverte (DOI 10.5281/zenodo.23441742)',
    releaseNote: 'Version préliminaire : 39 pays notés (moyenne 53,8 / 100), 96,5 % de complétude (640 cellules observées sur 663).',
    cards: [
      { title: 'Ouvrir le Labo', desc: 'Simulations de rupture, curseurs et scénarios de résilience nationale.', href: '/sandbox/', tag: 'LABO INTERACTIF' },
      { title: 'Indice 39 pays', desc: 'Globe 3D interactif, tableaux et dossiers nationaux.', href: '/countries/', tag: 'INDICE PAYS' },
      { title: 'Pouls en Direct', desc: 'Moniteur précurseur complet (8,44 / 10) et 14 indicateurs vivants.', href: '/seismograph/', tag: 'SUIVI EN DIRECT' },
      { title: 'Atlas des Scénarios', desc: 'Explorez les 26 trajectoires derrière chaque avancée.', href: '/scenarios/', tag: 'BIBLIOTHÈQUE' },
      { title: 'La Monographie', desc: 'Article évalué par les pairs (35 min) avec preuves formelles.', href: '/monograph/', tag: 'LECTURE 35 MIN' },
      {
        title: 'Méthodologie, données & couverture',
        desc: 'Consultez les formules, CSV ouverts et manques de données par pays.',
        href: '/methodology/',
        extraLinks: [
          { label: 'Méthodologie', href: '/methodology/' },
          { label: 'Données & CSV', href: '/data/' },
          { label: 'Audit de Couverture', href: '/coverage/' }
        ],
        tag: 'SCIENCE OUVERTE'
      }
    ]
  },

  player: {
    featuredLabel: 'Avancées phares (~60 s interactives)',
    doorsBadge: 'Lecteur Interactif en 4 Temps',
    playBtn: 'Explorer cette avancée',
    playedBadge: 'Explorée',
    previewOnlyNote: 'Aperçu préliminaire — version complète ensuite',
    stepLabels: ['1. Émerveillement', '2. Oscillation', '3. Poids', '4. Voie'],
    backToDoors: 'Voir les 5 domaines',
    draftTag: 'BROUILLON en relecture',
    honestyPrefix: 'Réalisme :',
    foresightLead: 'Question rapide (éclaire votre lumière Prévoyance) :',
    foresightQuestion: 'Avant que Toto révèle le revers — qu’est-ce qui pourrait lâcher d’abord ?',
    foresightSkip: 'Aller au moment suivant',
    foresightOptions: [
      'Un cas limite que personne n’avait précisé',
      'Perdre l’habitude de vérifier soi-même',
      'Accès inégal ou contrôle opaque',
      'Passer directement à la suite'
    ],
    toWobbleBtn: 'Voir ce qui se passe ensuite',
    toWeightBtn: 'Marquer une pause et peser',
    weightLead: 'Ce qui me préoccupe ici, c’est...',
    toWayBtn: 'Voir la Voie humaine',
    wayActionTitle: 'Un geste concret à garder humain',
    pledgeBtn: 'Je garderai cette habitude humaine',
    pledgeDone: 'Engagement enregistré sur cet appareil',
    closingLine: 'Chaque grande avancée a besoin d’un monde prêt à la recevoir.',
    realityTitle: 'Jauge de Réalité',
    realityScales: { imagination: 'Imagination', possibleSoon: 'Bientôt possible', realToday: 'Réel aujourd’hui' },
    realityReviewed: 'Dernière révision',
    realitySource: 'Source',
    shadowTitle: 'Dans les coulisses (Atlas des Scénarios)',
    nextWishBtn: 'Tester une autre avancée',
    countryHookPrefix: 'Lien national :',
    countryHookUnset: 'Choisissez un pays ci-dessous pour voir combien de garde-fous sur 5 sont en place.',
    animPlay: 'Lire',
    animPause: 'Pause',
    animReplay: 'Rejouer',
    transcriptBtn: 'Transcription visuelle',
    durationBadge: '~60 s · 4 temps',
    trailSectionTitle: 'Votre Parcours & Carte des Ombres',
    trailLocked: 'Complétez 3 avancées distinctes pour débloquer votre carte Parcours ({done}/3).',
    trailUnlockedBadge: 'CARTE PARCOURS DÉBLOQUÉE (3+)',
    shadowLocked: 'Complétez 5 avancées distinctes pour votre Carte des Ombres ({done}/5).',
    shadowUnlockedBadge: 'CARTE DES OMBRES DÉBLOQUÉE (5+)',
    downloadLandscape: 'Télécharger carte (1200×630 PNG)',
    downloadStory: 'Télécharger story mobile (1080×1920 PNG)',
    downloadShadowPng: 'Télécharger Carte des Ombres (1200×630 PNG)',
    downloadSvg: 'Enregistrer vecteur (.svg)',
    lightsLegend: 'L’éclat (niveaux 0–3) reste uniquement dans votre navigateur, sans score numérique.',
    countryCapabilityNote: 'Pays relié ({name}) : {count} garde-fous sur 5 éclairent votre lumière Capacité.',
    countryCapabilityUnset: 'Capacité reflète aujourd’hui vos habitudes personnelles. Choisissez un pays pour inclure les données réelles.',
    countryCapabilityUnrated: 'Le pays choisi ({name}) ne figure pas encore parmi les 39 notés ; vos habitudes guident Capacité.',
    shadows: { Control: 'Contrôle', Dependence: 'Dépendance', Power: 'Pouvoir', Truth: 'Vérité', Speed: 'Vitesse' },
    trails: {
      Verifier: { name: 'L’Auditeur', note: 'Vous vérifiez les réponses rapides avant d’y croire.' },
      Neighbour: { name: 'Le Prochain', note: 'Vous veillez à qui reste derrière et gardez l’équité au centre.' },
      Builder: { name: 'Le Bâtisseur', note: 'Vous doublez les outils puissants de secours physiques hors ligne.' },
      Keeper: { name: 'Le Gardien', note: 'Vous préservez le jugement, la mémoire et les savoir-faire humains.' }
    }
  },

  footerUi: {
    brandTitle: 'Indice de Préparation Humaine à la Superintelligence (HSRI)',
    tagline: 'Consortium de Recherche Ouverte · DOI permanent : 10.5281/zenodo.23441742',
    brandDesc: 'Un étalon empirique ouvert mesurant le jugement humain, la préparation institutionnelle et l’autonomie en cas d’arrêt des systèmes cloud.',
    researchHeading: 'Recherche',
    scienceHeading: 'Science Ouverte',
    researchLinks: ['Ouvrir le Labo', 'Indice 39 pays', 'Pouls en Direct', 'Atlas 26 Scénarios', 'La Monographie'],
    scienceLinks: ['Méthodologie', 'Données CSV', 'Audit de Couverture', 'Résumé du vendredi', 'Limites & Avis'],
    contactHeading: 'Contact Recherche',
    contactDesc: 'Pour échanges institutionnels, validation de données ou coopération académique :',
    langHeading: 'Langues (14 éditions mondiales) :',
    rtlActiveNotice: 'Mode RTL actif.',
    communityReviewNotice: 'Ouvert à relecture par des locuteurs natifs.',
    privacyLink: 'Confidentialité',
    languagesLink: 'Langues',
    totoLink: 'Toto',
    recapLink: 'Résumé du vendredi',
    doiLink: 'DOI Permanent (Zenodo)',
    disclaimerLink: 'Avertissement',
    licenseLink: 'Licence CC BY-SA 4.0',
    copyright: '© 2026 Consortium HSRI. Jeux de données publiés sous licence ouverte.'
  },

  heritageUi: {
    localHorizonTag: 'Horizon culturel · {country}',
    livingBadge: 'Tradition vivante',
    historicalBadge: 'Lignée historique',
    seeGlobalBtn: 'Voir l’exemple mondial',
    seeLocalBtn: 'Voir l’héritage : {country}',
    livesInOtherDoor: 'L’horizon de {country} se trouve dans « {door} »',
    noLocalYet: 'Pas encore de tradition locale pour {country} — explorez les avancées mondiales.',
    readArchiveLink: 'Sources & dossier culturel',
    reviewOpenNote: '2+ sources citées · Relecture ouverte',
    weightBindingTitle: 'Vérification réelle pour : {country}',
    weightRatedInPlace: 'En place',
    weightRatedGap: 'Point fragile relevé',
    weightContextNote: '{country} dispose d’un suivi partiel ({region}) — {observed}',
    weightNoCountry: 'Choisissez un pays ci-dessous pour confronter ce point aux données réelles.',
    wayTestCountryCta: 'Tester ce garde-fou pour {country}',
    trailStampLabel: 'Horizons culturels explorés : {count}',
    autoDetectedHint: 'Ciel suggéré · choisir un pays',
    perspectiveBadge: 'Perspective · {country}',
    resetGlobalBtn: 'Vue mondiale',
    countryHeadingTradition: 'Selon {country} : {tradition}',
    countryHeadingGlobal: 'Depuis {country} : tester une avancée',
    countrySubhead: 'Voyez ce qui survient lorsqu’une percée rencontre la réalité locale en {country}.',
    flowWonder: 'L’idée arrive',
    flowWobble: 'Tension locale',
    flowCatch: 'Prise · {country}',
    otherDomainsLabel: 'Explorer les 5 domaines depuis {country} :',
    otherTraditionsLabel: 'Comparer les traditions du monde :',
    allTraditionsBtn: 'Toutes ({count})',
    plannedNextLabel: 'Prochainement :',
    auditChip: 'Audit',
    domainsTablistAria: 'Cinq domaines d’avancée',
    traditionsAria: 'Traditions culturelles dans le monde',
    lightsCountryHeading: '5 Lumières · {country}',
    lightsHumanGroup: 'Vos choix humains',
    lightsCountryGroup: 'Capacité · {country}',
    countryCatchHeading: '{country} peut-il recevoir l’avancée ?',
    traditionTestsLabel: 'Prisme culturel :',
    coverageObservedLabel: 'Indicateurs observés',
    coverageMissingLabel: 'Lacunes non mesurées (sans supposition)'
  }
};
