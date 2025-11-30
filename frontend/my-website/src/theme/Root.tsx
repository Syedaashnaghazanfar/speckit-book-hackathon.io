/**
 * Root Component
 *
 * This component wraps the entire Docusaurus site and adds global components
 * like the ChatWidget and TextSelectionHandler that should appear on every page.
 */

import React, { useRef } from 'react';
// import { LanguageProvider } from '../context/LanguageContext';
import ChatWidget, { ChatWidgetRef } from '../components/ChatWidget/ChatWidget';
import TextSelectionHandler from '../components/TextSelectionHandler';
// import ContentTranslator from '../components/ContentTranslator';

export default function Root({children}) {
  const chatWidgetRef = useRef<ChatWidgetRef>(null);

  const handleSelectionQuery = (selectedText: string) => {
    chatWidgetRef.current?.askAboutSelection(selectedText);
  };

  return (
    <>
      {children}
      {/* <ContentTranslator /> */}
      <TextSelectionHandler onSelectionQuery={handleSelectionQuery} />
      <ChatWidget ref={chatWidgetRef} />
    </>
  );
}
