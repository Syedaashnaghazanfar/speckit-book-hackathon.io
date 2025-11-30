# Content Translation System

## Overview

This document describes the complete implementation of the English-Urdu bidirectional translation system for the Physical AI & Humanoid Robotics textbook website.

## Architecture

### Components

1. **LanguageContext** (`src/context/LanguageContext.tsx`)
   - Global state management for language selection (en/ur)
   - RTL/LTR direction management
   - Translation API integration
   - localStorage persistence

2. **LanguageToggle** (`src/components/LanguageToggle/`)
   - UI button for switching languages
   - Purple/neon theme styling
   - Loading state during translation

3. **ContentTranslator** (`src/components/ContentTranslator/`)
   - Non-visual component that triggers translation
   - Progress indicator during translation
   - Error handling with retry capability

4. **useContentTranslation** (`src/hooks/useContentTranslation.ts`)
   - Custom hook for page translation logic
   - Batch translation for performance
   - Caching to avoid redundant API calls
   - Original text preservation for reverting

5. **Translation Utilities** (`src/utils/translationUtils.ts`)
   - Element detection and filtering
   - Technical term preservation
   - Text extraction and replacement
   - RTL formatting helpers

### Backend API

- **Endpoint**: `http://localhost:8000/api/translate/`
- **Provider**: Gemini 2.5 Flash
- **Features**:
  - Single text translation
  - Batch translation (up to 100 items)
  - Translation caching
  - Technical term preservation

## How It Works

### Translation Flow

```
User clicks LanguageToggle
    ↓
LanguageContext updates language state
    ↓
useContentTranslation detects language change
    ↓
Extract translatable elements from DOM
    ↓
Batch elements into groups (50 per batch)
    ↓
Call backend /api/translate/batch endpoint
    ↓
Apply translations to elements
    ↓
Show completion
```

### Technical Term Preservation

The following technical terms are preserved in English:

- **Frameworks**: ROS 2, Gazebo, Isaac Sim, Isaac SDK, Docusaurus
- **Languages**: Python, C++, JavaScript, TypeScript
- **Protocols**: API, REST API, JSON, XML, HTTP, HTTPS, WebSocket
- **Robotics**: SLAM, LIDAR, IMU, URDF, SDF, TF2, Nav2
- **AI/ML**: VLA, LLM, GPT, Transformer, CNN, YOLO
- **Hardware**: GPU, CPU, NVIDIA, Jetson, CUDA
- **Tools**: GitHub, Docker, Ubuntu, Linux, CMake, Git

### Element Selection

#### Translatable Elements
- Headings (h1-h6)
- Paragraphs (p)
- List items (li)
- Table cells (td, th)
- Labels, buttons, links
- Navigation items
- Breadcrumbs
- Footer content

#### Non-Translatable Elements
- Code blocks (`<code>`, `<pre>`)
- Mermaid diagrams
- Scripts and styles
- Elements with `data-no-translate` attribute
- Elements with `.preserve-ltr` class

### RTL Support

When language is set to Urdu (`ur`):

1. **Document Direction**
   ```javascript
   document.documentElement.dir = "rtl";
   document.documentElement.lang = "ur";
   ```

2. **CSS Classes**
   - `html[dir="rtl"]` applied to document
   - `.rtl` class added to root element

3. **Content Alignment**
   - Text aligned right
   - Lists padded from right
   - Navigation reversed
   - Breadcrumbs flipped

4. **Preserved LTR Elements**
   - Code blocks remain LTR
   - URLs remain LTR
   - Technical identifiers remain LTR

## Usage

### For Users

1. Click the language toggle button in the navbar (🌐)
2. Wait for translation to complete (progress bar shown)
3. All page content translates to Urdu
4. Technical terms remain in English
5. Code blocks remain in English (LTR)
6. Click again to revert to English

### For Developers

#### Adding Non-Translatable Elements

```html
<!-- Method 1: Using data attribute -->
<div data-no-translate>
  This content will not be translated
</div>

<!-- Method 2: Using CSS class -->
<div class="preserve-ltr">
  This content stays LTR
</div>
```

#### Adding Technical Terms

Edit `src/utils/translationUtils.ts`:

```typescript
export const TECHNICAL_TERMS = [
  // ... existing terms
  "YourNewTerm",
];
```

#### Customizing Translatable Selectors

Edit `src/utils/translationUtils.ts`:

```typescript
export const TRANSLATABLE_SELECTORS = [
  // ... existing selectors
  ".your-custom-selector",
];
```

## Performance Optimization

### Caching Strategy

1. **In-Memory Cache**
   - Translations cached for 1 hour
   - Cache key: `${targetLang}:${text.substring(0, 100)}`
   - Automatic cache expiration

2. **Batch Translation**
   - Elements batched in groups of 50
   - Parallel processing within batches
   - Progress tracking per batch

