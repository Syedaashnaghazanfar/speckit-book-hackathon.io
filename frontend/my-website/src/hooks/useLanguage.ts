/**
 * useLanguage - Custom hook for accessing language context
 *
 * Provides easy access to:
 * - Current language
 * - Language switching
 * - Translation function
 * - RTL/LTR state
 */

import { useContext } from "react";
import {
  LanguageContext,
  LanguageContextValue,
} from "../context/LanguageContext";

export function useLanguage(): LanguageContextValue {
  const context = useContext(LanguageContext);

  if (context === undefined) {
    throw new Error(
      "useLanguage must be used within a LanguageProvider. " +
        "Make sure your component is wrapped in <LanguageProvider>."
    );
  }

  return context;
}

// Re-export types for convenience
export type { Language, LanguageContextValue } from "../context/LanguageContext";
