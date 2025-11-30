"""
Translation models for Urdu translation feature.

This module defines Pydantic models for translation requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class TranslationRequest(BaseModel):
    """Request model for text translation."""

    text: str = Field(..., description="Text to translate", min_length=1, max_length=50000)
    source_language: str = Field(default="en", description="Source language code (en, ur)")
    target_language: str = Field(..., description="Target language code (en, ur)")
    preserve_terms: Optional[List[str]] = Field(
        default=None,
        description="Technical terms to preserve during translation"
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context for better translation accuracy"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "text": "ROS 2 is a powerful robotics framework.",
                "source_language": "en",
                "target_language": "ur",
                "preserve_terms": ["ROS 2"],
                "context": "Technical robotics documentation"
            }
        }


class TranslationResponse(BaseModel):
    """Response model for translation results."""

    original_text: str = Field(..., description="Original text before translation")
    translated_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Translation confidence score (0.0 to 1.0)"
    )
    cached: bool = Field(default=False, description="Whether result was served from cache")
    preserved_terms: Optional[List[str]] = Field(
        default=None,
        description="Terms that were preserved during translation"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "original_text": "ROS 2 is a powerful robotics framework.",
                "translated_text": "ROS 2 ایک طاقتور روبوٹکس فریم ورک ہے۔",
                "source_language": "en",
                "target_language": "ur",
                "confidence": 0.95,
                "cached": False,
                "preserved_terms": ["ROS 2"]
            }
        }


class BatchTranslationRequest(BaseModel):
    """Request model for batch translation of multiple texts."""

    texts: List[str] = Field(..., description="List of texts to translate", max_length=100)
    source_language: str = Field(default="en", description="Source language code")
    target_language: str = Field(..., description="Target language code")
    preserve_terms: Optional[List[str]] = Field(
        default=None,
        description="Technical terms to preserve across all translations"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "texts": [
                    "Welcome to Physical AI",
                    "Learn about robotics",
                    "ROS 2 and Gazebo simulation"
                ],
                "source_language": "en",
                "target_language": "ur",
                "preserve_terms": ["ROS 2", "Gazebo"]
            }
        }


class BatchTranslationResponse(BaseModel):
    """Response model for batch translation results."""

    translations: List[TranslationResponse] = Field(
        ...,
        description="List of translation results"
    )
    total_count: int = Field(..., description="Total number of translations")
    cached_count: int = Field(default=0, description="Number of results from cache")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "translations": [
                    {
                        "original_text": "Welcome to Physical AI",
                        "translated_text": "فزیکل AI میں خوش آمدید",
                        "source_language": "en",
                        "target_language": "ur",
                        "confidence": 0.98,
                        "cached": False
                    }
                ],
                "total_count": 3,
                "cached_count": 0
            }
        }
