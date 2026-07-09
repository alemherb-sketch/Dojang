import axios from 'axios';

// Base URL of the Django backend.
// Defaults to the deployed Railway backend so the PWA works out of the box.
// Override for local backend development by creating frontend/.env.local with:
//   VITE_API_URL=http://127.0.0.1:8000
export const API_BASE =
  import.meta.env.VITE_API_URL || 'https://web-production-c2ca0.up.railway.app';

const api = axios.create({ baseURL: API_BASE });

export default api;
