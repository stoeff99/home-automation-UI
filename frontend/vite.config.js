// vite.config.js (CommonJS, works in Node 18 CJS)

const { defineConfig } = require("vite");
const react = require("@vitejs/plugin-react");

// Export Vite config
module.exports = defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        // Use Docker service name for backend
        target: "http://host.docker.internal:5000",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist",
  },
});
