/**
 * LanguageToggle Component
 *
 * A button to toggle between English and Urdu languages.
 * Features:
 * - Displays current language and target language
 * - Purple/neon gradient styling matching site theme
 * - Smooth transitions
 * - Loading state during translation
 * - Accessible keyboard navigation
 */

import React from "react";
import { useLanguage } from "../../hooks/useLanguage";
import styles from "./LanguageToggle.module.css";

const LanguageToggle: React.FC = () => {
  const { language, setLanguage, isTranslating } = useLanguage();

  const toggleLanguage = () => {
    const newLang = language === "en" ? "ur" : "en";
    setLanguage(newLang);
  };

  // Language labels
  const labels = {
    en: {
      current: "English",
      target: "اردو Urdu",
      ariaLabel: "Switch to Urdu",
    },
    ur: {
      current: "اردو",
      target: "English انگریزی",
      ariaLabel: "Switch to English",
    },
  };

  const currentLabels = labels[language];

  return (
    <button
      className={styles.languageToggle}
      onClick={toggleLanguage}
      disabled={isTranslating}
      aria-label={currentLabels.ariaLabel}
      title={currentLabels.ariaLabel}
    >
      <span className={styles.icon}>🌐</span>
      <span className={styles.label}>{currentLabels.target}</span>
      {isTranslating && <span className={styles.spinner}>⏳</span>}
    </button>
  );
};

export default LanguageToggle;
