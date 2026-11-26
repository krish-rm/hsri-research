import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';

const interactDirectiveIntegration = {
  name: 'hr-interact-directive',
  hooks: {
    'astro:config:setup': ({ addClientDirective }) => {
      addClientDirective({
        name: 'interact',
        entrypoint: './src/directives/interact.mjs',
      });
    },
  },
};

export default defineConfig({
  site: 'https://humanityreadiness.org',
  base: '/',
  integrations: [interactDirectiveIntegration, svelte(), sitemap()],
  output: 'static',
  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
  },
});
