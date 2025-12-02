import React from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './UserStatus.module.css';

export default function UserStatus() {
  const { user, logout, openAuthModal } = useAuth();

  if (!user) {
    return (
      <button 
        className="button button--primary button--sm" 
        onClick={openAuthModal}
        style={{ marginLeft: '10px', fontWeight: 'bold' }}
      >
        Sign In
      </button>
    );
  }

  return (
    <div className={styles.userContainer}>
      <span className={styles.greeting}>
        Hi, <span className={styles.username}>{user.full_name || user.email.split('@')[0]}</span>
      </span>
      <button 
        className="button button--secondary button--sm" 
        onClick={logout}
        title="Sign Out"
      >
        Logout
      </button>
    </div>
  );
}
