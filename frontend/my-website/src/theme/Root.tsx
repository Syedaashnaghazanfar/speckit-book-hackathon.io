/**
 * Root Component
 *
 * This component wraps the entire Docusaurus site and adds global components
 * like the ChatWidget and TextSelectionHandler that should appear on every page.
 */

import React, { useRef, useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { AuthProvider } from '../context/AuthContext';
import AuthModal from '../components/Auth/AuthModal';
import ChatWidget, { ChatWidgetRef } from '../components/ChatWidget/ChatWidget';
import TextSelectionHandler from '../components/TextSelectionHandler';
import UserStatus from '../components/Auth/UserStatus';
import RouteGuard from '../components/Auth/RouteGuard';
import DocPageControls from '../components/DocPageControls';
import { useLocation } from '@docusaurus/router';

// Helper to portal the UserStatus into the navbar
const NavbarUserStatusPortal = () => {
  const [mounted, setMounted] = useState(false);
  const [container, setContainer] = useState<Element | null>(null);
  const location = useLocation();

  useEffect(() => {
    setMounted(true);
    
    const updateContainer = () => {
        // We look for the right-side navbar items container
        const items = document.querySelectorAll('.navbar__items--right');
        if (items.length > 0) {
            setContainer(items[0]);
        } else {
            // Fallback
            const allItems = document.querySelectorAll('.navbar__items');
            if (allItems.length > 0) {
                setContainer(allItems[allItems.length - 1]);
            }
        }
    };

    // Run immediately
    updateContainer();

    // Also retry a few times just in case of rendering delays
    // especially important on route changes
    const interval = setInterval(updateContainer, 100);
    setTimeout(() => clearInterval(interval), 1000);

    return () => clearInterval(interval);
  }, [location]); // Re-run on route change

  if (!mounted || !container) return null;

  return ReactDOM.createPortal(<UserStatus />, container);
};

export default function Root({children}) {
  const chatWidgetRef = useRef<ChatWidgetRef>(null);
  const location = useLocation();

  const handleSelectionQuery = (selectedText: string) => {
    chatWidgetRef.current?.askAboutSelection(selectedText);
  };

  const isDocPage = location.pathname.startsWith('/docs');

  return (
    <AuthProvider>
      <RouteGuard>
        {isDocPage && <DocPageControls />}
        {children}
      </RouteGuard>
      <NavbarUserStatusPortal />
      <AuthModal />
      {/* <ContentTranslator /> */}
      <TextSelectionHandler onSelectionQuery={handleSelectionQuery} />
      <ChatWidget ref={chatWidgetRef} />
    </AuthProvider>
  );
}
