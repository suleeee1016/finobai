import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService.ts';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (userData: RegisterData) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth, AuthProvider içinde kullanılmalı');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem('finoba_token');
    if (savedToken) {
      setToken(savedToken);
      // Kullanıcı profilini al
      authService.getProfile().then((userData) => {
        setUser(userData);
      }).catch(() => {
        localStorage.removeItem('finoba_token');
        localStorage.removeItem('finoba_refresh_token');
      }).finally(() => {
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await authService.login(email, password);
      setUser(response.user);
      setToken(response.tokens.access);
      localStorage.setItem('finoba_token', response.tokens.access);
      localStorage.setItem('finoba_refresh_token', response.tokens.refresh);
      return true;
    } catch (error) {
      return false;
    }
  };

  const register = async (userData: RegisterData): Promise<boolean> => {
    try {
      const response = await authService.register(userData);
      setUser(response.user);
      setToken(response.tokens.access);
      localStorage.setItem('finoba_token', response.tokens.access);
      localStorage.setItem('finoba_refresh_token', response.tokens.refresh);
      return true;
    } catch (error) {
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('finoba_token');
    localStorage.removeItem('finoba_refresh_token');
    authService.logout();
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    loading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
