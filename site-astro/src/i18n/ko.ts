// Korean (한국어) translation dictionary for Humanity Readiness
import type { TranslationDict } from './en';

export const ko: TranslationDict = {
  lang: 'ko',
  dir: 'ltr',
  label: '한국어',

  headerUi: {
    homeAria: 'HSRI — 홈',
    tagline: '인류 초지능 대비 지수',
    primaryNavAria: '주요 메뉴',
    nav: {
      sandbox: '실험실',
      sandboxBadge: '시뮬레이터',
      countries: '국가 지수',
      seismograph: '실시간 맥박',
      liveBadge: 'LIVE',
      scenarios: '시나리오 아틀라스',
      monograph: '연구 논문',
      monographBadge: '논문',
      scienceGroup: '과학과 데이터'
    },
    utility: {
      methodology: '연구 방법론',
      methodologyDesc: '산출 기준과 수리적 증명',
      data: '데이터 및 범위',
      dataDesc: '지표와 공개 다운로드',
      researchLogs: '연구 기록',
      researchLogsDesc: '업데이트 및 프리프린트',
      doiDesc: '영구 기록 — CC BY-SA 4.0'
    },
    langSwitcherAria: '웹사이트 언어 선택',
    langMenuLabel: '언어',
    themeDarkAria: '다크 모드로 전환',
    themeLightAria: '밝은 종이 테마로 전환',
    menuOpenAria: '메뉴 열기',
    menuCloseAria: '메뉴 닫기'
  },

  meta: {
    title: '우리가 초지능에게 요구하는 변화, 인류는 받아들일 준비가 되었을까? | HSRI',
    description:
      '하나의 도약을 선택하고, 도착 순간 어디가 흔들리는지 추적하며, 자국의 실제 대비 데이터를 점검하세요. 39개국 공개 연구.'
  },

  hero: {
    eyebrow: '인류 준비도의 이야기',
    headline: '우리가 초지능에게 바라는 변화, 인류는 받아들일 준비가 되었나요?',
    headlineLead: '우리가 초지능에게 바라는 변화, ',
    headlineAccent: '인류는 받아들일 준비가 되었나요?',
    subhead:
      '하나의 혁신을 선택하고, 도착했을 때 생기는 균열을 따라가며, 실제 국가별 데이터로 대비 상태를 확인해 보세요.',
    ctaPrimary: '도약 하나 고르기',
    ctaSecondary: '우리 나라 현황 보기',
    guideCue: '토토(Toto)의 하늘 선택기에서 시작하세요:',
    ctaCountryPrimary: '{country} 시각에서 도약 보기',
    ctaCountrySecondary: '{country}는 버틸 수 있을까?',
    cityLabel: '새벽 하늘 위치:',
    cityNeutralName: '해안 항구',
    cityNeutralOption: '해안 항구 (글로벌)',
    cityNeutralNote: '기본 항구 전망 · 도시를 고르면 지평선이 바뀝니다',
    citySelectLabel: '국가 또는 도시 배경 전환',
    nextCityBtn: '다음 도시',
    nextCityTitle: '다음 나라 위로 토토를 띄우기',
    pauseBtn: '일시정지',
    playBtn: '재생',
    replayBtn: '다시 보기',
    pauseAria: '소개 애니메이션 일시정지',
    playAria: '소개 애니메이션 재생',
    replayAria: '소개 애니메이션 다시 재생',
    scrubAria: '토토 등장 타임라인 탐색',
    jumpSceneAria: '장면 {n}으로 이동',
    regionGroups: {
      'Featured Skies': '추천 하늘',
      Africa: '아프리카',
      Americas: '아메리카',
      'Asia & Middle East': '아시아·중동',
      Europe: '유럽',
      Oceania: '오세아니아',
      'Global view': '전 세계'
    },
    totoCaption: '동틀 녘 토토가 도착합니다: «한 사람당 하나의 도약을 건넬 수 있습니다. 분명하게 요청하세요.»',
    ringTitle: '당신 같은 사람들이 함께 밝히는 인류의 대비도',
    ringEmptyHeadline: '첫 200명의 참여자가 되어 보세요.',
    ringEmptySub: '200명이 한 번의 여정을 마치면 이곳에 공동의 준비 링이 켜집니다.'
  },

  pulse: {
    label: '인류의 맥박',
    sectionKicker: '지금 대비가 필요한 이유 · 실시간 속도 감시',
    tooltipTrigger: '기술 판독치',
    states: {
      steady: { word: '안정', sentence: '자동화 도구는 아직 사람이 결정을 하나씩 검토할 수 있을 만큼 천천히 움직입니다.' },
      stirring: { word: '움직임 시작', sentence: '소프트웨어가 사람의 검토 속도를 앞서기 시작했습니다. 지금 단순한 비상 대책을 점검할 때입니다.' },
      rising: { word: '상승 중', sentence: '이번 주 기계는 예전에 사람이 확인하던 다단계 작업에서 한층 빨라졌습니다. 검증 계획이 중요한 이유입니다.' }
    },
    cta: '실시간 맥박 보기',
    humanPaceLabel: '사람의 속도',
    aiPaceLabel: 'AI 속도 (약 3,200×)'
  },

  totoCard: {
    eyebrow: '안내자 만나기',
    heading: '토토(Toto)를 소개합니다.',
    body: '토토는 한 가지 질문을 탐구하기 위한 가상의 초지능입니다. «인류가 요청한 그대로를 손에 넣으면 어떤 일이 일어날까?» 토토는 친절하고 빠르며 아주 글자 그대로 작동합니다.',
    chipsLabel: '토토의 특징',
    chips: ['허구 캐릭터, 실제 시스템 아님', '도움을 주며 적대적이지 않음', '철저히 글자 그대로 동작'],
    ctaPrimary: '도약 하나 고르기',
    ctaSecondary: '토토 이야기 읽기',
    footnote: '토토는 스토리텔링 장치일 뿐 미래 예측이나 실제 AI가 아닙니다.',
    svgAlt: '가는 궤도 고리 안에서 새벽빛처럼 빛나는 가상의 안내자 토토'
  },

  totoIntro: {
    ariaLabel: '토토의 첫인사',
    badge: '처음 방문 · 토토 만나기',
    lines: [
      '안녕하세요. 저는 토토입니다.',
      '세상에 큰 도약 하나를 전해드릴 수 있어요. 원하는 것을 골라 보세요.',
      '말씀하신 그대로 정확히 실행하겠습니다. 유심히 보신 뒤, 이것이 제대로 작동했는지 우리가 어떻게 알 수 있을지 들려주세요.'
    ] as readonly [string, string, string],
    startBtn: '시작하기',
    skipBtn: '건너뛰기',
    svgAlt: '호기심 어린 모습의 토토',
    footnote: '이 브라우저에만 조용히 저장됩니다 (hr:v1:intro_seen) — 개인정보 페이지에서 언제든 지울 수 있습니다.'
  },

  totoBeats: {
    speaker: '토토',
    wonder: '완료했습니다.',
    wobble: '음… 원래 의도하신 뜻과는 조금 달랐던 모양이네요?',
    weight: '이제 당신 차례입니다. 이게 정말 바르게 작동했는지 어떻게 알 수 있을까요?',
    way: '좋아요. 사람들이 여전히 직접 쥐고 갈 수 있는 해법이 여기 있습니다.',
    close: '모든 위대한 도약에는 준비된 세상이 필요합니다.'
  },

  totoPage: {
    eyebrow: '스토리 가이드 · 픽션',
    title: '토토를 소개합니다.',
    lead: '«인류가 요청한 것을 그대로 얻었을 때 무슨 일이 벌어질까?»를 차분히 살피기 위해 만든 가상의 초지능입니다.',
    posesLabel: '토토의 표정',
    poses: [
      { name: '차분함', caption: '도약이 매끄럽게 도착하고 사회 규칙도 준비된 상태.', alt: '차분한 토토' },
      { name: '호기심', caption: '열린 질문: «제대로 작동했음을 어떻게 확인할까요?»', alt: '호기심 어린 토토' },
      { name: '미안함', caption: '글자 그대로의 이행이 암묵적 맥락을 놓친 흔들림의 순간.', alt: '사과하는 토토' }
    ],
    whoTitle: '토토는 누구인가',
    whoBody: '거대한 지능에 작은 이름—그 대비가 의도입니다. 토토는 차분하고 친절하며 요청받은 문장 그대로를 실현합니다.',
    rulesTitle: '토토의 세 가지 규칙',
    rules: [
      '한 사람에게 한 가지 도약을 건네며, 그 뒤의 대가도 반드시 함께 보여줍니다.',
      '결코 거짓말하지 않으며 편안한 말로 갈등을 가리지 않습니다.',
      '늘 묻습니다. «이게 제대로 됐다는 걸 우리가 어떻게 알죠?»'
    ],
    notTitle: '토토가 아닌 것',
    notBody: '예언이나 실제 제품, 악역이 아닙니다. 성찰과 시민의 실질적 행동을 잇는 서사 장치입니다.',
    backCta: '도약 하나 고르기',
    homeLink: '홈으로 돌아가기'
  },

  doors: {
    heading: '인류에게 무엇이 주어지길 바라시나요?',
    subhead: '다섯 개 영역. 저마다 수 세기 동안 인류가 품어온 꿈이 담겨 있습니다.',
    microcopy: '도약 하나. 약 60초.',
    phase2Badge: '4막 대화형 플레이어 · 작동 중',
    sampleHeading: '이 영역 속 이야기:',
    previewCta: '4막 이야기 체험하기',
    items: [
      {
        id: 'mysteries',
        title: '미해결 난제',
        icon: 'chalkboard',
        lead: '인류가 아직 홀로 풀지 못한 깊은 질문들.',
        samples: ['리만 가설 증명하기', '고대 문자 해독하기'],
        moreCount: '+ 암흑물질 해명 & P vs NP 문제',
        wishes: [
          {
            id: 'prove-riemann-hypothesis',
            title: '리만 가설 증명하기',
            honesty: '상상 단계',
            honestyNote: '오늘날 AI는 짧은 보조정리는 검증하지만 밀레니엄 난제를 풀지는 못합니다.',
            beatSummary: '토토가 하룻밤 새 증명을 발표합니다—하지만 백만 쪽에 달해 살아있는 누구도 끝까지 검증할 수 없습니다.'
          },
          {
            title: '잊힌 고대 문자 해독하기',
            honesty: '머지않아 가능',
            honestyNote: '파편 패턴 분석은 빠르게 늘고 있으나 대조할 이중 언어 자료가 부족합니다.',
            beatSummary: '잃어버린 비문이 순식간에 읽힙니다—이내 엇갈린 해석이 무엇이 증명인지 묻게 합니다.'
          }
        ]
      },
      {
        id: 'gadgets',
        title: '일상의 기술',
        icon: 'pocket',
        lead: '주머니 공방, 만능 번역기, 그리고 일상 비서.',
        samples: ['주머니 공방', '자비스 같은 생활 비서'],
        moreCount: '+ 만능 번역기와 시간 관리',
        wishes: [
          {
            id: 'jarvis-for-my-life',
            title: '자비스 같은 생활 비서',
            honesty: '머지않아 가능',
            honestyNote: '예약과 결제를 돕는 도구는 이미 있지만 안전한 경계선과 오프라인 대안은 뒤처져 있습니다.',
            beatSummary: '한 주가 마법처럼 굴러갑니다—조용한 장애가 난 아침, 내 비밀번호조차 기억나지 않을 때까지.'
          },
          {
            title: '주머니 공방 — 무엇이든 뚝딱 제작',
            honesty: '상상 단계',
            honestyNote: '물질을 즉석에서 찍어내는 일은 여전히 상상의 영역입니다.',
            beatSummary: '어떤 도구든 즉석에서 생겨납니다—어느새 동네 수리점이 사라져 고칠 줄 아는 사람이 남지 않을 때까지.'
          }
        ]
      },
      {
        id: 'epic',
        title: '변혁의 힘',
        icon: 'eye',
        lead: '치유, 비행, 조기 경보, 공동 보호에 대한 인류 공통의 염원.',
        samples: ['만능 치료(급성 질환 종식)', '모두의 비행'],
        moreCount: '+ 지구 규모 태풍 경보와 공동 방패',
        wishes: [
          {
            id: 'sanjeevani',
            title: '만능 치료: 급성 질환의 종식',
            honesty: '상상 단계',
            honestyNote: '전반적으론 상상(좁은 표적 후보 탐색은 AI 지원 가능)—만병통치와는 거리가 멉니다.',
            beatSummary: '새벽 병실이 고요히 비워집니다—곧 병원들은 모든 예산과 연금 규칙이 어제의 세상을 가정했음을 깨닫습니다.'
          },
          {
            title: '행성 조기 경보 — 모든 폭풍 예측',
            honesty: '머지않아 가능',
            honestyNote: '위성과 센서망이 이미 태풍과 기반 시설을 실시간으로 추적합니다.',
            beatSummary: '수백 킬로미터 밖 폭풍도 훤히 보입니다—동시에 모두가 모두를 들여다볼 수 있게 되었다는 사실과 함께.'
          }
        ]
      },
      {
        id: 'movie',
        title: '문화와 창작',
        icon: 'frame',
        lead: '몇 초 만에 걸어 들어가고 고쳐 쓰고 연출하는 세계.',
        samples: ['고전 영화 속으로 들어가기', '모든 거장을 스승으로'],
        moreCount: '+ 결말 바꾸기 & 글로 영화 감독하기',
        wishes: [
          {
            id: 'walk-into-classic-film',
            title: '고전 영화 속으로 걸어 들어가기',
            honesty: '머지않아 가능',
            honestyNote: '대화형 3D 세계는 빠르게 성장하지만 긴 기억의 일관성은 여전히 약합니다.',
            beatSummary: '빗속 골목이 당신 말에 응답합니다—그사이 현실 동네 카페의 발길이 하나둘 줄어드는 것을 봅니다.'
          },
          {
            title: '말로 설명해 영화 한 편 완성하기',
            honesty: '오늘 일부 가능',
            honestyNote: '짧은 장면은 오늘도 만들 수 있으나 장편 서사 제어는 아직 어렵습니다.',
            beatSummary: '점심시간에 장편 영화가 완성됩니다—관객들은 각자의 맞춤형 편집본 속에서 함께 나눌 이야기를 잃습니다.'
          }
        ]
      },
      {
        id: 'world',
        title: '공공의 선',
        icon: 'lamp',
        lead: '우리 동네의 돌봄, 맑은 강물, 스승, 그리고 공동의 기억.',
        samples: ['우리 강 되살리기', '모든 아이에게 선생님을'],
        moreCount: '+ 사라지는 언어 살리기 & 마을 진료소',
        wishes: [
          {
            id: 'fix-my-river',
            title: '우리 강 되살리기',
            honesty: '머지않아 가능',
            honestyNote: '센서는 오염원을 바로 찾지만 강을 되살리려면 상·하류 주민의 합의가 필요합니다.',
            beatSummary: '센서가 모든 비밀 배관을 짚어냅니다—하지만 위아래 마을이 양보에 합의할 때까지 물은 맑아지지 않습니다.'
          },
          {
            title: '모든 아이를 위한 배움의 길잡이',
            honesty: '머지않아 가능',
            honestyNote: '디지털 튜터가 많은 학생을 돕고 있으나 사람 스승과 학교 공동체는 대체할 수 없습니다.',
            beatSummary: '집에서 아이들마다 척척 배웁니다—어른들이 이웃끼리 서로 가르치던 풍경이 사라진 뒤를 묻기 전까지는.'
          }
        ]
      }
    ]
  },

  beats: {
    heading: '모든 도약에는 네 순간이 있습니다',
    items: [
      { key: '경이', desc: '바람이 현실로 옵니다.' },
      { key: '흔들림', desc: '작은 빈틈이 어긋납니다.' },
      { key: '무게', desc: '무엇이 중요한지 드러납니다.' },
      { key: '길', desc: '사람이 여전히 할 수 있는 일을 봅니다.' }
    ],
    footerLine: '모든 위대한 도약에는 준비된 세상이 필요합니다.'
  },

  lights: {
    heading: '다섯 개 등불로 보는 나의 준비도',
    items: [
      { key: '명료함', meaning: '내가 무엇을 원하는지 분명히 아나요?' },
      { key: '선견지명', meaning: '부작용까지 함께 떠올려 보았나요?' },
      { key: '공정함', meaning: '그 선택에 다른 사람도 포함되었나요?' },
      { key: '지혜', meaning: '무엇을 사람의 몫으로 남기고 싶나요?' },
      { key: '실행력', meaning: '현실에서 실제로 감당할 수 있나요?' }
    ],
    emptyState: '첫 번째 도약을 선택해 첫 등불을 밝혀 보세요.',
    lowLightNote: '흐린 불빛은 실패가 아니라 앞으로 채워 갈 방향입니다.',
    trailNote: '3개를 마치면 공유 가능한 여정 카드, 5개를 마치면 그림자 지도가 열립니다.'
  },

  country: {
    heading: '우리 나라는 이 도약을 받아낼 수 있을까요?',
    subhead: '나라를 골라 이미 갖춘 기반과 아직 빈 자리를 확인하세요.',
    searchPlaceholder: '148개국 이름 검색...',
    searchLabel: '나라 이름으로 검색',
    selectLabel: '국가 선택',
    checklistLabel: '순위가 아닌 단순한 점검표',
    unratedBadge: '39개국 심층 지수에는 아직 미포함',
    unratedHelpCta: '자국 데이터 보완에 참여하기',
    openCountryCta: '국가 상세 페이지 열기',
    openLabCta: '실험실에서 전환 시나리오 더 보기',
    techReadingLabel: '기술 해설',
    benchmarkBadge: '39개국 기준',
    autoDetectedBadge: '자동 감지',
    benchmarkGroupTpl: '기준 평가국 ({count})',
    coverageGroupTpl: '데이터 범위 감사 ({count})',
    partialDataSuffix: '일부 데이터',
    runsOfflineLabel: '오프라인 지속',
    catchesLabel: '수용 여력',
    safeguardsReadyLabel: '갖춘 안전장치',
    ofFiveTpl: '5개 중 {count}개',
    catchStates: { easily: '여유 있음', effort: '노력 필요', struggles: '버거움' },
    safeguardPills: ['72시간 오프라인', '전력·통신망', '사실 판별력', '공공 규칙', '생계 완충'],
    detailsSummaryTpl: '{country}의 5가지 안전장치와 핵심 병목 보기',
    mainConstraintLabel: '핵심 제약:',
    checkingBaseline: '국가 기본 데이터 확인 중...',
    neverGuessedNote: '추측으로 채우지 않음',
    countryHookTpl: '«{title}»을 받아들이기 위해 {country}는 5가지 중 {count}가지를 갖추고 있습니다.'
  },

  episode: {
    heading: '이번 주 토토와 함께',
    episodeLabel: '에피소드 1',
    badge: '파일럿 에피소드 1 · 제작 중',
    title: '첫 번째 도약',
    synopsis: '항구에 새벽이 옵니다. 야간 근무 중인 간호사 미라가 도시의 첫 도약을 고릅니다. 모든 병상이 낫습니다—이내 복도에는 기계가 미리 정해주지 않은 질문이 울립니다. 내일 누구부터 들어오는가?',
    voteNote: '3분 대화형 이야기와 공개 투표는 4단계에서 열립니다.',
    recapTitle: '금요 요약 받기',
    recapBody: '주간 형식을 정하기 전에 세계 각지 독자 의견을 듣고 있습니다. 스팸은 없습니다.',
    recapStatus: '독자 선호가 정리되면 채널이 열립니다.'
  },

  wishWall: {
    heading: '세상이 바라는 것',
    themes: ['건강', '배움', '기후', '존엄', '경이', '진실'],
    emptyHeadline: '첫 20개의 익명 참여가 모이면 «세상이 바라는 것» 벽이 열립니다.',
    emptyBody: '선택은 기본적으로 내 브라우저에만 남습니다. 최소 20명의 실제 참여가 모일 때만 공통 주제가 표시됩니다.',
    cta: '도약 하나 고르기'
  },

  wisher: {
    heading: '훌륭한 도약일수록 준비된 세상이 필요한 이유',
    cards: [
      {
        title: '속도 격차',
        body: '기계는 사람이 눈을 깜빡이기보다 수천 배 빠르게 움직입니다. 지켜보기만 해서는 늦으며, 도착 전에 점검 장치가 들어가 있어야 합니다.',
        techHint: '현재 사람 한 줄 검토 대비 약 ~3,200× 빠름.'
      },
      {
        title: '의존성',
        body: '더 많이 맡길수록 멈추기가 어려워집니다. 병원, 전기, 식량은 끄기 힘든 망 위에서 돕습니다. 작은 종이 비상 사본이 큰 가치를 가집니다.',
        techHint: '전력망, 식량 물류 및 병원 단절 내성으로 측정.'
      }
    ],
    closingLine: '두려움이 아니라, 맞이할 준비에 관한 이야기입니다.'
  },

  deeper: {
    eyebrow: '개방형 실증 연구 기반',
    heading: '이야기 뒤의 과학 연구',
    subhead: '위의 모든 비유는 동료 심사 측정, 공개 코드, 한 번의 탭으로 열리는 국가 데이터에 기반합니다.',
    statNations: '심층 평가 국가',
    statCompleteness: '관측 지표 충실도',
    statScenarios: '모델링된 전환 위험',
    statSignals: '모니터링 중인 조기 신호',
    primaryCta: '실험실에서 스트레스 테스트 해보기',
    citationSummary: '인용 정보 및 공개 데이터 보증 (DOI 10.5281/zenodo.23441742)',
    releaseNote: '미리보기: 39개국 평가(평균 53.8 / 100), 관측 완전성 96.5%(663개 항목 중 640개 실측).',
    cards: [
      { title: '실험실 열기', desc: '맞춤 스트레스 테스트, 시간 슬라이더 및 국가 회복탄력성 시나리오.', href: '/sandbox/', tag: '대화형 랩' },
      { title: '39개국 지수', desc: '인터랙티브 3D 지구본, 전체 순위표 및 국가별 보고서.', href: '/countries/', tag: '국가 지수' },
      { title: '실시간 맥박', desc: '전조 모니터 (8.44 / 10)와 14개 실시간 지표.', href: '/seismograph/', tag: '실시간 추적' },
      { title: '시나리오 아틀라스', desc: '모든 도약 뒤에 숨은 26개 AI 전환 경로 탐구.', href: '/scenarios/', tag: '아틀라스' },
      { title: '연구 모노그래프', desc: '수리적 증명을 담은 35분 분량의 동료 심사 논문.', href: '/monograph/', tag: '35분 읽기' },
      {
        title: '방법론·데이터·범위',
        desc: '공식 확인, 공개 CSV 내려받기 및 미평가 국가 공백 점검.',
        href: '/methodology/',
        extraLinks: [
          { label: '방법론', href: '/methodology/' },
          { label: '데이터 다운로드', href: '/data/' },
          { label: '글로벌 범위 감사', href: '/coverage/' }
        ],
        tag: '오픈 사이언스'
      }
    ]
  },

  player: {
    featuredLabel: '대표 도약 체험 (~60초 인터랙티브)',
    doorsBadge: '4막 대화형 플레이어',
    playBtn: '이 도약 체험하기',
    playedBadge: '완료됨',
    previewOnlyNote: '초기 미리보기 — 전체 대본은 다음 단계에서 열립니다',
    stepLabels: ['1. 경이', '2. 흔들림', '3. 무게', '4. 길'],
    backToDoors: '5개 영역 전체 보기',
    draftTag: '검토 중인 초안',
    honestyPrefix: '현실성 점검:',
    foresightLead: '선택형 미리보기 질문 (선견지명 등불이 켜집니다):',
    foresightQuestion: '토토가 걸림돌을 보여주기 전에—어디가 먼저 어긋날 것 같나요?',
    foresightSkip: '바로 흔들림 보기',
    foresightOptions: [
      '아무도 미리 적어두지 않은 예외 규칙',
      '사람들이 스스로 확인하는 습관을 잃음',
      '불평등한 접근 또는 숨은 통제',
      '바로 다음 단계로 건너뛰기'
    ],
    toWobbleBtn: '다음에 무슨 일이 생길지 보기',
    toWeightBtn: '멈춰서 무게 재어보기',
    weightLead: '여기서 가장 신경 쓰이는 점은...',
    toWayBtn: '인간의 길 보기',
    wayActionTitle: '생활 속 구체적인 한 걸음',
    pledgeBtn: '이 인간적 습관을 지키겠습니다',
    pledgeDone: '이 기기에 다짐이 기록됨',
    closingLine: '모든 위대한 도약에는 준비된 세상이 필요합니다.',
    realityTitle: '현실성 측정기',
    realityScales: { imagination: '상상 단계', possibleSoon: '머지않아 가능', realToday: '오늘 일부 현실' },
    realityReviewed: '최근 검토',
    realitySource: '출처',
    shadowTitle: '이 도약의 배경 (시나리오 아틀라스)',
    nextWishBtn: '다른 도약 체험하기',
    countryHookPrefix: '국가 준비도 연결:',
    countryHookUnset: '아래에서 나라를 골라 5가지 안전장치 중 몇 개가 있는지 확인하세요.',
    animPlay: '재생',
    animPause: '일시정지',
    animReplay: '다시',
    transcriptBtn: '장면 대본',
    durationBadge: '~60초 · 4막',
    trailSectionTitle: '나의 준비 여정과 그림자 지도',
    trailLocked: '서로 다른 3가지 도약을 완료하면 공유용 여정 카드가 열립니다 ({done}/3 완료).',
    trailUnlockedBadge: '여정 카드 잠금 해제 (3개 이상)',
    shadowLocked: '서로 다른 5가지 도약을 완료하면 개인 그림자 지도가 열립니다 ({done}/5 완료).',
    shadowUnlockedBadge: '그림자 지도 잠금 해제 (5개 이상)',
    downloadLandscape: '여정 카드 저장 (1200×630 PNG)',
    downloadStory: '모바일 스토리 저장 (1080×1920 PNG)',
    downloadShadowPng: '그림자 지도 저장 (1200×630 PNG)',
    downloadSvg: '벡터 저장 (.svg)',
    lightsLegend: '빛의 밝기(0–3)는 내 브라우저에만 저장되며 점수 순위를 매기지 않습니다.',
    countryCapabilityNote: '연결된 국가 ({name}): 5개 중 {count}개 안전장치가 실행력 등불에 힘을 보탭니다.',
    countryCapabilityUnset: '실행력은 현재 개인 습관만 반영합니다. 아래에서 나라를 선택해 실제 국가 데이터를 연결해 보세요.',
    countryCapabilityUnrated: '선택한 나라({name})는 아직 39개국 지수 외 국가여서 개인 습관이 실행력을 이끕니다.',
    shadows: { Control: '통제', Dependence: '의존', Power: '권력', Truth: '진실', Speed: '속도' },
    trails: {
      Verifier: { name: '검증하는 사람', note: '빠른 답을 믿기 전 먼저 확인하며 검증자를 누가 검증하는지 묻습니다.' },
      Neighbour: { name: '이웃을 살피는 사람', note: '누가 뒤처지는지 살피고 공정함을 중심에 둡니다.' },
      Builder: { name: '토대를 세우는 사람', note: '강력한 도구 옆에 오프라인 백업과 공동체 대안을 함께 둡니다.' },
      Keeper: { name: '손길을 지키는 사람', note: '기계의 속도 속에서도 인간의 판단, 기억, 살아있는 기술을 보존합니다.' }
    }
  },

  footerUi: {
    brandTitle: '인류 초지능 대비 지수 (HSRI)',
    tagline: '오픈 연구 컨소시엄 · 영구 DOI: 10.5281/zenodo.23441742',
    brandDesc: '클라우드 자동화 시스템이 멈출 때 인간의 판단력, 제도적 대비, 사회의 자립 능력을 측정하는 공개 실증 연구.',
    researchHeading: '연구와 탐색',
    scienceHeading: '오픈 사이언스',
    researchLinks: ['실험실 열기', '39개국 지수', '실시간 맥박', '26개 시나리오 아틀라스', '연구 모노그래프'],
    scienceLinks: ['과학적 방법론', '데이터 다운로드', '범위 감사', '금요 요약', '한계 및 고지'],
    contactHeading: '연구 문의',
    contactDesc: '기관 브리핑, 데이터 검증 또는 학술 협력 문의:',
    langHeading: '언어 (전 세계 14개 에디션):',
    rtlActiveNotice: '오른쪽에서 왼쪽(RTL) 레이아웃 활성.',
    communityReviewNotice: '원어민 커뮤니티 검토를 환영합니다.',
    privacyLink: '개인정보',
    languagesLink: '언어',
    totoLink: '토토',
    recapLink: '금요 요약',
    doiLink: '영구 DOI (Zenodo)',
    disclaimerLink: '통계 유의사항',
    licenseLink: 'CC BY-SA 4.0 라이선스',
    copyright: '© 2026 HSRI 연구 컨소시엄. 공개 연구 라이선스 배포.'
  },

  heritageUi: {
    localHorizonTag: '문화적 지평 · {country}',
    livingBadge: '살아있는 전통',
    historicalBadge: '역사적 맥락',
    seeGlobalBtn: '글로벌 예시 보기',
    seeLocalBtn: '{country} 전통 보기',
    livesInOtherDoor: '{country}의 문화 지평은 «{door}»에 있습니다',
    noLocalYet: '{country} 고유 전통이 아직 추가되지 않았습니다 — 글로벌 도약을 탐색해 보세요.',
    readArchiveLink: '출처 및 문화 자료집',
    reviewOpenNote: '2곳 이상 인용 출처 · 원어민 검토 환영',
    weightBindingTitle: '{country} 실제 전달 기반 점검',
    weightRatedInPlace: '갖춰짐',
    weightRatedGap: '취약점 관측됨',
    weightContextNote: '{country}는 부분 추적 중입니다 ({region}) — {observed}',
    weightNoCountry: '아래에서 나라를 선택해 실제 국가 데이터와 대조해 보세요.',
    wayTestCountryCta: '국가 점검에서 {country} 안전장치 테스트',
    trailStampLabel: '탐험한 문화 지평: {count}',
    autoDetectedHint: '자동 추천 하늘 · 국가 변경 가능',
    perspectiveBadge: '시각 · {country}',
    resetGlobalBtn: '글로벌 보기',
    countryHeadingTradition: '{country}의 시각에서: {tradition}',
    countryHeadingGlobal: '{country}의 시각에서 도약 시험하기',
    countrySubhead: 'AI 도약이 {country}의 현실과 만났을 때 무엇이 벌어지는지 살펴봅니다.',
    flowWonder: '바람이 오고',
    flowWobble: '지역 부담',
    flowCatch: '{country} 수용력',
    otherDomainsLabel: '{country} 시각으로 5개 영역 전체 탐색:',
    otherTraditionsLabel: '세계 여러 전통 비교하기:',
    allTraditionsBtn: '전체 {count}개',
    plannedNextLabel: '다음 예정:',
    auditChip: '감사',
    domainsTablistAria: '다섯 개 도약 영역',
    traditionsAria: '세계의 문화 전통',
    lightsCountryHeading: '{country}의 5가지 준비 등불',
    lightsHumanGroup: '당신의 선택',
    lightsCountryGroup: '{country} 역량',
    countryCatchHeading: '{country}는 버틸 수 있을까?',
    traditionTestsLabel: '전통 렌즈:',
    coverageObservedLabel: '관측된 안전장치',
    coverageMissingLabel: '미측정 공백 (추정 금지)'
  }
};
