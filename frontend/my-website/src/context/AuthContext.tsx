import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import Swal from 'sweetalert2';

interface User {
  id: number;
  email: string;
  full_name?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isInitialized: boolean;
  error: string | null;
  isAuthModalOpen: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  openAuthModal: () => void;
  closeAuthModal: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Detect environment and use appropriate API URL
const API_URL = typeof window !== 'undefined' && window.location.hostname === "localhost"
  ? "http://localhost:8000"
  : "https://ashnaali22-hackhathon-backend.hf.space";

// Theme colors matching the website
const THEME_COLOR = '#9333ea'; // Purple
const BG_COLOR = '#1A0F2E';    // Dark Purple/Black
const TEXT_COLOR = '#ffffff';  // White

// Common SweetAlert configuration for theme consistency
const swalConfig = {
  background: BG_COLOR,
  color: TEXT_COLOR,
  confirmButtonColor: THEME_COLOR,
  cancelButtonColor: '#ff006e',
  customClass: {
    popup: 'neon-border-popup' // We can add this class globally if needed, or just rely on inline styles
  }
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isInitialized, setIsInitialized] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState<boolean>(false);

  useEffect(() => {
    // Check local storage for token on load
    const storedToken = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('auth_user');
    if (storedToken && storedUser) {
      setToken(storedToken);
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error("Failed to parse stored user", e);
        logout();
      }
    }
    setIsInitialized(true);
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Login failed');
      }

      const data = await response.json();
      const { access_token, user } = data;

      setToken(access_token);
      setUser(user);
      localStorage.setItem('auth_token', access_token);
      localStorage.setItem('auth_user', JSON.stringify(user));
      closeAuthModal();
      
      Swal.fire({
        ...swalConfig,
        title: 'Welcome Back!',
        text: `Successfully logged in as ${user.full_name || user.email}`,
        icon: 'success',
        timer: 2000,
        showConfirmButton: false
      });
      
    } catch (err: any) {
      setError(err.message);
      Swal.fire({
        ...swalConfig,
        title: 'Login Failed',
        text: err.message,
        icon: 'error',
      });
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (email: string, password: string, full_name?: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, full_name }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Signup failed');
      }

      const data = await response.json();
      const { access_token, user } = data;

      setToken(access_token);
      setUser(user);
      localStorage.setItem('auth_token', access_token);
      localStorage.setItem('auth_user', JSON.stringify(user));
      closeAuthModal();
      
      Swal.fire({
        ...swalConfig,
        title: 'Welcome!',
        text: 'Your account has been created successfully.',
        icon: 'success',
        timer: 2000,
        showConfirmButton: false
      });

    } catch (err: any) {
      setError(err.message);
      Swal.fire({
        ...swalConfig,
        title: 'Signup Failed',
        text: err.message,
        icon: 'error',
      });
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    
    Swal.fire({
        ...swalConfig,
        title: 'Logged Out',
        text: 'See you soon!',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
    });
  };

  const openAuthModal = () => setIsAuthModalOpen(true);
  const closeAuthModal = () => {
    setIsAuthModalOpen(false);
    setError(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isInitialized,
        error,
        isAuthModalOpen,
        login,
        signup,
        logout,
        openAuthModal,
        closeAuthModal,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};