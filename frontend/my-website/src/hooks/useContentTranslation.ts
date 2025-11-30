/**
 * useContentTranslation Hook
 *
 * Manages translation of page content when language changes.
 * Features:
 * - Automatic detection of translatable elements
 * - Batch translation for performance
 * - Caching to avoid redundant API calls
 * - Original text preservation for reverting
 * - Loading state management
 */

import { useEffect, useState, useCallback, useRef } from "react";
import { useLanguage } from "./useLanguage";
import {
  extractTranslatableElements,
  batchElements,
  storeOriginalText,
  restoreOriginalText,
  replaceTextContent,
  getTextContent,
  sanitizeTranslatedText,
  translationCache,
  TECHNICAL_TERMS,
} from "../utils/translationUtils";

interface TranslationProgress {
  total: number;
  completed: number;
  isTranslating: boolean;
}

interface UseContentTranslationReturn {
  progress: TranslationProgress;
  error: string | null;
  retryTranslation: () => void;
}

// Get API URL from environment or use default
const getApiUrl = () => {
  try {
    return process.env.REACT_APP_API_URL || "http://localhost:8000";
  } catch (e) {
    return "http://localhost:8000";
  }
};

const API_URL = getApiUrl();

export function useContentTranslation(): UseContentTranslationReturn {
  const { language, isRTL } = useLanguage();
  const [progress, setProgress] = useState<TranslationProgress>({
    total: 0,
    completed: 0,
    isTranslating: false,
  });
  const [error, setError] = useState<string | null>(null);

  // Track previous language to detect changes
  const previousLanguageRef = useRef<string>(language);

  // Track if translation is in progress to prevent duplicate requests
  const translationInProgressRef = useRef(false);

  /**
   * Translate a single element
   */
  const translateElement = useCallback(
    async (element: HTMLElement, targetLang: string): Promise<void> => {
      const text = getTextContent(element);

      if (!text || text.trim().length === 0) {
        return;
      }

      // Store original text before translation
      storeOriginalText(element);

      // Check cache first
      const cached = translationCache.get(text, targetLang);
      if (cached) {
        replaceTextContent(element, cached);
        return;
      }

      try {
        const sourceLang = targetLang === "ur" ? "en" : "ur";

        const response = await fetch(`${API_URL}/api/translate/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text,
            source_language: sourceLang,
            target_language: targetLang,
            preserve_terms: TECHNICAL_TERMS,
          }),
        });

        if (!response.ok) {
          throw new Error(`Translation failed: ${response.status}`);
        }

        const data = await response.json();
        const translatedText = sanitizeTranslatedText(data.translated_text);

        // Cache the translation
        translationCache.set(text, translatedText, targetLang);

        // Update element text
        replaceTextContent(element, translatedText);
      } catch (err) {
        console.error("Failed to translate element:", err);
        // Keep original text on error
      }
    },
    []
  );

  /**
   * Translate batch of elements
   */
  const translateBatch = useCallback(
    async (elements: HTMLElement[], targetLang: string): Promise<void> => {
      const texts: string[] = [];
      const elementMap = new Map<string, HTMLElement[]>();

      // Collect texts and map them to elements
      elements.forEach((element) => {
        const text = getTextContent(element);
        if (text && text.trim().length > 0) {
          storeOriginalText(element);

          // Check cache
          const cached = translationCache.get(text, targetLang);
          if (cached) {
            replaceTextContent(element, cached);
          } else {
            texts.push(text);
            if (!elementMap.has(text)) {
              elementMap.set(text, []);
            }
            elementMap.get(text)!.push(element);
          }
        }
      });

      // If all were cached, we're done
      if (texts.length === 0) {
        return;
      }

      try {
        const sourceLang = targetLang === "ur" ? "en" : "ur";

        const response = await fetch(`${API_URL}/api/translate/batch`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            texts,
            source_language: sourceLang,
            target_language: targetLang,
            preserve_terms: TECHNICAL_TERMS,
          }),
        });

        if (!response.ok) {
          throw new Error(`Batch translation failed: ${response.status}`);
        }

        const data = await response.json();

        // Apply translations to elements
        data.translations.forEach(
          (item: { original_text: string; translated_text: string }) => {
            const translatedText = sanitizeTranslatedText(item.translated_text);

            // Cache the translation
            translationCache.set(item.original_text, translatedText, targetLang);

            // Update all elements with this text
            const elementsToUpdate = elementMap.get(item.original_text) || [];
            elementsToUpdate.forEach((el) => {
              replaceTextContent(el, translatedText);
            });
          }
        );
      } catch (err) {
        console.error("Failed to translate batch:", err);
        throw err;
      }
    },
    []
  );

  /**
   * Translate all content on the page
   */
  const translatePage = useCallback(
    async (targetLang: string) => {
      if (translationInProgressRef.current) {
        console.log("Translation already in progress, skipping...");
        return;
      }

      translationInProgressRef.current = true;
      setError(null);

      try {
        // Extract all translatable elements
        const elements = extractTranslatableElements();

        if (elements.length === 0) {
          setProgress({
            total: 0,
            completed: 0,
            isTranslating: false,
          });
          translationInProgressRef.current = false;
          return;
        }

        setProgress({
          total: elements.length,
          completed: 0,
          isTranslating: true,
        });

        // Batch elements for efficient translation
        const batches = batchElements(elements, 50);

        // Translate batches sequentially
        for (let i = 0; i < batches.length; i++) {
          const batch = batches[i];

          try {
            await translateBatch(batch, targetLang);

            // Update progress
            setProgress((prev) => ({
              ...prev,
              completed: Math.min((i + 1) * 50, elements.length),
            }));
          } catch (err) {
            console.error(`Failed to translate batch ${i + 1}:`, err);
            // Continue with next batch even if one fails
          }
        }

        // Translation complete
        setProgress({
          total: elements.length,
          completed: elements.length,
          isTranslating: false,
        });
      } catch (err) {
        console.error("Translation failed:", err);
        setError(err instanceof Error ? err.message : "Translation failed");
        setProgress((prev) => ({ ...prev, isTranslating: false }));
      } finally {
        translationInProgressRef.current = false;
      }
    },
    [translateBatch]
  );

  /**
   * Revert page to original language
   */
  const revertPage = useCallback(() => {
    const elements = extractTranslatableElements();

    elements.forEach((element) => {
      if (element.dataset.originalText) {
        restoreOriginalText(element);
      }
    });

    setProgress({
      total: 0,
      completed: 0,
      isTranslating: false,
    });
  }, []);

  /**
   * Handle language change
   */
  useEffect(() => {
    const hasLanguageChanged = previousLanguageRef.current !== language;

    if (hasLanguageChanged) {
      console.log(`Language changed from ${previousLanguageRef.current} to ${language}`);

      if (language === "ur") {
        // Translate to Urdu
        translatePage("ur");
      } else {
        // Revert to English
        revertPage();
      }

      previousLanguageRef.current = language;
    }
  }, [language, translatePage, revertPage]);

  /**
   * Retry translation on error
   */
  const retryTranslation = useCallback(() => {
    if (language === "ur") {
      translatePage("ur");
    }
  }, [language, translatePage]);

  return {
    progress,
    error,
    retryTranslation,
  };
}
