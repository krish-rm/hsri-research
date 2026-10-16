<script lang="ts">
  let expandedCard: number | null = null;

  function toggleExpand(index: number) {
    expandedCard = expandedCard === index ? null : index;
  }

  const dilemmas = [
    {
      id: "gorilla",
      number: "01",
      tag: "COGNITIVE ASYMMETRY",
      title: "The Slower-Species Dilemma",
      question: "Can a slower mind permanently govern a faster intelligence?",
      plainEnglish: "Gorillas did not lose control of their habitat through war or formal negotiation; they lost control because humans reached a cognitive threshold that allowed them to reshape the physical environment faster than gorillas could comprehend. When an artificial intelligence thinks 1,000x faster than biological humans, 'human-in-the-loop' supervision becomes a dangerous psychological illusion.",
      groundingTitle: "Formal Grounding & Literature Evidence",
      groundingText: "Nick Bostrom's Gorilla Problem (Superintelligence, Ch. 1) & Roman Yampolskiy's Turing Undecidability Theorem. Proves that an entity with computational depth C_ASI >> C_human cannot be verified before execution by a slower observer without running at machine speeds.",
      metricBadge: "Verification Wedge: 3,200x",
      icon: "🦍"
    },
    {
      id: "warfare",
      number: "02",
      tag: "MACHINE-SPEED OFFENSE",
      title: "Machine-Speed Asymmetric Warfare",
      question: "What happens when digital weapons move faster than human biological reflexes?",
      plainEnglish: "Autonomous cyber suites can discover, chain, and execute zero-day exploits across electrical grids, water treatment facilities, and financial networks in milliseconds. Concurrently, generative biological tools eliminate the graduate-level lab barriers to designing immune-evasive pathogens. Defense cannot keep pace with machine-speed digital offense.",
      groundingTitle: "Formal Grounding & Literature Evidence",
      groundingText: "Dan Hendrycks (CAIS, Catastrophic AI Risks), Kevin Esvelt (MIT Sculpting Evolution, Generative Biology), and Paul Scharre (CNAS, Army of None). Proves that compressed military OODA loops force humans out of fire-control loops, risking automated sub-second flash-war escalation.",
      metricBadge: "Exploit Latency: < 60s",
      icon: "⚡"
    },
    {
      id: "atrophy",
      number: "03",
      tag: "HUMAN DESKILLING",
      title: "Cognitive Atrophy & Epistemic Collapse",
      question: "If algorithms solve every problem, what happens to human discernment?",
      plainEnglish: "When humans rely on AI co-pilots for coding, legal analysis, medical diagnosis, and crisis triage, their own tacit troubleshooting intuition atrophies. Furthermore, when generative models flood the information commons with hyper-realistic synthetic media, objective ground truth dissolves, paralyzing societal consensus during existential emergencies.",
      groundingTitle: "Formal Grounding & Literature Evidence",
      groundingText: "Lisanne Bainbridge's Ironies of Automation (1983) 5 ironies: skill atrophy, 30-min Mackworth vigilance decrement, and troubleshooting Catch-22. Empirically validated in HSRI EXP-01–09 Psychometric Battery (ΔR² = +0.4870) and Paul Christiano's 'Going Out with a Whimper' model.",
      metricBadge: "Mackworth Limit: 30 Mins",
      icon: "🧠"
    },
    {
      id: "abundance",
      number: "04",
      tag: "SYSTEMIC FRAGILITY",
      title: "The Abundance Trap",
      question: "Why does hyper-efficiency make civilizational collapse instantaneous?",
      plainEnglish: "Superintelligence offers god-like constructive power: instant software synthesis, novel materials, and automated logistics. But hyper-efficiency strips away all physical buffers, warehouse inventories, and manual bypasses. When the entire economy is hard-coupled to continuous AI inference, a single disruption causes immediate, non-linear civilizational paralysis.",
      groundingTitle: "Formal Grounding & Literature Evidence",
      groundingText: "Daron Acemoglu & Simon Johnson (2024 Nobel Laureates, Power and Progress) & Nassim Nicholas Taleb's Antifragile. Mathematical proof of Negative Cross-Elasticity (∂P2/∂P4 < 0) and Jensen's inequality in hyper-optimized networks where elimination of slack guarantees catastrophic failure under shock.",
      metricBadge: "Operational Slack: 0.00",
      icon: "🌐"
    },
    {
      id: "blackout",
      number: "05",
      tag: "CIVILIZATIONAL FLOOR",
      title: "The Civilizational Decoupling Floor",
      question: "How many hours does your nation survive if the digital cloud goes dark?",
      plainEnglish: "In an extreme crisis—whether a runaway cyber conflict, physical subsea cable severance, or containment failure—global AI clouds may dark-screen. Modern cities have zero analog food, water, or grid fallback. HSRI measures a nation's Decoupling Half-Life (T_half): the exact duration it can maintain basic human survival in total digital isolation.",
      groundingTitle: "Formal Grounding & Literature Evidence",
      groundingText: "Wassily Leontief's Non-Compensatory Input-Output Economics (Y = min_j(H_j)) and HSRI Pillar 6 Decoupling Simulator. Validated in HSRI Tabletop Console: Singapore T_half = 8h vs Norway T_half > 336h, establishing the Solvency II 99.5% SCR civilizational reinsurance capital charge.",
      metricBadge: "Global Median T_half: 48h",
      icon: "🔌"
    }
  ];
