import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// Backend routes the UI calls. In Docker, nginx forwards these;
// in `npm run dev`, Vite forwards them to the FastAPI server.
const BACKEND = process.env.VITE_BACKEND_URL ?? "http://127.0.0.1:8000";
const API_PATHS = [
  "generate", "ai", "skills", "projects", "experience", "education",
  "personal", "summary", "contact", "certifications", "achievements",
  "generated",
];

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: Object.fromEntries(
      API_PATHS.map((p) => [`^/${p}(/|$)`, { target: BACKEND, changeOrigin: true }])
    ),
  },
});