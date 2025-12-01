/**
 * TextSelectionHandler Component
 *
 * Detects text selection and provides a floating button to ask questions
 * about the selected text using scoped RAG queries.
 */

import React, { useState, useEffect, useCallback } from 'react';
import styles from './TextSelectionHandler.module.css';

interface TextSelectionHandlerProps {
  onSelectionQuery: (selectedText: string) => void;
}

const TextSelectionHandler: React.FC<TextSelectionHandlerProps> = ({
  onSelectionQuery,
}) => {
  const [selectedText, setSelectedText] = useState('');
  const [buttonPosition, setButtonPosition] = useState<{ x: number; y: number } | null>(null);

  const handleTextSelection = useCallback(() => {
    // Small delay to ensure selection is complete (especially on mobile)
    setTimeout(() => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();

      if (text && text.length > 10) {
        // Only show button for selections > 10 characters
        setSelectedText(text);

        // Get selection position
        const range = selection?.getRangeAt(0);
        const rect = range?.getBoundingClientRect();

        if (rect) {
          // Calculate position with viewport awareness for mobile
          const viewportWidth = window.innerWidth;
          const viewportHeight = window.innerHeight;

          let x = rect.left + rect.width / 2;
          let y = rect.top - 50; // Position above selection

          // Ensure button stays within viewport bounds
          const buttonWidth = 150; // Approximate button width
          const buttonHeight = 40; // Approximate button height

          // Adjust horizontal position if too close to edge
          if (x - buttonWidth / 2 < 10) {
            x = buttonWidth / 2 + 10;
          } else if (x + buttonWidth / 2 > viewportWidth - 10) {
            x = viewportWidth - buttonWidth / 2 - 10;
          }

          // If not enough space above, position below selection
          if (y < 10) {
            y = rect.bottom + 10;
          }

          // Ensure button doesn't go below viewport
          if (y + buttonHeight > viewportHeight - 10) {
            y = rect.top - 50;
          }

          setButtonPosition({ x, y });
        }
      } else {
        setSelectedText('');
        setButtonPosition(null);
      }
    }, 10);
  }, []);

  const handleAskAboutSelection = () => {
    if (selectedText) {
      onSelectionQuery(selectedText);
      // Clear selection
      setSelectedText('');
      setButtonPosition(null);
      window.getSelection()?.removeAllRanges();
    }
  };

  const handleClickOutside = useCallback((e: MouseEvent) => {
    const target = e.target as HTMLElement;
    if (!target.closest(`.${styles.floatingButton}`)) {
      setSelectedText('');
      setButtonPosition(null);
    }
  }, []);

  useEffect(() => {
    // Mouse events for desktop
    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('click', handleClickOutside);

    // Touch events for mobile
    document.addEventListener('touchend', handleTextSelection);
    document.addEventListener('touchstart', handleClickOutside);

    // Handle selection change event (works on both mobile and desktop)
    document.addEventListener('selectionchange', handleTextSelection);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('click', handleClickOutside);
      document.removeEventListener('touchend', handleTextSelection);
      document.removeEventListener('touchstart', handleClickOutside);
      document.removeEventListener('selectionchange', handleTextSelection);
    };
  }, [handleTextSelection, handleClickOutside]);

  if (!buttonPosition) {
    return null;
  }

  return (
    <button
      className={styles.floatingButton}
      style={{
        position: 'fixed',
        left: `${buttonPosition.x}px`,
        top: `${buttonPosition.y}px`,
        transform: 'translateX(-50%)',
      }}
      onClick={handleAskAboutSelection}
      title="Ask AI about selected text"
    >
      🤔 Ask about this
    </button>
  );
};

export default TextSelectionHandler;
