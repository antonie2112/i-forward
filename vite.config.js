import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg', 'logo.png'],
      manifest: {
        name: 'I.Forward - A Sales Hub',
        short_name: 'I.Forward',
        description: 'Elite Sales Enablement Hub for Ecolab Institutional',
        theme_color: '#0ea5e9',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: 'logo.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'logo.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'logo.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any maskable'
          }
        ]
      }
    })
  ],
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
      '/system-assets': {
        target: 'https://ecolabwallchart.azurewebsites.net',
        changeOrigin: true,
        secure: false, // Bypass potential SSL verification issues on mobile
        rewrite: (path) => path.replace(/^\/system-assets/, '')
      }
    }
  }
});
