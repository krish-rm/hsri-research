<script lang="ts">
  // Footer navigation items
  const footerNav = {
    'Project': [
      { name: 'About', href: '/about' },
      { name: 'Methodology', href: '/methodology' },
      { name: 'Data Sources', href: '/data-sources' },
      { name: 'Limitations', href: '/limitations' },
    ],
    'Resources': [
      { name: 'Country Profiles', href: '/countries' },
      { name: 'Timeline Explorer', href: '/timeline' },
      { name: 'Comparison Tool', href: '/compare' },
      { name: 'Downloads', href: '/downloads' },
    ],
    'Research': [
      { name: 'Papers', href: '/papers' },
      { name: 'Pre-registration', href: '/preregistration' },
      { name: 'Datasets', href: '/datasets' },
      { name: 'Code', href: '/code' },
    ],
    'Community': [
      { name: 'Contribute', href: '/contribute' },
      { name: 'Blog', href: '/blog' },
      { name: 'Forum', href: '/forum' },
      { name: 'Newsletter', href: '/newsletter' },
    ]
  };

  // Social links
  const socialLinks = [
    { name: 'GitHub', href: 'https://github.com/krish-rm/hsri-research', icon: 'github' },
    { name: 'Twitter', href: 'https://twitter.com/hsri_research', icon: 'twitter' },
    { name: 'Email', href: 'mailto:contact@hsri-research.org', icon: 'email' },
  ];
</script>

<footer class="hsri-footer">
  <div class="container">
    <div class="footer-content">
      <!-- Brand section -->
      <div class="footer-brand">
        <div class="brand-header">
          <svg class="logo" width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="19" stroke="var(--primary-color)" stroke-width="2"/>
            <path d="M20 5 L15 15 L5 20 L15 25 L20 35 L25 25 L35 20 L25 15 Z" fill="var(--primary-color)" opacity="0.8"/>
            <circle cx="20" cy="20" r="8" fill="white"/>
          </svg>
          <div>
            <h3 class="footer-title">Human Superintelligence Readiness Index</h3>
            <p class="footer-tagline">v0.1 Public Preview</p>
          </div>
        </div>
        <p class="footer-description">
          A research feasibility project investigating whether human psychological and behavioral readiness for increasingly capable AI can be scientifically measured.
        </p>
      </div>

      <!-- Navigation sections -->
      <div class="footer-nav">
        {#each Object.entries(footerNav) as [section, links]}
          <div class="nav-section">
            <h4 class="nav-title">{section}</h4>
            <ul class="nav-links">
              {#each links as link}
                <li><a href={link.href} class="nav-link">{link.name}</a></li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>

      <!-- Contact section -->
      <div class="footer-contact">
        <h4 class="contact-title">Stay Updated</h4>
        <p class="contact-description">
          Subscribe to our newsletter for updates on research findings and methodology improvements.
        </p>
        <form class="newsletter-form" on:submit|preventDefault>
          <input
            type="email"
            placeholder="Enter your email"
            class="newsletter-input"
            required
          />
          <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>

        <!-- Social links -->
        <div class="social-links">
          {#each socialLinks as link}
            <a href={link.href} class="social-link" target="_blank" rel="noopener noreferrer" aria-label={link.name}>
              <span class="sr-only">{link.name}</span>
              {#if link.icon === 'github'}
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              {:else if link.icon === 'twitter'}
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              {:else if link.icon === 'email'}
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 5.457v13.909c0 .9-.7 1.636-1.564 1.636H5.464c-.864 0-1.564-.736-1.564-1.636V5.457c0-.9.7-1.636 1.564-1.636h16.972c.864 0 1.564.736 1.564 1.636M23.188 14.5V7.865l-7.821 5.67 7.821 1.001M5.312 7.865v6.635l7.821-1.001L5.312 7.865m.299 8.758l7.914 1.013 7.914-1.013v-1.635H5.611v1.635"/>
                </svg>
              {/if}
            </a>
          {/each}
        </div>
      </div>
    </div>

    <!-- Bottom section -->
    <div class="footer-bottom">
      <div class="footer-links">
        <a href="/disclaimer" class="footer-link">Disclaimer</a>
        <a href="/ethics" class="footer-link">Ethics Statement</a>
        <a href="/privacy" class="footer-link">Privacy Policy</a>
        <a href="/terms" class="footer-link">Terms of Use</a>
      </div>

      <div class="copyright">
        <p>&copy; 2026 HSRI Research. Licensed under CC BY-SA 4.0. <a href="/license">View license details</a>.</p>
      </div>
    </div>
  </div>
</footer>

<style>
  .hsri-footer {
    background-color: var(--surface-color);
    color: var(--text-primary);
    margin-top: var(--spacing-2xl);
    padding: var(--spacing-2xl) 0 0;
  }

  .footer-content {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: var(--spacing-2xl);
    margin-bottom: var(--spacing-2xl);
  }

  .footer-brand {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .brand-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .footer-title {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--primary-color);
  }

  .footer-tagline {
    margin: 0;
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  .footer-description {
    font-size: var(--font-size-sm);
    line-height: 1.5;
    color: var(--text-secondary);
  }

  .footer-nav {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-xl);
  }

  .nav-section h4 {
    margin: 0 0 var(--spacing-sm);
    font-size: var(--font-size-base);
    font-weight: 600;
    color: var(--text-primary);
  }

  .nav-links {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .nav-links li {
    margin-bottom: var(--spacing-xs);
  }

  .nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: var(--font-size-sm);
    transition: color 0.2s;
  }

  .nav-link:hover {
    color: var(--accent-color);
  }

  .footer-contact {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .contact-title {
    margin: 0;
    font-size: var(--font-size-base);
    font-weight: 600;
    color: var(--text-primary);
  }

  .contact-description {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .newsletter-form {
    display: flex;
    gap: var(--spacing-sm);
  }

  .newsletter-input {
    flex: 1;
    padding: var(--spacing-sm);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
  }

  .newsletter-input:focus {
    outline: none;
    border-color: var(--accent-color);
  }

  .social-links {
    display: flex;
    gap: var(--spacing-md);
    margin-top: var(--spacing-md);
  }

  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 50%;
    color: var(--text-secondary);
    transition: all 0.2s;
  }

  .social-link:hover {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
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

  .footer-bottom {
    border-top: 1px solid var(--border-color);
    padding-top: var(--spacing-xl);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--spacing-md);
  }

  .footer-links {
    display: flex;
    gap: var(--spacing-lg);
  }

  .footer-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: var(--font-size-sm);
    transition: color 0.2s;
  }

  .footer-link:hover {
    color: var(--accent-color);
  }

  .copyright {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .copyright a {
    color: var(--text-secondary);
    text-decoration: underline;
  }

  /* Responsive styles */
  @media (max-width: 1024px) {
    .footer-content {
      grid-template-columns: 1fr;
      gap: var(--spacing-xl);
    }

    .footer-nav {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 640px) {
    .footer-nav {
      grid-template-columns: 1fr;
    }

    .footer-bottom {
      flex-direction: column;
      text-align: center;
    }

    .footer-links {
      flex-wrap: wrap;
      justify-content: center;
      gap: var(--spacing-md);
    }

    .newsletter-form {
      flex-direction: column;
    }
  }
</style>