<script lang="ts">
  import { onMount } from 'svelte';
  import { activeLocale, dict, initLocale, setLocale, SUPPORTED_LOCALES, type LocaleKey } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';

  const base = (import.meta.env.BASE_URL || '/hsri-research').replace(/\/$/, '');

  // Curated, localized footer navigation preserving all research routes
  $: footerNav = {
    [$dict.footerUi.researchHeading]: [
      { name: $dict.footerUi.researchLinks[0], href: `${base}/sandbox/` },
      { name: $dict.footerUi.researchLinks[1], href: `${base}/countries/` },
      { name: $dict.footerUi.researchLinks[2], href: `${base}/seismograph/` },
      { name: $dict.footerUi.researchLinks[3], href: `${base}/scenarios/` },
      { name: $dict.footerUi.researchLinks[4], href: `${base}/monograph/` },
    ],
    [$dict.footerUi.scienceHeading]: [
      { name: $dict.footerUi.scienceLinks[0], href: `${base}/methodology/` },
      { name: $dict.footerUi.scienceLinks[1], href: `${base}/data/` },
      { name: $dict.footerUi.scienceLinks[2], href: `${base}/coverage/` },
      { name: $dict.footerUi.scienceLinks[3], href: `${base}/toto/#this-week` },
      { name: $dict.footerUi.scienceLinks[4], href: `${base}/methodology/#limitations` },
    ]
  };

  // Curated channels (zero github links)
  $: socialLinks = [
    { name: 'X / Twitter', href: 'https://twitter.com/hsri_research', icon: 'twitter' },
    { name: $dict.footerUi.contactHeading, href: 'mailto:contact@humanityreadiness.org', icon: 'email' },
  ];

  function chooseLocale(loc: LocaleKey) {
    setLocale(loc);
    trackEvent('locale_switched', { locale: loc });
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new Event('hr:hydrate'));
    }
  }

  onMount(() => {
    initLocale();
  });
</script>

