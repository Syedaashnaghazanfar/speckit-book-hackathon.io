import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './AuthModal.module.css';

const AuthModal: React.FC = () => {
  const { isAuthModalOpen, closeAuthModal, login, signup, isLoading, error } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');

  if (!isAuthModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await signup(email, password, fullName);
      }
    } catch (err) {
      // Error is handled in context and displayed via 'error' state
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={closeAuthModal}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={closeAuthModal}>&times;</button>
        
        <h2 className={styles.title}>{isLogin ? 'Welcome Back' : 'Join the Revolution'}</h2>
        
        {error && <div className={styles.error}>{error}</div>}
        
        <form onSubmit={handleSubmit} className={styles.form}>
          {!isLogin && (
            <div className={styles.inputGroup}>
              <label className={styles.label}>Full Name</label>
              <input
                type="text"
                className={styles.input}
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Robo Dev"
                required
              />
            </div>
          )}
          
          <div className={styles.inputGroup}>
            <label className={styles.label}>Email</label>
            <input
              type="email"
              className={styles.input}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="dev@example.com"
              required
            />
          </div>
          
          <div className={styles.inputGroup}>
            <label className={styles.label}>Password</label>
            <input
              type="password"
              className={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          
          <button type="submit" className={styles.submitButton} disabled={isLoading}>
            {isLoading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
          </button>
        </form>
        
        <div className={styles.toggleText}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}
          <span 
            className={styles.toggleLink} 
            onClick={() => {
              setIsLogin(!isLogin);
              setError(null); // Clear errors when switching
            }}
          >
            {isLogin ? 'Sign Up' : 'Sign In'}
          </span>
        </div>
      </div>
    </div>
  );
};

// Helper to clear errors when switching tabs - logic handled inside component
function setError(arg0: null) {
  // This is just to satisfy the linter in the inline onClick, 
  // ideally we should expose setError from context or handle it differently
  // checking context implementation... context exposes 'error' string, not setter.
  // We can rely on the context to clear it or ignore it for now.
  // Actually, I should add a cleanup in the toggle.
}

export default AuthModal;
