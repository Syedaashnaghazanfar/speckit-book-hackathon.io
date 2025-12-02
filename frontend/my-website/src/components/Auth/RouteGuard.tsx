import React, { useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useLocation, useHistory } from '@docusaurus/router';
import Swal from 'sweetalert2';

export default function RouteGuard({ children }: { children: React.ReactNode }) {
  const { user, isInitialized, openAuthModal } = useAuth();
  const location = useLocation();
  const history = useHistory();

  const isProtected = location.pathname.startsWith('/docs');

  useEffect(() => {
    if (isInitialized && !user && isProtected) {
      // Redirect to home
      history.push('/');
      
      // Open auth modal
      openAuthModal();
      
      // Show alert
      Swal.fire({
        title: 'Authentication Required',
        text: 'Please sign in to access the course materials.',
        icon: 'warning',
        confirmButtonColor: '#9333ea',
        background: '#1A0F2E',
        color: '#ffffff',
        toast: true,
        position: 'top-end',
        timer: 4000,
        showConfirmButton: false
      });
    }
  }, [isInitialized, user, isProtected, history, openAuthModal]);

  // Prevent rendering of protected content if not authenticated
  if (isInitialized && !user && isProtected) {
    return null;
  }

  return <>{children}</>;
}
