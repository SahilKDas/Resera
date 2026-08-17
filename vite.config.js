import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  base: '/Resera/',
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000'
    }
  },
  build: {
    outDir: 'dist/client'
  }
});
