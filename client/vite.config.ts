import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8080' //tells Vite's development server to proxy requests from /api to your Flask backend running on localhost:8080  
    }
  }
})
