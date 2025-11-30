"""
Translation service for English-Urdu bidirectional translation.

Uses Google Gemini for high-quality translation with technical term preservation.
"""

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Optional, Dict
import asyncio
import logging
import hashlib
import re

from ..config import settings
from ..models.translation import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse
)

logger = logging.getLogger(__name__)


class TranslationService:
    """Provides English-Urdu translation with technical term preservation."""

    # Common technical terms that should be preserved during translation
    DEFAULT_PRESERVE_TERMS = [
        "ROS 2", "ROS", "SLAM", "API", "SDK", "URDF", "YAML", "XML", "JSON",
        "Gazebo", "Isaac Sim", "NVIDIA", "Python", "C++", "JavaScript",
        "Docker", "Kubernetes", "Git", "GitHub", "Linux", "Ubuntu",
        "TensorFlow", "PyTorch", "OpenCV", "numpy", "pandas",
        "HTTP", "HTTPS", "REST", "GraphQL", "WebSocket",
        "AI", "ML", "DL", "CNN", "RNN", "LSTM", "GAN", "VAE",
        "RGB", "LIDAR", "IMU", "GPS", "USB", "TCP", "IP",
        "CPU", "GPU", "RAM", "SSD", "HDD",
        "VLA", "LLM", "Transformer", "BERT", "GPT"
    ]

    def __init__(self):
        """Initialize Gemini client and translation cache."""
        genai.configure(api_key=settings.gemini_api_key)

        # Configure safety settings to be permissive for translation
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Configure for accurate translation
        self.model = genai.GenerativeModel(
            model_name='models/gemini-2.5-flash',  # Updated to gemini-2.5-flash
            generation_config={
                'temperature': 0.1,  # Low temperature for consistent translation
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 8192,
            },
            safety_settings=safety_settings
        )

        # Simple in-memory cache for translations
        # Key: hash(text + source + target), Value: translated_text
        self._cache: Dict[str, str] = {}

        logger.info("Translation service initialized with Gemini")

    def _get_cache_key(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> str:
        """Generate cache key for translation."""
        content = f"{text}:{source_lang}:{target_lang}"
        return hashlib.md5(content.encode()).hexdigest()

    def _build_translation_prompt(
        self,
        text: str,
        source_language: str,
        target_language: str,
        preserve_terms: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> str:
        """Build translation prompt for Gemini."""

        # Merge default and custom preserve terms
        terms_to_preserve = set(self.DEFAULT_PRESERVE_TERMS)
        if preserve_terms:
            terms_to_preserve.update(preserve_terms)

        # Build prompt
        lang_map = {
            "en": "English",
            "ur": "Urdu"
        }

        source = lang_map.get(source_language, source_language)
        target = lang_map.get(target_language, target_language)

        prompt = f"""You are a professional translator specializing in technical education content.

Task: Translate the following {source} text to {target}.

Important Guidelines:
1. Maintain the exact meaning and tone of the original text
2. For technical terms, acronyms, and code snippets, preserve them in English
3. Preserve these specific terms in English: {', '.join(sorted(terms_to_preserve))}
4. Keep URLs, file paths, and code blocks unchanged
5. Maintain proper grammar and natural phrasing in {target}
6. For Urdu translations, use modern standard Urdu with technical terms in English where appropriate
7. Preserve formatting (line breaks, punctuation, special characters)
8. Do NOT add any explanations, notes, or extra content - only provide the translation
"""

        if context:
            prompt += f"\nContext: {context}\n"

        prompt += f"""
Text to translate:
{text}

Translation ({target}):"""

        return prompt

    async def translate(
        self,
        request: TranslationRequest
    ) -> TranslationResponse:
        """
        Translate text from source to target language.

        Args:
            request: Translation request with text and language parameters

        Returns:
            TranslationResponse with translated text
        """
        # Check cache
        cache_key = self._get_cache_key(
            request.text,
            request.source_language,
            request.target_language
        )

        if cache_key in self._cache:
            logger.info("Translation served from cache")
            return TranslationResponse(
                original_text=request.text,
                translated_text=self._cache[cache_key],
                source_language=request.source_language,
                target_language=request.target_language,
                confidence=1.0,
                cached=True,
                preserved_terms=request.preserve_terms
            )

        # Build prompt
        prompt = self._build_translation_prompt(
            request.text,
            request.source_language,
            request.target_language,
            request.preserve_terms,
            request.context
        )

        try:
            # Generate translation (sync API, run in executor)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )

            # Extract translated text
            if not response.candidates or not response.candidates[0].content.parts:
                logger.warning("Translation blocked or failed")
                translated_text = request.text  # Fallback to original
                confidence = 0.0
            else:
                translated_text = response.text.strip()
                confidence = 0.95  # High confidence for Gemini translations

            # Store in cache
            self._cache[cache_key] = translated_text

            logger.info(
                f"Translation completed: {request.source_language} → {request.target_language}, "
                f"Length: {len(request.text)} → {len(translated_text)}"
            )

            return TranslationResponse(
                original_text=request.text,
                translated_text=translated_text,
                source_language=request.source_language,
                target_language=request.target_language,
                confidence=confidence,
                cached=False,
                preserved_terms=request.preserve_terms
            )

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise

    async def batch_translate(
        self,
        request: BatchTranslationRequest
    ) -> BatchTranslationResponse:
        """
        Translate multiple texts in batch.

        Args:
            request: Batch translation request

        Returns:
            BatchTranslationResponse with all translations
        """
        translations = []
        cached_count = 0

        # Create individual translation requests
        tasks = []
        for text in request.texts:
            translation_request = TranslationRequest(
                text=text,
                source_language=request.source_language,
                target_language=request.target_language,
                preserve_terms=request.preserve_terms
            )
            tasks.append(self.translate(translation_request))

        # Execute all translations concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Batch translation item failed: {str(result)}")
                # Add error placeholder
                translations.append(TranslationResponse(
                    original_text="",
                    translated_text="[Translation Error]",
                    source_language=request.source_language,
                    target_language=request.target_language,
                    confidence=0.0,
                    cached=False
                ))
            else:
                translations.append(result)
                if result.cached:
                    cached_count += 1

        logger.info(
            f"Batch translation completed: {len(translations)} items, "
            f"{cached_count} from cache"
        )

        return BatchTranslationResponse(
            translations=translations,
            total_count=len(translations),
            cached_count=cached_count
        )

    def _detect_code_blocks(self, text: str) -> List[tuple]:
        """
        Detect code blocks in markdown-style text.

        Returns list of (start_pos, end_pos) tuples.
        """
        code_blocks = []

        # Match ```...``` code blocks
        pattern = r'```[\s\S]*?```'
        for match in re.finditer(pattern, text):
            code_blocks.append((match.start(), match.end()))

        # Match inline code `...`
        pattern = r'`[^`]+`'
        for match in re.finditer(pattern, text):
            code_blocks.append((match.start(), match.end()))

        return code_blocks

    def clear_cache(self):
        """Clear translation cache."""
        self._cache.clear()
        logger.info("Translation cache cleared")

    def get_cache_size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


# Global instance
translation_service = TranslationService()
