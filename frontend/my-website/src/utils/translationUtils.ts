/**
 * Translation Utilities
 *
 * Provides helper functions for:
 * - Identifying translatable elements
 * - Preserving technical terms
 * - Handling RTL formatting
 * - Batch translation optimization
 */

/**
 * Technical terms that should be preserved in English
 */
export const TECHNICAL_TERMS = [
  // Frameworks & Tools
  "ROS 2",
  "ROS",
  "Gazebo",
  "Isaac Sim",
  "Isaac SDK",
  "Docusaurus",
  "NVIDIA Isaac",

  // Programming & APIs
  "Python",
  "C++",
  "JavaScript",
  "TypeScript",
  "API",
  "REST API",
  "JSON",
  "XML",

  // Robotics Concepts
  "SLAM",
  "LIDAR",
  "LiDAR",
  "IMU",
  "URDF",
  "SDF",
  "TF2",
  "Nav2",

  // AI/ML Terms
  "VLA",
  "Vision-Language-Action",
  "LLM",
  "GPT",
  "Transformer",
  "CNN",
  "YOLO",

  // Protocols & Standards
  "DDS",
  "TCP/IP",
  "UDP",
  "HTTP",
  "HTTPS",
  "WebSocket",

  // Hardware
  "GPU",
  "CPU",
  "NVIDIA",
  "Jetson",
  "CUDA",

  // Software Engineering
  "GitHub",
  "Docker",
  "Ubuntu",
  "Linux",
  "CMake",
  "Git",

  // File Extensions
  ".py",
  ".cpp",
  ".js",
  ".ts",
  ".tsx",
  ".yaml",
  ".xml",
  ".urdf",
  ".sdf",
];

/**
 * CSS selectors for elements that should NOT be translated
 */
export const NON_TRANSLATABLE_SELECTORS = [
  "code",
  "pre",
  "script",
  "style",
  "noscript",
  "iframe",
  ".preserve-ltr",
  ".language-toggle",
  "[data-no-translate]",
  ".prism-code",
  ".token",
  ".mermaid",
];

/**
 * CSS selectors for translatable content
 */
export const TRANSLATABLE_SELECTORS = [
  // Main content
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "p",
  "li",
  "td",
  "th",
  "label",
  "button:not(.language-toggle button)",
  "a:not(.navbar__brand)",

  // Docusaurus specific
  ".navbar__item",
  ".menu__link",
  ".breadcrumbs__link",
  ".pagination-nav__label",
  ".admonition-heading",
  ".footer__title",
  ".hero__title",
  ".hero__subtitle",

  // Table of contents
  ".table-of-contents__link",
];

/**
 * Interface for translation cache entry
 */
interface CachedTranslation {
  original: string;
  translated: string;
  timestamp: number;
  language: string;
}

/**
 * In-memory translation cache to avoid redundant API calls
 */
class TranslationCache {
  private cache: Map<string, CachedTranslation> = new Map();
  private maxAge = 1000 * 60 * 60; // 1 hour

  getCacheKey(text: string, targetLang: string): string {
    return `${targetLang}:${text.trim().substring(0, 100)}`;
  }

  get(text: string, targetLang: string): string | null {
    const key = this.getCacheKey(text, targetLang);
    const cached = this.cache.get(key);

    if (!cached) return null;

    // Check if cache entry is still valid
    if (Date.now() - cached.timestamp > this.maxAge) {
      this.cache.delete(key);
      return null;
    }

    return cached.translated;
  }

  set(text: string, translated: string, targetLang: string): void {
    const key = this.getCacheKey(text, targetLang);
    this.cache.set(key, {
      original: text,
      translated,
      timestamp: Date.now(),
      language: targetLang,
    });
  }

  clear(): void {
    this.cache.clear();
  }

  getSize(): number {
    return this.cache.size;
  }
}

export const translationCache = new TranslationCache();

/**
 * Check if an element should be translated
 */
export function isTranslatable(element: HTMLElement): boolean {
  // Skip if element or any parent has data-no-translate
  if (element.closest("[data-no-translate]")) {
    return false;
  }

  // Skip non-translatable elements
  for (const selector of NON_TRANSLATABLE_SELECTORS) {
    if (element.matches(selector)) {
      return false;
    }
  }

  // Check if element has text content
  const text = getTextContent(element);
  if (!text || text.trim().length === 0) {
    return false;
  }

  // Skip if text is purely numeric, URL, or code-like
  if (isPurelyTechnical(text)) {
    return false;
  }

  return true;
}

