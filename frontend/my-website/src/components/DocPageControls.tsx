import React, { useEffect, useState } from 'react';
import styles from './DocPageControls.module.css';

export default function DocPageControls() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechInstance, setSpeechInstance] = useState<SpeechSynthesisUtterance | null>(null);

  // 1. Handle Scroll Progress
  useEffect(() => {
    const updateScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (window.scrollY / totalHeight) * 100;
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', updateScroll);
    return () => window.removeEventListener('scroll', updateScroll);
  }, []);

  // 2. Handle Text to Speech
  const toggleSpeech = () => {
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      // Get the main content text (Docusaurus usually puts content in 'main' or specific markdown classes)
      const content = document.querySelector('article')?.innerText;
      
      if (content) {
        const utterance = new SpeechSynthesisUtterance(content);
        // Select a nice voice if available (English)
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Google US English')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;
        
        utterance.rate = 1.0;
        utterance.onend = () => setIsSpeaking(false);
        
        window.speechSynthesis.speak(utterance);
        setSpeechInstance(utterance);
        setIsSpeaking(true);
      }
    }
  };

  // Cleanup speech on unmount
  useEffect(() => {
    return () => {
      window.speechSynthesis.cancel();
    };
  }, []);

  return (
    <>
      {/* Progress Bar */}
      <div className={styles.progressBarContainer}>
        <div 
          className={styles.progressBar} 
          style={{ width: `${scrollProgress}%` }} 
        />
      </div>

      {/* Listen Button (Floating Bottom Left or Top Right) */}
      <button 
        className={`${styles.listenButton} ${isSpeaking ? styles.speaking : ''}`}
        onClick={toggleSpeech}
        title={isSpeaking ? "Stop Listening" : "Listen to Page"}
      >
        {isSpeaking ? '🔇 Stop Audio' : '🎧 Listen'}
      </button>
    </>
  );
}