<footer class="hsri-footer">
  <div class="container">
    <div class="footer-content">
      <!-- Brand section -->
      <div class="footer-brand">
        <div class="brand-header">
          <svg class="logo" width="36" height="36" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="19" stroke="var(--primary-color)" stroke-width="2"/>
            <path d="M20 5 L15 15 L5 20 L15 25 L20 35 L25 25 L35 20 L25 15 Z" fill="var(--primary-color)" opacity="0.8"/>
            <circle cx="20" cy="20" r="8" fill="var(--bg-canvas, #fbf7ee)"/>
          </svg>
          <div>
            <h3 class="footer-title">{$dict.footerUi.brandTitle}</h3>
            <p class="footer-tagline">{$dict.footerUi.tagline}</p>
          </div>
        </div>
        <p class="footer-description">
          {$dict.footerUi.brandDesc}
        </p>
      </div>

      <!-- Simplified Navigation sections -->
      <div class="footer-nav">
        {#each Object.entries(footerNav) as [section, links]}
          <div class="nav-section">
            <h4 class="nav-title">{section}</h4>
            <ul class="nav-links">
              {#each links as link}
                <li>
                  <a
                    href={link.href}
                    class="nav-link"
                    target={link.href.startsWith('http') ? '_blank' : undefined}
                    rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                  >
                    {link.name}
                  </a>
                </li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>

      <!-- Inquiries section -->
      <div class="footer-contact">
        <h4 class="contact-title">{$dict.footerUi.contactHeading}</h4>
        <p class="contact-description">
          {$dict.footerUi.contactDesc}
        </p>
        <a href="mailto:contact@humanityreadiness.org" class="contact-link">
          contact@humanityreadiness.org
        </a>

        <!-- Social links -->
        <div class="social-links">
          {#each socialLinks as link}
            <a href={link.href} class="social-link" target={link.href.startsWith('http') ? '_blank' : undefined} rel="noopener noreferrer" aria-label={link.name} title={link.name}>
              <span class="sr-only">{link.name}</span>
              {#if link.icon === 'twitter'}
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              {:else if link.icon === 'email'}
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 5.457v13.909c0 .9-.7 1.636-1.564 1.636H5.464c-.864 0-1.564-.736-1.564-1.636V5.457c0-.9.7-1.636 1.564-1.636h16.972c.864 0 1.564.736 1.564 1.636M23.188 14.5V7.865l-7.821 5.67 7.821 1.001M5.312 7.865v6.635l7.821-1.001L5.312 7.865m.299 8.758l7.914 1.013 7.914-1.013v-1.635H5.611v1.635"/>
                </svg>
              {/if}
            </a>
          {/each}
        </div>
      </div>
    </div>

    <!-- Language & RTL Layout Switcher (14 global editions) -->
    <div id="languages" class="footer-languages" aria-label={$dict.headerUi.langSwitcherAria}>
      <span class="lang-heading">{$dict.footerUi.langHeading}</span>
      {#each SUPPORTED_LOCALES as locOpt}
        <button
          type="button"
          class="lang-btn"
          class:active={$activeLocale === locOpt.code}
          aria-pressed={$activeLocale === locOpt.code}
          title={locOpt.englishName}
          on:click={() => chooseLocale(locOpt.code)}
        >
          {locOpt.label}
        </button>
      {/each}
      {#if $activeLocale === 'ar' || $activeLocale === 'rtl-stub'}
        <span class="rtl-badge" role="status">{$dict.footerUi.rtlActiveNotice}</span>
      {/if}
      {#if $activeLocale !== 'en'}
        <span class="review-badge">{$dict.footerUi.communityReviewNotice}</span>
      {/if}
    </div>

    <!-- Bottom section -->
    <div class="footer-bottom">
      <div class="footer-links">
        <a href={`${base}/privacy/`} class="footer-link">{$dict.footerUi.privacyLink}</a>
        <a href={`${base}/toto/`} class="footer-link">{$dict.footerUi.totoLink}</a>
        <a href="#languages" class="footer-link">{$dict.footerUi.languagesLink}</a>
        <a href={`${base}/#this-week`} class="footer-link">{$dict.footerUi.recapLink}</a>
        <a href="https://doi.org/10.5281/zenodo.23441742" class="footer-link" target="_blank" rel="noopener noreferrer">{$dict.footerUi.doiLink}</a>
        <a href={`${base}/methodology/#limitations`} class="footer-link">{$dict.footerUi.disclaimerLink}</a>
        <a href="https://creativecommons.org/licenses/by-sa/4.0/" class="footer-link" target="_blank" rel="noopener noreferrer">{$dict.footerUi.licenseLink}</a>
      </div>

      <div class="copyright">
        <p>{$dict.footerUi.copyright}</p>
      </div>
    </div>
  </div>
</footer>

<style>
  .hsri-footer {
    background-color: var(--surface-color, #ffffff);
    color: var(--text-primary, #0f172a);
    margin-top: var(--spacing-2xl, 3rem);
    padding: var(--spacing-2xl, 3rem) 0 var(--spacing-xl, 2rem);
    border-top: 1px solid var(--border-color, #e2e8f0);
  }

  .footer-content {
    display: grid;
    grid-template-columns: 1.2fr 1.5fr 1fr;
    gap: var(--spacing-2xl, 3rem);
    margin-bottom: var(--spacing-2xl, 2.5rem);
  }

  .footer-brand {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md, 1rem);
  }

  .brand-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md, 1rem);
  }

  .footer-title {
    margin: 0;
    font-family: var(--font-family-display, 'Boldonse', sans-serif);
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: var(--primary-color, #1e293b);
    line-height: 1.3;
  }

  .footer-tagline {
    margin: 0.25rem 0 0;
    font-size: 0.75rem;
    color: var(--text-secondary, #64748b);
  }

  .footer-description {
    font-size: 0.8125rem;
    line-height: 1.6;
    color: var(--text-secondary, #64748b);
    margin: 0;
  }

  .footer-nav {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-xl, 2rem);
  }

  .nav-section h4 {
    margin: 0 0 var(--spacing-md, 0.875rem);
    font-family: var(--font-family-display, 'Boldonse', sans-serif);
    font-size: 0.90rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-primary, #0f172a);
  }

  .nav-links {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .nav-links li {
    margin-bottom: var(--spacing-sm, 0.5rem);
  }

  .nav-link {
    color: var(--text-secondary, #64748b);
    text-decoration: none;
    font-family: var(--font-family-display, 'Boldonse', sans-serif);
    font-size: 0.88rem;
    letter-spacing: 0.02em;
    transition: color 0.15s ease;
  }

  .nav-link:hover {
    color: var(--accent-color, #2563eb);
  }

  .footer-contact {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .contact-title {
    margin: 0;
    font-family: var(--font-family-display, 'Boldonse', sans-serif);
    font-size: 0.90rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-primary, #0f172a);
  }

  .contact-description {
    font-size: 0.8125rem;
    color: var(--text-secondary, #64748b);
    line-height: 1.5;
    margin: 0;
  }

  .contact-link {
    color: var(--accent-color, #2563eb);
    font-size: 0.8125rem;
    font-weight: 600;
    text-decoration: none;
    word-break: break-all;
    transition: opacity 0.15s;
  }

  .contact-link:hover {
    text-decoration: underline;
  }

  .social-links {
    display: flex;
    gap: var(--spacing-sm, 0.5rem);
    margin-top: 0.5rem;
  }

  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background-color: var(--surface-color, #ffffff);
    border: 1px solid var(--border-color, #e2e8f0);
    border-radius: 50%;
    color: var(--text-secondary, #64748b);
    transition: all 0.2s ease;
  }

  .social-link:hover {
    background-color: var(--accent-color, #2563eb);
    color: #ffffff;
    border-color: var(--accent-color, #2563eb);
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  .footer-languages {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.55rem;
    padding: 0.9rem 0;
    border-top: 1px solid var(--border-color, #e2e8f0);
  }

  .lang-heading {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--text-secondary, #64748b);
  }

  .lang-btn {
    border: 1px solid var(--border-medium, #d4caa8);
    background: var(--bg-surface-elevated, #ffffff);
    color: var(--text-primary, #1e1915);
    border-radius: 9999px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: border-color 0.15s ease, background-color 0.15s ease, color 0.15s ease;
  }

  .lang-btn:hover {
    border-color: var(--accent-primary, #1b6756);
    color: var(--accent-primary, #1b6756);
  }

  .lang-btn.active {
    background: var(--accent-primary, #1b6756);
    border-color: var(--accent-primary, #1b6756);
    color: var(--btn-primary-text, #ffffff);
  }

  .lang-btn.active:hover {
    color: var(--btn-primary-text, #ffffff);
  }

  .rtl-badge {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.7rem;
    color: var(--accent-primary, #1b6756);
    font-weight: 700;
  }

  .review-badge {
    font-size: 0.72rem;
    color: var(--text-secondary, #64748b);
    font-style: italic;
  }

  .footer-bottom {
    border-top: 1px solid var(--border-color, #e2e8f0);
    padding-top: var(--spacing-lg, 1.5rem);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--spacing-md, 1rem);
  }

  .footer-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.25rem;
  }

  .footer-link {
    display: inline-flex;
    align-items: center;
    min-height: 32px;
    padding: 0.2rem 0.25rem;
    color: var(--text-secondary, #64748b);
    text-decoration: none;
    font-size: 0.78rem;
    transition: color 0.15s;
  }

  .footer-link:hover {
    color: var(--accent-color, #2563eb);
  }

  .copyright {
    font-size: 0.75rem;
    color: var(--text-secondary, #64748b);
  }

  .copyright p {
    margin: 0;
  }

  /* Responsive styles */
  @media (max-width: 1024px) {
    .footer-content {
      grid-template-columns: 1fr;
      gap: var(--spacing-xl, 2rem);
    }

    .footer-nav {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 640px) {
    .hsri-footer {
      margin-top: 0;
      padding: 1.5rem 0 1.25rem;
    }

    .footer-content {
      gap: 1.25rem;
      margin-bottom: 1.25rem;
    }

    .footer-nav {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
    }

    .nav-section h4 {
      margin-bottom: 0.45rem;
    }

    .nav-links li {
      margin-bottom: 0.3rem;
    }

    .footer-bottom {
      flex-direction: column;
      text-align: center;
    }

    .footer-links {
      flex-wrap: wrap;
      justify-content: center;
      gap: var(--spacing-md, 1rem);
    }
  }
</style>