</script>

<div class="dilemmas-container" id="dilemmas">
  <div class="section-intro">
    <span class="eyebrow-pill">FOUNDATIONAL REALITIES</span>
    <h2 class="section-title">The Five Existential Dilemmas</h2>
    <p class="section-desc">
      Superintelligence is not a software upgrade. It is a fundamental phase change in planetary agency. 
      Here are the five civilizational failure modes governing human survival.
    </p>
  </div>

  <div class="dilemma-grid">
    {#each dilemmas as d, i}
      <div class="dilemma-card" class:active={expandedCard === i}>
        <div class="card-top">
          <div class="badge-row">
            <span class="number-tag">{d.number}</span>
            <span class="category-tag">{d.tag}</span>
            <span class="metric-pill">{d.metricBadge}</span>
          </div>
          <div class="card-icon">{d.icon}</div>
        </div>

        <h3 class="card-title">{d.title}</h3>
        <p class="card-question">"{d.question}"</p>
        <p class="card-body">{d.plainEnglish}</p>

        <div class="accordion-wrapper">
          <button 
            type="button" 
            class="accordion-btn" 
            on:click={() => toggleExpand(i)}
            aria-expanded={expandedCard === i}
          >
            <span>{expandedCard === i ? '▲ Hide Academic Grounding' : '▼ View Academic Grounding & Formal Proofs'}</span>
          </button>

          {#if expandedCard === i}
            <div class="accordion-content">
              <div class="grounding-box">
                <div class="grounding-header">{d.groundingTitle}</div>
                <p class="grounding-text">{d.groundingText}</p>
              </div>
            </div>
          {/if}
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .dilemmas-container {
    padding: 3.5rem 0;
  }

  .section-intro {
    text-align: center;
    max-width: 760px;
    margin: 0 auto 2.5rem auto;
  }

  .eyebrow-pill {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #2563eb;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
  }

  .section-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 0 0 0.75rem 0;
  }

  .section-desc {
    font-size: 1.05rem;
    color: #475569;
    line-height: 1.6;
    margin: 0;
  }

  .dilemma-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 1.5rem;
  }

  .dilemma-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.75rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: flex;
    flex-direction: column;
  }

  .dilemma-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.08);
    border-color: #93c5fd;
  }

  .dilemma-card.active {
    border-color: #3b82f6;
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.15);
  }

  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
  }

  .number-tag {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: #2563eb;
    background: #eff6ff;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
  }

  .category-tag {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #475569;
    background: #f1f5f9;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
  }

  .metric-pill {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    color: #0d9488;
    background: #f0fdfa;
    border: 1px solid #ccfbf1;
    padding: 0.15rem 0.45rem;
    border-radius: 6px;
  }

  .card-icon {
    font-size: 1.5rem;
  }

  .card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
  }

  .card-question {
    font-size: 0.95rem;
    font-weight: 600;
    font-style: italic;
    color: #2563eb;
    margin: 0 0 0.85rem 0;
    line-height: 1.4;
  }

  .card-body {
    font-size: 0.925rem;
    color: #334155;
    line-height: 1.6;
    margin: 0 0 1.25rem 0;
    flex-grow: 1;
  }

  .accordion-wrapper {
    margin-top: auto;
    border-top: 1px solid #f1f5f9;
    padding-top: 0.85rem;
  }

  .accordion-btn {
    background: none;
    border: none;
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0.35rem 0;
    text-align: left;
    width: 100%;
    transition: color 0.15s ease;
  }

  .accordion-btn:hover {
    color: #2563eb;
  }

  .accordion-content {
    margin-top: 0.75rem;
    animation: fadeIn 0.2s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .grounding-box {
    background: #f8fafc;
    border-left: 3px solid #3b82f6;
    padding: 0.75rem 0.85rem;
    border-radius: 0 6px 6px 0;
  }

  .grounding-header {
    font-size: 0.75rem;
    font-weight: 700;
    color: #1e40af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }

  .grounding-text {
    font-size: 0.825rem;
    color: #475569;
    line-height: 1.5;
    margin: 0;
    font-family: 'Roboto', sans-serif;
  }

  @media (max-width: 640px) {
    .dilemma-grid {
      grid-template-columns: 1fr;
    }
    .section-title {
      font-size: 1.75rem;
    }
  }
</style>
