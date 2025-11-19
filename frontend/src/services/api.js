import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
  register: (userData) => api.post('/api/auth/register', userData),
  login: (credentials) => {
    // Convert to form data for FastAPI OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  },
  requestPasswordReset: (email) => api.post('/api/auth/password-reset-request', { email }),
  resetPassword: (token, newPassword) => api.post('/api/auth/password-reset', { token, new_password: newPassword }),
};

// Packages API
export const packagesAPI = {
  getAll: () => api.get('/api/packages/'),
  add: (packageData) => api.post('/api/packages/', packageData),
  get: (id) => api.get(`/api/packages/${id}`),
  update: (id, data) => api.put(`/api/packages/${id}`, data),
  delete: (id) => api.delete(`/api/packages/${id}`),
  track: (id) => api.get(`/api/packages/${id}/track`),
};

// Carriers API
export const carriersAPI = {
  getAll: () => api.get('/api/packages/carriers'),
};

export default api;
