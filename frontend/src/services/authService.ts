import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - her istekte token ekle
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('finoba_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - token yenileme
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;

      try {
        const refreshToken = localStorage.getItem('finoba_refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/auth/refresh/`, {
            refresh_token: refreshToken,
          });
          
          const { access_token } = response.data;
          localStorage.setItem('finoba_token', access_token);
          
          return api(original);
        }
      } catch (refreshError) {
        localStorage.removeItem('finoba_token');
        localStorage.removeItem('finoba_refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/auth/login/', { email, password });
    return response.data;
  },

  async register(userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name: string;
    last_name: string;
  }) {
    console.log('Attempting to register with data:', userData);
    console.log('API_URL:', API_URL);
    
    try {
      // Veriyi açıkça JSON olarak gönder
      const response = await api.post('/auth/register/', userData, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log('Register response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Register error details:', {
        message: error.message,
        responseData: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers
      });
      
      // Backend'den gelen detaylı hata mesajlarını göster
      if (error.response?.data) {
        console.error('Backend validation errors:', error.response.data);
      }
      
      throw error;
    }
  },

  async logout() {
    try {
      await api.post('/auth/logout/');
    } catch (error) {
      // Logout hatası önemli değil
    }
  },

  async getProfile() {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  async updateProfile(userData: {
    first_name?: string;
    last_name?: string;
    email?: string;
  }) {
    const response = await api.patch('/auth/profile/update/', userData);
    return response.data;
  },
};
