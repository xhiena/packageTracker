import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (token, newPassword) => api.post('/auth/reset-password', { token, password: newPassword }),
};

// Packages API
export const packagesAPI = {
  getAll: () => api.get('/packages'),
  add: (data) => api.post('/packages', data),
  delete: (id) => api.delete(`/packages/${id}`),
  update: (id, data) => api.put(`/packages/${id}`, data),
};

// Carriers API
export const carriersAPI = {
  getAll: () => api.get('/carriers'),
};

export default api;
