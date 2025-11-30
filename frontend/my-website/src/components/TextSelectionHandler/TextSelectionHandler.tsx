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
    const selection = window.getSelection();
    const text = selection?.toString().trim();

    if (text && text.length > 10) {
      // Only show button for selections > 10 characters
      setSelectedText(text);

      // Get selection position
      const range = selection?.getRangeAt(0);
      const rect = range?.getBoundingClientRect();

      if (rect) {
        setButtonPosition({
          x: rect.left + rect.width / 2,
          y: rect.top - 40, // Position above selection
        });
      }
    } else {
      setSelectedText('');
      setButtonPosition(null);
    }
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
    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('click', handleClickOutside);
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