3. **Lazy Translation**
   - Only visible elements translated
   - Original text stored for reverting
   - No re-translation on language switch back

### API Rate Limiting

- Maximum 100 texts per batch request
- Sequential batch processing to avoid overload
- Error handling with retry capability

## Testing

### Manual Testing

1. **Start Backend**
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

2. **Start Frontend**
   ```bash
   cd frontend/my-website
   npm start
   ```

3. **Test Translation**
   - Navigate to any page
   - Click language toggle
   - Verify content translates
   - Verify technical terms preserved
   - Verify code blocks remain LTR
   - Verify RTL layout applied
   - Click toggle again to revert

### Test Checklist

- [ ] Homepage translates correctly
- [ ] Documentation pages translate
- [ ] Navigation menu translates
- [ ] Footer translates
- [ ] Buttons translate
- [ ] Technical terms preserved
- [ ] Code blocks remain LTR
- [ ] Mermaid diagrams not affected
- [ ] RTL layout applied correctly
- [ ] Translation cache works
- [ ] Error handling works
- [ ] Retry functionality works
- [ ] Language persists on reload
- [ ] Mobile responsive

## Troubleshooting

### Translation Not Working

1. **Check Backend**
   ```bash
   curl http://localhost:8000/api/translate/health
   ```
   Should return: `{"status": "healthy"}`

2. **Check Console**
   - Open browser DevTools
   - Look for translation errors
   - Check network requests

3. **Clear Cache**
   ```javascript
   // In browser console
   localStorage.clear();
   location.reload();
   ```

### Performance Issues

1. **Reduce Batch Size**
   - Edit `useContentTranslation.ts`
   - Change batch size from 50 to 25

2. **Clear Translation Cache**
   ```javascript
   // In browser console
   import { translationCache } from './utils/translationUtils';
   translationCache.clear();
   ```

### RTL Layout Issues

1. **Check CSS**
   - Verify `custom.css` has RTL rules
   - Check `html[dir="rtl"]` selector

2. **Force RTL**
   ```javascript
   // In browser console
   document.documentElement.dir = 'rtl';
   document.documentElement.classList.add('rtl');
   ```

## File Structure

```
frontend/my-website/src/
├── components/
│   ├── ContentTranslator/
│   │   ├── index.tsx               # Translation progress UI
│   │   └── ContentTranslator.module.css
│   └── LanguageToggle/
│       ├── index.tsx               # Language switch button
│       └── LanguageToggle.module.css
├── context/
│   └── LanguageContext.tsx         # Language state management
├── hooks/
│   ├── useLanguage.ts              # Language context hook
│   └── useContentTranslation.ts    # Translation logic hook
├── utils/
│   └── translationUtils.ts         # Translation utilities
├── theme/
│   └── Root.tsx                    # Root component (includes ContentTranslator)
└── css/
    └── custom.css                  # RTL styles
```

## API Reference

### LanguageContext

```typescript
interface LanguageContextValue {
  language: "en" | "ur";
  setLanguage: (lang: Language) => void;
  isRTL: boolean;
  translate: (text: string, targetLang?: Language) => Promise<string>;
  isTranslating: boolean;
}
```

### useContentTranslation

```typescript
interface UseContentTranslationReturn {
  progress: {
    total: number;
    completed: number;
    isTranslating: boolean;
  };
  error: string | null;
  retryTranslation: () => void;
}
```

### Translation API

**Single Translation**
```bash
POST http://localhost:8000/api/translate/
Content-Type: application/json

{
  "text": "Hello World",
  "source_language": "en",
  "target_language": "ur",
  "preserve_terms": ["API", "ROS 2"]
}
```

**Batch Translation**
```bash
POST http://localhost:8000/api/translate/batch
Content-Type: application/json

{
  "texts": ["Hello", "World"],
  "source_language": "en",
  "target_language": "ur",
  "preserve_terms": ["API", "ROS 2"]
}
```

## Future Enhancements

1. **More Languages**
   - Add support for Hindi, Arabic, etc.
   - Language detection

2. **Offline Mode**
   - IndexedDB for persistent cache
   - Service worker for offline translation

3. **Custom Glossaries**
   - User-defined term preservation
   - Domain-specific dictionaries

4. **Translation Quality**
   - User feedback on translations
   - Machine learning for improvement

5. **Performance**
   - Web Workers for background translation
   - Progressive translation (visible first)
   - Virtual scrolling for large pages

## Credits

- **Translation Provider**: Google Gemini 2.5 Flash
- **Framework**: Docusaurus v4
- **UI Library**: React 18
- **Styling**: CSS Modules + Custom CSS
- **Theme**: Purple/Neon

## License

Part of the Physical AI & Humanoid Robotics Textbook project.
Copyright © 2024 Ashna Ghazanfar.
