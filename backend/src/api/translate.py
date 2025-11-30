"""
Translation API endpoint for English-Urdu bidirectional translation.

Handles:
- Single text translation
- Batch translation
- Translation caching
- Error handling
"""

from fastapi import APIRouter, HTTPException, status
import logging

from ..models.translation import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse
)
from ..services.translation import translation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/translate", tags=["translation"])


@router.post("/", response_model=TranslationResponse, status_code=status.HTTP_200_OK)
async def translate_text(request: TranslationRequest):
    """
    Translate text from source to target language.

    Args:
        request: TranslationRequest with text and language parameters

    Returns:
        TranslationResponse with translated text and metadata

    Raises:
        HTTPException: If translation fails
    """
    try:
        logger.info(
            f"Translation request: {request.source_language} → {request.target_language}, "
            f"Text length: {len(request.text)}"
        )

        # Validate language codes
        valid_languages = {'en', 'ur'}
        if request.source_language not in valid_languages or request.target_language not in valid_languages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid language code. Supported: {valid_languages}"
            )

        # Prevent same-language translation
        if request.source_language == request.target_language:
            return TranslationResponse(
                original_text=request.text,
                translated_text=request.text,
                source_language=request.source_language,
                target_language=request.target_language,
                confidence=1.0,
                cached=False,
                preserved_terms=request.preserve_terms
            )

        # Perform translation
        result = await translation_service.translate(request)

        logger.info(
            f"Translation completed: Cached={result.cached}, "
            f"Confidence={result.confidence}"
        )

        return result

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.post("/batch", response_model=BatchTranslationResponse, status_code=status.HTTP_200_OK)
async def translate_batch(request: BatchTranslationRequest):
    """
    Translate multiple texts in batch.

    Args:
        request: BatchTranslationRequest with list of texts

    Returns:
        BatchTranslationResponse with all translations

    Raises:
        HTTPException: If batch translation fails
    """
    try:
        logger.info(
            f"Batch translation request: {request.source_language} → {request.target_language}, "
            f"Items: {len(request.texts)}"
        )

        # Validate language codes
        valid_languages = {'en', 'ur'}
        if request.source_language not in valid_languages or request.target_language not in valid_languages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid language code. Supported: {valid_languages}"
            )

        # Validate batch size
        if len(request.texts) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch must contain at least one text"
            )

        if len(request.texts) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size exceeds maximum of 100 texts"
            )

        # Perform batch translation
        result = await translation_service.batch_translate(request)

        logger.info(
            f"Batch translation completed: {result.total_count} items, "
            f"{result.cached_count} from cache"
        )

        return result

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Batch translation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch translation failed: {str(e)}"
        )


@router.post("/cache/clear", status_code=status.HTTP_200_OK)
async def clear_translation_cache():
    """
    Clear translation cache.

    Returns:
        Success message
    """
    try:
        old_size = translation_service.get_cache_size()
        translation_service.clear_cache()
        logger.info(f"Translation cache cleared: {old_size} entries removed")

        return {
            "status": "success",
            "message": f"Cache cleared ({old_size} entries)"
        }

    except Exception as e:
        logger.error(f"Failed to clear cache: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )


@router.get("/cache/stats", status_code=status.HTTP_200_OK)
async def get_cache_stats():
    """
    Get translation cache statistics.

    Returns:
        Cache size and statistics
    """
    try:
        cache_size = translation_service.get_cache_size()

        return {
            "cache_size": cache_size,
            "status": "operational"
        }

    except Exception as e:
        logger.error(f"Failed to get cache stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check for translation service."""
    return {
        "status": "healthy",
        "service": "translation",
        "supported_languages": ["en", "ur"],
        "provider": "gemini-2.5-flash"
    }
