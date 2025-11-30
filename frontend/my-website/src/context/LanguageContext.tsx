/**
 * LanguageContext - Global state management for language selection
 *
 * Provides:
 * - Current language state (en/ur)
 * - Language switching functionality
 * - Translation API integration
 * - localStorage persistence
 * - RTL/LTR direction management
 */

import React, { createContext, useState, useEffect, ReactNode } from "react";

export type Language = "en" | "ur";

export interface LanguageContextValue {
  language: Language;
  setLanguage: (lang: Language) => void;
  isRTL: boolean;
  translate: (text: string, targetLang?: Language) => Promise<string>;
  isTranslating: boolean;
}

export const LanguageContext = createContext<LanguageContextValue | undefined>(
  undefined
);

interface LanguageProviderProps {
  children: ReactNode;
}

const LANGUAGE_STORAGE_KEY = "preferred-language";

// Safely get API URL without crashing if process is undefined
const getApiUrl = () => {
  try {
    return process.env.REACT_APP_API_URL || "http://localhost:8000";
  } catch (e) {
    return "http://localhost:8000";
  }
};

const API_URL = getApiUrl();

export const LanguageProvider: React.FC<LanguageProviderProps> = ({
  children,
}) => {
  // Initialize language from localStorage or default to English
  const [language, setLanguageState] = useState<Language>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem(LANGUAGE_STORAGE_KEY);
      return (saved === "ur" ? "ur" : "en") as Language;
    }
    return "en";
  });

  const [isTranslating, setIsTranslating] = useState(false);

  // Compute RTL based on language
  const isRTL = language === "ur";

  // Persist language to localStorage and update document direction
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, language);

      // Update document direction
      document.documentElement.dir = isRTL ? "rtl" : "ltr";
      document.documentElement.lang = language;

      // Add/remove RTL class for additional styling
      if (isRTL) {
        document.documentElement.classList.add("rtl");
      } else {
        document.documentElement.classList.remove("rtl");
      }

      console.log(`Language changed to: ${language}, RTL: ${isRTL}`);
    }
  }, [language, isRTL]);

  // Set language with validation
  const setLanguage = (lang: Language) => {
    if (lang !== "en" && lang !== "ur") {
      console.error(`Invalid language: ${lang}`);
      return;
    }
    setLanguageState(lang);
  };

  // Translate text using backend API
  const translate = async (
    text: string,
    targetLang?: Language
  ): Promise<string> => {
    const target = targetLang || language;
    const source: Language = target === "en" ? "ur" : "en";

    // If target is same as current text language, return as-is
    if (source === target) {
      return text;
    }

    setIsTranslating(true);

    try {
      const response = await fetch(`${API_URL}/api/translate/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          source_language: source,
          target_language: target,
          preserve_terms: [
            "ROS 2",
            "ROS",
            "SLAM",
            "Gazebo",
            "Isaac Sim",
            "Isaac SDK",
            "Python",
            "C++",
            "JavaScript",
            "TypeScript",
            "API",
            "REST API",
            "JSON",
            "XML",
            "LIDAR",
            "LiDAR",
            "IMU",
            "URDF",
            "SDF",
            "TF2",
            "Nav2",
            "VLA",
            "Vision-Language-Action",
            "LLM",
            "GPT",
            "Transformer",
            "CNN",
            "YOLO",
            "DDS",
            "TCP/IP",
            "UDP",
            "HTTP",
            "HTTPS",
            "WebSocket",
            "GPU",
            "CPU",
            "NVIDIA",
            "Jetson",
            "CUDA",
            "GitHub",
            "Docker",
            "Ubuntu",
            "Linux",
            "CMake",
            "Git",
          ],
        }),
      });

      if (!response.ok) {
        throw new Error(`Translation failed: ${response.status}`);
      }

      const data = await response.json();
      return data.translated_text;
    } catch (error) {
      console.error("Translation error:", error);
      // Return original text on error
      return text;
    } finally {
      setIsTranslating(false);
    }
  };

  const value: LanguageContextValue = {
    language,
    setLanguage,
    isRTL,
    translate,
    isTranslating,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};
