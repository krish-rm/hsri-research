import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DRAFT15_ABS_PATH = path.join(__dirname, 'src/data/wishes.draft15.json').replace(/\\/g, '/');

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

function hsriDraftFlagsPlugin() {
  let isServe = false;
  return {
    name: 'hsri-draft-flags',
    config(_config, { command }) {
      isServe = command === 'serve';
      const showDraftBadge = isServe || process.env.PUBLIC_SHOW_DRAFTS === 'true';
      const includeDev15 = isServe || process.env.PUBLIC_SHOW_DEV_BREAKTHROUGHS === 'true';
      return {
        define: {
          __HSRI_SHOW_DRAFTS__: JSON.stringify(showDraftBadge),
          __HSRI_INCLUDE_DEV15__: JSON.stringify(includeDev15),
        },
      };
    },
    resolveId(id) {
      if (id === 'virtual:hsri-dev15') return '\0virtual:hsri-dev15';
    },
    load(id) {
      if (id === '\0virtual:hsri-dev15') {
        const includeDev15 = isServe || process.env.PUBLIC_SHOW_DEV_BREAKTHROUGHS === 'true';
        if (includeDev15) {
          return `import draft15 from ${JSON.stringify(DRAFT15_ABS_PATH)};\nexport default draft15;\n`;
        }
        return 'export default [];\n';
      }
    },
  };
}

export default defineConfig({
  site: 'https://humanityreadiness.org',
  base: '/',
  integrations: [interactDirectiveIntegration, svelte(), sitemap()],
  vite: {
    plugins: [hsriDraftFlagsPlugin()],
  },
  output: 'static',
  build: {
    format: 'directory',
    inlineStylesheets: 'never',
  },
});
