import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://humanityreadiness.org',
  base: '/',
  integrations: [svelte(), sitemap()],
  output: 'static',
  build: {
    format: 'directory',
  },
});
