import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (userData) => api.post('/api/auth/register', userData),
  login: (credentials) => api.post('/api/auth/login', credentials, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  requestPasswordReset: (email) => api.post('/api/auth/password-reset-request', { email }),
  resetPassword: (token, newPassword) => api.post('/api/auth/password-reset', { token, new_password: newPassword }),
};

// Packages API
export const packagesAPI = {
  getCarriers: () => api.get('/api/packages/carriers'),
  create: (packageData) => api.post('/api/packages/', packageData),
  list: () => api.get('/api/packages/'),
  get: (id) => api.get(`/api/packages/${id}`),
  update: (id, data) => api.put(`/api/packages/${id}`, data),
  delete: (id) => api.delete(`/api/packages/${id}`),
  track: (id) => api.get(`/api/packages/${id}/track`),
};

export default api;
