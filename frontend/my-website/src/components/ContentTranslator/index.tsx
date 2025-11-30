/**
 * ContentTranslator Component
 *
 * Automatically translates page content when language changes.
 * This is a non-visual component that hooks into language state changes
 * and triggers content translation.
 *
 * Features:
 * - Automatic translation on language switch
 * - Progress indicator during translation
 * - Error handling with retry capability
 * - Seamless integration with existing UI
 */

import React from "react";
import { useContentTranslation } from "../../hooks/useContentTranslation";
import { useLanguage } from "../../hooks/useLanguage";
import styles from "./ContentTranslator.module.css";

const ContentTranslator: React.FC = () => {
  const { progress, error, retryTranslation } = useContentTranslation();
  const { language } = useLanguage();

  // Don't show anything if not translating
  if (!progress.isTranslating && !error) {
    return null;
  }

  return (
    <>
      {/* Translation Progress Indicator */}
      {progress.isTranslating && (
        <div className={styles.translationProgress} role="status" aria-live="polite">
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{
                width: `${(progress.completed / progress.total) * 100}%`,
              }}
            />
          </div>
          <p className={styles.progressText}>
            {language === "ur"
              ? `ترجمہ ہو رہا ہے... ${progress.completed} / ${progress.total}`
              : `Translating... ${progress.completed} / ${progress.total}`}
          </p>
        </div>
      )}

      {/* Error Message */}
      {error && !progress.isTranslating && (
        <div
          className={styles.errorMessage}
          role="alert"
          aria-live="assertive"
        >
          <div className={styles.errorContent}>
            <span className={styles.errorIcon}>⚠️</span>
            <p className={styles.errorText}>
              {language === "ur"
                ? `ترجمہ ناکام: ${error}`
                : `Translation failed: ${error}`}
            </p>
            <button
              className={styles.retryButton}
              onClick={retryTranslation}
              aria-label={
                language === "ur" ? "دوبارہ کوشش کریں" : "Retry translation"
              }
            >
              {language === "ur" ? "دوبارہ کوشش کریں" : "Retry"}
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default ContentTranslator;
