import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

export default defineConfig({
  integrations: [svelte()],
  output: 'static',
  build: {
    format: 'directory',
  },
  site: 'https://krish-rm.github.io',
  base: '/hsri-research',
});