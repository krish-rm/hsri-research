import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

export default defineConfig({
  integrations: [svelte()],
  output: 'static',
  build: {
    format: 'directory',
  },
  site: 'https://humanreadinessindex.org',
  base: '/',
});
