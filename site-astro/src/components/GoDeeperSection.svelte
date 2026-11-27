<script lang="ts">
  import { dict } from '../i18n/store';

  export let base = '';
</script>

<section id="go-deeper" class="explore-strip">
  <div class="story-container">
    <div class="es-head">
      <h2>{$dict.deeper.heading}</h2>
      <p>{$dict.deeper.subhead}</p>
    </div>

    <nav class="es-links" aria-label="Research instruments and story guides">
      <a href={`${base}/toto/`} class="es-pill">Guide: Toto &amp; How It Works &rarr;</a>
      <a href={`${base}/seismograph/`} class="es-pill">Live AI Pace &rarr;</a>
      <a href={`${base}/countries/`} class="es-pill">39-Country Index &rarr;</a>
      <a href={`${base}/sandbox/`} class="es-pill">Interactive Lab &rarr;</a>
      <a href={`${base}/scenarios/`} class="es-pill">26 Scenarios &rarr;</a>
      <a href={`${base}/monograph/`} class="es-pill">The Monograph &rarr;</a>
    </nav>

    <div class="es-open-science">
      <a href={`${base}/methodology/`}>Methodology</a>
      <span>&middot;</span>
      <a href={`${base}/data/`}>Data &amp; CSVs</a>
      <span>&middot;</span>
      <a href={`${base}/coverage/`}>Global Coverage Audit</a>
      <span>&middot;</span>
      <a href={`${base}/privacy/`}>Privacy</a>
      <span>&middot;</span>
      <a href="https://doi.org/10.5281/zenodo.23441742" target="_blank" rel="noopener noreferrer">
        DOI 10.5281/zenodo.23441742
      </a>
    </div>
  </div>
</section>

<style>
  .explore-strip {
    contain: layout style;
    padding: 1.5rem 0;
    background: var(--bg-surface-sunken);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
  }

  .story-container {
    max-width: 1020px;
    margin: 0 auto;
    padding: 0 1.15rem;
    text-align: center;
  }

  .es-head h2 {
    margin: 0 0 0.25rem;
    font-size: clamp(1.2rem, 2.2vw, 1.5rem);
    font-weight: 800;
    color: var(--text-primary);
  }

  .es-head p {
    margin: 0 auto 0.9rem;
    max-width: 620px;
    font-size: 0.88rem;
    color: var(--text-secondary);
  }

  .es-links {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.45rem;
    margin-bottom: 0.85rem;
  }

  .es-pill {
    display: inline-flex;
    align-items: center;
    min-height: 38px;
    padding: 0.42rem 0.85rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    color: var(--text-primary);
    font-size: 0.82rem;
    font-weight: 700;
    text-decoration: none;
  }

  .es-pill:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .es-open-science {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.35rem 0.55rem;
    font-size: 0.78rem;
    color: var(--text-muted);
  }

  .es-open-science a {
    color: var(--accent-primary);
    font-weight: 600;
    text-decoration: none;
  }

  .es-open-science a:hover {
    text-decoration: underline;
  }
</style>
