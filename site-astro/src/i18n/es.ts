// Spanish translation dictionary for Humanity Readiness (Phase 2 global i18n)
// Calm, plain-language copy without Section 12 technical jargon.
import type { TranslationDict } from './en';

export const es: TranslationDict = {
  lang: 'es',
  dir: 'ltr',
  label: 'Español',

  meta: {
    title:
      'Humanity Readiness: ¿estamos listos para recibir lo que deseamos? | Humanity Superintelligence Readiness Index',
    description:
      'Imagina que una superinteligencia te ofrece un deseo. Elígelo, míralo hacerse realidad y descubre qué pueden seguir haciendo las personas. Con el respaldo de datos abiertos en 39 países.'
  },

  hero: {
    eyebrow: 'UNA HISTORIA DE PREPARACIÓN HUMANA',
    headline: 'Humanity Readiness: ¿estamos listos para recibir lo que deseamos?',
    subhead:
      'Imagina que una superinteligencia te concede un deseo. Elígelo. Míralo hacerse realidad. Y descubre qué haría falta de verdad.',
    ctaPrimary: 'Pide tu deseo',
    ctaSecondary: 'Mira cómo va tu país',
    cityLabel: 'Cielo de llegada sobre:',
    cityNeutralName: 'Puerto Costero',
    cityNeutralNote: 'Vista portuaria neutral · elige una ciudad para cambiar el horizonte',
    kalpaCaption: 'Kalpa llega al amanecer: «Puedo ofrecer un deseo por persona. Pídelo con claridad.»',
    ringTitle: 'La preparación de la humanidad, según personas como tú',
    ringEmptyHeadline: 'Sé una de las primeras 200 personas en pedir un deseo.',
    ringEmptySub: 'El pulso colectivo aparecerá aquí cuando 200 personas hayan completado un deseo.'
  },

  pulse: {
    label: 'Pulso de la Humanidad',
    tooltipTrigger: 'Lectura técnica',
    states: {
      steady: {
        word: 'Estable',
        sentence:
          'Las herramientas automáticas todavía avanzan despacio para que las personas revisen cada decisión.'
      },
      stirring: {
        word: 'En movimiento',
        sentence:
          'Los sistemas de software empiezan a superar el ritmo de la revisión manual. Conviene revisar planes de respaldo.'
      },
      rising: {
        word: 'En ascenso',
        sentence:
          'Esta semana las máquinas aceleraron en tareas de varios pasos que antes revisaban personas. Por eso importan las verificaciones.'
      }
    },
    cta: 'Ver el pulso en vivo'
  },

  doors: {
    heading: '¿Qué desearías?',
    subhead: 'Cinco puertas. Detrás de cada una, anhelos que la humanidad ha soñado durante siglos.',
    microcopy: 'Un deseo. Unos 60 segundos.',
    phase2Badge: 'Reproductor interactivo de 4 momentos · activo',
    sampleHeading: 'Dentro de esta puerta:',
    previewCta: 'Jugar un deseo de 4 momentos',
    items: [
      {
        id: 'mysteries',
        title: 'Misterios sin Resolver',
        icon: 'chalkboard',
        lead: 'Preguntas profundas que nadie ha resuelto en solitario todavía.',
        samples: ['Demostrar la Hipótesis de Riemann', 'Leer la escritura del Indo'],
        moreCount: '+ Explicar la materia oscura y P vs NP',
        wishes: [
          {
            id: 'prove-riemann-hypothesis',
            title: 'Demostrar la Hipótesis de Riemann',
            honesty: 'Imaginación',
            honestyNote:
              'La IA actual verifica lemas cortos, pero no resuelve problemas del Milenio completos.',
            beatSummary:
              'Kalpa publica una demostración de la noche a la mañana, pero ocupa un millón de páginas que nadie vivo puede leer.'
          },
          {
            title: 'Leer la escritura del Indo',
            honesty: 'Posible pronto',
            honestyNote:
              'El reconocimiento de patrones en sellos breves avanza rápido, aunque faltan textos bilingües de referencia.',
            beatSummary:
              'Las inscripciones cobran vida al instante — hasta que distintas lecturas enfrentan a los historiadores sobre qué vale como prueba.'
          }
        ]
      },
      {
        id: 'gadgets',
        title: 'Artefactos de Imaginación',
        icon: 'pocket',
        lead: 'Bolsillos imposibles, traductores universales y asistentes personales.',
        samples: ['El bolsillo de Doraemon', 'Un Jarvis para mi vida'],
        moreCount: '+ Traductor universal y Giratiempo',
        wishes: [
          {
            id: 'jarvis-for-my-life',
            title: 'Un Jarvis para mi vida',
            honesty: 'Posible pronto',
            honestyNote:
              'Ya existen asistentes que reservan, pagan y responden, aunque sus límites confiables aún van detrás.',
            beatSummary:
              'Tu semana fluye como magia — hasta que un fallo silencioso te deja sin recordar ni tus propias contraseñas.'
          },
          {
            title: 'El bolsillo de Doraemon',
            honesty: 'Imaginación',
            honestyNote:
              'Crear objetos físicos bajo demanda sigue siendo ficción; solo la fabricación digital se acerca al borde.',
            beatSummary:
              'Cualquier herramienta aparece al instante — hasta que cierran los talleres del barrio y nadie sabe reparar nada.'
          }
        ]
      },
      {
        id: 'epic',
        title: 'Poderes Épicos',
        icon: 'eye',
        lead: 'Relatos antiguos de visión lejana, vuelo, curación y protección.',
        samples: ['Sanjeevani (curar todo)', 'Pushpaka Vimana (vuelo para todos)'],
        moreCount: '+ Divya drishti y escudo Brahmastra',
        wishes: [
          {
            id: 'sanjeevani',
            title: 'Sanjeevani — curarlo todo',
            honesty: 'Imaginación',
            honestyNote:
              'Imaginación en conjunto — la IA ya apoya el descubrimiento en enfermedades concretas (Posible pronto), no una cura universal.',
            beatSummary:
              'Las salas de hospital se vacían al alba — y luego todos descubren que las reglas de cuidado y presupuesto eran del mundo de ayer.'
          },
          {
            title: 'Divya drishti — visión a distancia',
            honesty: 'Posible pronto',
            honestyNote:
              'Satélites y sensores globales ya siguen tormentas e infraestructuras en tiempo real.',
            beatSummary:
              'Cada tormenta se ve a kilómetros de distancia — junto a la certeza de que cualquiera puede observar a los demás.'
          }
        ]
      },
      {
        id: 'movie',
        title: 'Vivir una Película',
        icon: 'frame',
        lead: 'Mundos en los que puedes entrar, reescribir o dirigir en segundos.',
        samples: ['Entrar en un clásico del cine', 'Cada maestro como mi mentor'],
        moreCount: '+ Reescribir finales y dirigir con texto',
        wishes: [
          {
            id: 'walk-into-classic-film',
            title: 'Entrar en un clásico del cine',
            honesty: 'Posible pronto',
            honestyNote:
              'Los mundos 3D interactivos avanzan rápido, pero la memoria coherente a largo plazo sigue siendo frágil.',
            beatSummary:
              'Caminas por una calle bajo la lluvia que responde a tu voz — y notas menos gente en los cafés reales de tu barrio.'
          },
          {
            title: 'Dirigir cine con una frase',
            honesty: 'Parcialmente real hoy',
            honestyNote:
              'Las escenas breves ya funcionan; el control cinematográfico de varias horas aún no.',
            beatSummary:
              'Un largometraje se genera al mediodía — y el público se ahoga en millones de versiones sin una historia común.'
          }
        ]
      },
      {
        id: 'world',
        title: 'Deseos para Mi Mundo',
        icon: 'lamp',
        lead: 'Cuidado, agua limpia, docentes y memoria compartida donde vives.',
        samples: ['Limpiar mi río', 'Un docente para cada niño'],
        moreCount: '+ Revivir una lengua y clínicas locales',
        wishes: [
          {
            id: 'fix-my-river',
            title: 'Limpiar mi río',
            honesty: 'Posible pronto',
            honestyNote:
              'Los sensores detectan vertidos a tiempo; limpiar la cuenca física exige acuerdos humanos.',
            beatSummary:
              'El sensor marca cada desagüe contaminante — pero nada cambia hasta que los pueblos acuerdan quién reduce su vertido.'
          },
          {
            title: 'Un docente para cada niño',
            honesty: 'Posible pronto',
            honestyNote:
              'Tutores digitales ya apoyan el estudio; el acompañamiento humano y la comunidad escolar siguen siendo esenciales.',
            beatSummary:
              'Cada niño avanza desde casa — hasta que los mayores preguntan qué pasa cuando los vecinos dejan de enseñarse entre sí.'
          }
        ]
      }
    ]
  },

  beats: {
    heading: 'Cada deseo tiene cuatro momentos',
    items: [
      { key: 'Asombro', desc: 'Tu deseo se cumple.' },
      { key: 'Tambaleo', desc: 'Algo pequeño sale de lado.' },
      { key: 'Peso', desc: 'Notas lo que importa.' },
      { key: 'Camino', desc: 'Ves lo que aún podemos hacer.' }
    ],
    footerLine: 'Todo gran deseo necesita a alguien preparado para pedirlo.'
  },

  lights: {
    heading: 'Tu preparación, en cinco luces',
    items: [
      { key: 'Claridad', meaning: '¿sabes lo que quieres?' },
      { key: 'Previsión', meaning: '¿pensaste en los efectos secundarios?' },
      { key: 'Equidad', meaning: '¿tu deseo incluyó a los demás?' },
      { key: 'Sabiduría', meaning: '¿qué conservarías humano?' },
      { key: 'Capacidad', meaning: '¿podrías usar el regalo de verdad?' }
    ],
    emptyState: 'Pide tu primer deseo para encender tu primera luz.',
    lowLightNote: 'Una luz tenue no es un fracaso: muestra dónde crecer después.',
    trailNote: 'Completa 3 deseos para desbloquear tu tarjeta de recorrido y 5 para tu Mapa de Sombras.'
  },

  country: {
    heading: '¿Puede tu país recibir el regalo?',
    subhead: 'Elige un país. Mira qué ya funciona y qué falta aún.',
    searchPlaceholder: 'Buscar entre 148 países...',
    checklistLabel: 'Lista sencilla, no un ranking',
    unratedBadge: 'Aún sin calificación completa en el índice de 39 países',
    unratedHelpCta: 'Ayúdanos a evaluar tu país',
    openCountryCta: 'Abrir página completa del país',
    openLabCta: 'Explorar transiciones en el Laboratorio',
    techReadingLabel: 'Lectura técnica'
  },

  episode: {
    heading: 'Esta semana en la ciudad de Kalpa',
    badge: 'EPISODIO PILOTO 1 · EN PRODUCCIÓN',
    title: 'El Primer Deseo',
    synopsis:
      'Amanece en el puerto. Meera, en el turno de noche del hospital, pide el primer deseo de la ciudad. Todas las camas sanan — y el pasillo hace la pregunta que ninguna máquina resolvió: ¿quién pasa primero mañana?',
    voteNote: 'Historia interactiva de 3 minutos y votación abierta en la Fase 4.',
    recapTitle: 'Recibe el resumen del viernes',
    recapBody: 'Escuchamos a los primeros visitantes antes de elegir el formato semanal. Cero spam.',
    recapStatus: 'El canal de envío abrirá cuando definamos las preferencias.'
  },

  wishWall: {
    heading: 'Lo que el mundo está deseando',
    themes: ['Salud', 'Aprendizaje', 'Clima', 'Dignidad', 'Asombro', 'Verdad'],
    emptyHeadline: 'El Muro Global abrirá tras los primeros 20 deseos compartidos de forma anónima.',
    emptyBody:
      'Cada deseo permanece privado en tu navegador por defecto. Los temas colectivos solo aparecen cuando al menos 20 personas reales deciden compartirlos.',
    cta: 'Pide un deseo propio'
  },

  wisher: {
    heading: 'Por qué un buen deseo aún necesita un buen guardián',
    cards: [
      {
        title: 'Velocidad',
        body: 'Las máquinas pueden actuar miles de veces más rápido que un parpadeo. No basta con mirar: hacen falta controles antes de recibir el regalo.',
        techHint: 'Actualmente ~3.200× más rápido que la revisión humana línea a línea.'
      },
      {
        title: 'Dependencia',
        body: 'Cuanto más delegamos, más cuesta detenerse. Hospitales, electricidad y alimentos funcionan en sistemas que no se apagan sin más. Un respaldo en papel vale mucho.',
        techHint: 'Medido en redes eléctricas, logística alimentaria y tolerancias hospitalarias.'
      }
    ],
    closingLine: 'No se trata de miedo, sino de estar listos para recibir.'
  },

  deeper: {
    heading: 'La investigación detrás de la historia',
    subhead:
      'Cada metáfora anterior se apoya en mediciones revisadas por pares, código abierto y datos por país a un toque.',
    releaseNote:
      'Edición preliminar: 39 países evaluados (media base 53,8 / 100), 96,5% de integridad de datos (proporción de indicadores observados en 39 países de referencia — 640 de 663 celdas).',
    cards: [
      {
        title: 'Abrir el Laboratorio',
        desc: 'Ejecuta pruebas de estrés personalizadas, controles temporales y escenarios nacionales.',
        href: '/sandbox/',
        tag: 'LABORATORIO INTERACTIVO'
      },
      {
        title: 'Índice de 39 países',
        desc: 'Globo 3D interactivo, clasificaciones completas y expedientes nacionales.',
        href: '/countries/',
        tag: 'ÍNDICE NACIONAL'
      },
      {
        title: 'Pulso en Vivo',
        desc: 'Monitor completo de señales (8,44 / 10), brecha de velocidad y 14 indicadores.',
        href: '/seismograph/',
        tag: 'RASTREADOR EN VIVO'
      },
      {
        title: 'Atlas de Escenarios',
        desc: 'Explora las 26 trayectorias de transición detrás de cada deseo.',
        href: '/scenarios/',
        tag: 'BIBLIOTECA DE SOMBRAS'
      },
      {
        title: 'La Monografía',
        desc: 'Artículo revisado por pares de 35 minutos con pruebas formales (DOI 10.5281/zenodo.23441742).',
        href: '/monograph/',
        tag: 'LECTURA 35 MIN'
      },
      {
        title: 'Metodología, datos y cobertura',
        desc: 'Consulta fórmulas, descarga CSV abiertos o revisa países aún sin datos completos.',
        href: '/methodology/',
        extraLinks: [
          { label: 'Metodología', href: '/methodology/' },
          { label: 'Datos y Descargas', href: '/data/' },
          { label: 'Auditoría Global', href: '/coverage/' }
        ],
        tag: 'CIENCIA ABIERTA'
      }
    ]
  },

  player: {
    featuredLabel: 'Tres deseos destacados (~60 s interactivos)',
    doorsBadge: 'Reproductor Interactivo de 4 Momentos',
    playBtn: 'Jugar este deseo',
    playedBadge: 'Completado',
    previewOnlyNote: 'Boceto preliminar — la versión completa abre en la Fase 6',
    stepLabels: ['1. Asombro', '2. Tambaleo', '3. Peso', '4. Camino'],
    backToDoors: 'Ver las 5 puertas',
    kalpaDone: 'Kalpa: Hecho.',
    draftTag: 'BORRADOR pendiente de revisión',
    honestyPrefix: 'Realismo:',
    foresightLead: 'Pregunta rápida opcional (ilumina tu luz de Previsión):',
    foresightQuestion: 'Antes de ver el tropiezo, ¿qué podría salir de lado primero?',
    foresightSkip: 'Ir directo al Tambaleo',
    foresightOptions: [
      'Un caso o regla que nadie especificó',
      'Perder el hábito humano de comprobarlo',
      'Acceso desigual o control oculto',
      'Saltar directo al Tambaleo'
    ],
    toWobbleBtn: 'Ver qué pasa después',
    toWeightBtn: 'Detenerse y sopesar',
    weightLead: 'Lo que me inquieta aquí es...',
    toWayBtn: 'Ver el Camino humano',
    wayActionTitle: 'Un paso humano concreto',
    pledgeBtn: 'Mantendré este hábito humano',
    pledgeDone: 'Hábito guardado en este dispositivo',
    closingLine: 'Every great wish needs a good wisher.',
    realityTitle: 'Medidor de Realidad',
    realityReviewed: 'Última revisión',
    realitySource: 'Fuente',
    shadowTitle: 'Detrás de este deseo (Atlas de Escenarios)',
    nextWishBtn: 'Probar otro deseo',
    countryHookPrefix: 'Conexión nacional:',
    countryHookUnset: 'Elige tu país abajo para ver cuántas de 5 salvaguardas tiene listas para este deseo.',
    animPlay: 'Reproducir',
    animPause: 'Pausar',
    animReplay: 'Repetir',
    transcriptBtn: 'Transcripción visual',
    durationBadge: '~60 s · 4 momentos',
    trailSectionTitle: 'Tu Recorrido y Mapa de Sombras',
    trailLocked: 'Completa 3 deseos distintos para desbloquear tu tarjeta compartible ({done}/3 hechos).',
    trailUnlockedBadge: 'TARJETA DESBLOQUEADA (3+ DESEOS)',
    shadowLocked: 'Completa 5 deseos distintos para desbloquear tu Mapa de Sombras ({done}/5 hechos).',
    shadowUnlockedBadge: 'MAPA DE SOMBRAS DESBLOQUEADO (5+ DESEOS)',
    downloadLandscape: 'Descargar tarjeta (1200×630 PNG)',
    downloadStory: 'Descargar historia móvil (1080×1920 PNG)',
    downloadShadowPng: 'Descargar Mapa de Sombras (1200×630 PNG)',
    downloadSvg: 'Guardar vector (.svg)',
    lightsLegend: 'El brillo (niveles 0–3) vive solo en tu navegador, sin puntuaciones numéricas.',
    countryCapabilityNote:
      'País conectado ({name}): aporta {count} de 5 salvaguardas a tu luz de Capacidad.',
    countryCapabilityUnset:
      'Capacidad refleja ahora tus hábitos humanos. Elige un país abajo para sumar datos reales nacionales.',
    countryCapabilityUnrated:
      'Tu país seleccionado ({name}) aún no figura en el índice completo de 39 países; tus hábitos humanos guían Capacidad.',
    shadows: {
      Control: 'Control',
      Dependence: 'Dependencia',
      Power: 'Poder',
      Truth: 'Verdad',
      Speed: 'Velocidad'
    },
    trails: {
      Verifier: {
        name: 'Quien Verifica',
        note: 'Pides comprobar respuestas veloces antes de darlas por ciertas.'
      },
      Neighbour: {
        name: 'Quien Cuida',
        note: 'Preguntas quién queda atrás primero y proteges reglas justas para todos.'
      },
      Builder: {
        name: 'Quien Construye',
        note: 'Acompañas grandes herramientas con respaldos físicos y resiliencia local.'
      },
      Keeper: {
        name: 'Quien Conserva',
        note: 'Mantienes vivos el criterio, la memoria y los oficios humanos.'
      }
    }
  },

  footerUi: {
    brandTitle: 'Índice de Preparación ante la Superinteligencia (HSRI)',
    brandDesc:
      'Referencia empírica abierta que mide el criterio humano, la preparación institucional y cuánto pueden sostenerse las sociedades si los sistemas en la nube se detienen.',
    langHeading: 'Idiomas:',
    rtlActiveNotice: 'Modo RTL activo.',
    privacyLink: 'Privacidad',
    languagesLink: 'Idiomas',
    recapLink: 'Resumen del viernes'
  }
};