/**
 * Get clean text content from element (excluding child elements)
 */
export function getTextContent(element: HTMLElement): string {
  // For elements with only text nodes
  const textNodes: string[] = [];

  element.childNodes.forEach((node) => {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent?.trim();
      if (text) {
        textNodes.push(text);
      }
    }
  });

  return textNodes.join(" ");
}

/**
 * Check if text is purely technical (should not be translated)
 */
export function isPurelyTechnical(text: string): boolean {
  const trimmed = text.trim();

  // Check if it's a number
  if (/^\d+$/.test(trimmed)) {
    return true;
  }

  // Check if it's a URL
  if (/^(https?:\/\/|www\.|\/[a-z])/i.test(trimmed)) {
    return true;
  }

  // Check if it's a file path
  if (/^[./~].*\.(py|js|ts|tsx|cpp|h|yaml|xml|urdf|sdf|json)$/i.test(trimmed)) {
    return true;
  }

  // Check if it's code-like (contains special programming characters)
  if (/[{}[\]();=><]/.test(trimmed) && trimmed.length < 50) {
    return true;
  }

  // Check if it's a single technical term
  if (TECHNICAL_TERMS.some((term) => term.toLowerCase() === trimmed.toLowerCase())) {
    return true;
  }

  return false;
}

/**
 * Extract all translatable text nodes from the page
 */
export function extractTranslatableElements(): HTMLElement[] {
  const elements: HTMLElement[] = [];
  const seen = new Set<HTMLElement>();

  for (const selector of TRANSLATABLE_SELECTORS) {
    const found = document.querySelectorAll<HTMLElement>(selector);

    found.forEach((element) => {
      // Skip if already processed or not translatable
      if (seen.has(element) || !isTranslatable(element)) {
        return;
      }

      // Skip if element is inside a code block
      if (element.closest("pre, code")) {
        return;
      }

      // Add to collection
      elements.push(element);
      seen.add(element);
    });
  }

  return elements;
}

/**
 * Batch elements into groups for efficient translation
 */
export function batchElements(
  elements: HTMLElement[],
  maxBatchSize: number = 50
): HTMLElement[][] {
  const batches: HTMLElement[][] = [];

  for (let i = 0; i < elements.length; i += maxBatchSize) {
    batches.push(elements.slice(i, i + maxBatchSize));
  }

  return batches;
}

/**
 * Store original text in element's dataset for reverting
 */
export function storeOriginalText(element: HTMLElement): void {
  const text = getTextContent(element);
  if (text && !element.dataset.originalText) {
    element.dataset.originalText = text;
  }
}

/**
 * Restore original text from element's dataset
 */
export function restoreOriginalText(element: HTMLElement): void {
  if (element.dataset.originalText) {
    // Replace only text nodes, preserve child elements
    element.childNodes.forEach((node) => {
      if (node.nodeType === Node.TEXT_NODE && node.textContent?.trim()) {
        node.textContent = element.dataset.originalText!;
      }
    });
  }
}

/**
 * Replace text in element while preserving child elements
 */
export function replaceTextContent(element: HTMLElement, newText: string): void {
  // Find and replace only text nodes
  let replaced = false;

  element.childNodes.forEach((node) => {
    if (node.nodeType === Node.TEXT_NODE && node.textContent?.trim()) {
      if (!replaced) {
        node.textContent = newText;
        replaced = true;
      } else {
        node.textContent = ""; // Clear other text nodes
      }
    }
  });

  // If no text nodes found, set textContent directly
  if (!replaced) {
    element.textContent = newText;
  }
}

/**
 * Sanitize translated text to prevent XSS
 */
export function sanitizeTranslatedText(text: string): string {
  // Remove any HTML tags that might have been added
  return text.replace(/<[^>]*>/g, "");
}

/**
 * Check if element is currently visible
 */
export function isElementVisible(element: HTMLElement): boolean {
  return element.offsetParent !== null;
}

/**
 * Apply RTL formatting markers if needed
 */
export function applyRTLMarkers(text: string, isRTL: boolean): string {
  if (!isRTL) return text;

  // Add RTL marks around the text
  const RLM = "\u200F"; // Right-to-Left Mark
  return `${RLM}${text}${RLM}`;
}
