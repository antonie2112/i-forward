import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [],
  build: {
    rollupOptions: {
      input: {
        main: 'index.html'
      }
    }
  },
  server: {
    host: true, // Allow external access via IP
    port: 8080,
    proxy: {
      '/cdn-proxy': {
        target: 'https://ecolabwallchart.azurewebsites.net',
        changeOrigin: true,
        secure: false, // Bypass potential SSL verification issues on mobile
        rewrite: (path) => path.replace(/^\/cdn-proxy/, '')
      }
    }
  }
});
