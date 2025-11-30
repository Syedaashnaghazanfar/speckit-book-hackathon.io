"""
Response generation service for RAG chatbot.

Uses Google Gemini for grounded, citation-backed responses.
"""

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Dict
import asyncio
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class GenerationService:
    """Generates RAG-grounded responses with citations."""

    SYSTEM_PROMPT = """You are an AI teaching assistant for a Physical AI & Humanoid Robotics textbook.

Your role:
- Answer questions ONLY using information from the provided textbook excerpts
- Always cite sources using [Source: Module X, Week Y - Section Title] format
- If information is not in the provided context, explicitly state: "This information is not covered in the available textbook content."
- Provide clear, educational explanations suitable for students learning robotics
- Include code examples from context when relevant
- Use technical terminology correctly (ROS, URDF, SLAM, etc.)

Guidelines:
- Be concise but thorough
- Use bullet points for multi-part answers
- Highlight key concepts
- Never make up information not in the context
- If context is ambiguous or incomplete, acknowledge limitations
"""

    def __init__(self):
        """Initialize Gemini client."""
        genai.configure(api_key=settings.gemini_api_key)

        # Configure safety settings to be more permissive for educational content
        # Using proper enum types for Gemini API
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = genai.GenerativeModel(
            model_name='models/gemini-2.5-flash',  # Updated to gemini-2.5-flash
            generation_config={
                'temperature': 0.3,  # Low temperature for factual responses
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,  # Increased for longer responses
            },
            safety_settings=safety_settings
        )

    def _format_context(self, retrieved_chunks: List[Dict]) -> str:
        """Format retrieved chunks into context string with citations."""
        if not retrieved_chunks:
            return "No relevant textbook content found."

        context_parts = []

        for i, chunk in enumerate(retrieved_chunks, 1):
            payload = chunk.get('payload', {})

            # Extract metadata
            week = payload.get('week', 0)
            section = payload.get('section', 'Unknown Section')
            content = payload.get('content', '')

            # Format as numbered excerpt
            citation = f"Week {week} - {section}"

            context_parts.append(f"""
[Excerpt {i}] {citation}
{content}
---
""")

        return "\n".join(context_parts)

    def _build_prompt(self, query: str, context: str) -> str:
        """Build full prompt for Gemini."""
        return f"""{self.SYSTEM_PROMPT}

Textbook Excerpts:
{context}

Student Question: {query}

Instructions:
1. Answer the question using ONLY information from the excerpts above
2. Cite each piece of information with [Source: Excerpt X]
3. If the question cannot be answered from the provided context, state: "This information is not covered in the available textbook content."
4. Provide a clear, educational response

Your Answer:"""

    async def generate_response(
        self,
        query: str,
        retrieved_chunks: List[Dict]
    ) -> Dict:
        """
        Generate RAG-grounded response.

        Returns:
        {
            'answer': str,
            'sources': List[Dict],
            'has_answer': bool,
            'confidence': str
        }
        """
        # Format context
        context = self._format_context(retrieved_chunks)

        # Build prompt
        prompt = self._build_prompt(query, context)

        try:
            # Generate response (sync API, run in executor)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )

            # Check if response was blocked by safety filters
            if not response.candidates or not response.candidates[0].content.parts:
                # Safety filter blocked the response
                finish_reason = response.candidates[0].finish_reason if response.candidates else None
                logger.warning(f"Response blocked by safety filter. Finish reason: {finish_reason}")

                # Return a fallback response
                answer_text = "I apologize, but I'm unable to generate a response for this query due to content safety filters. Please try rephrasing your question or ask about a different topic from the textbook."
                has_answer = False
            else:
                answer_text = response.text
                # Parse response to extract citations and assess confidence
                has_answer = "not covered" not in answer_text.lower()

            # Extract sources from citations in response
            sources = []
            for i, chunk in enumerate(retrieved_chunks, 1):
                payload = chunk.get('payload', {})
                sources.append({
                    'excerpt_num': i,
                    'week': payload.get('week', 0),
                    'section': payload.get('section', 'Unknown'),
                    'file_path': payload.get('file_path', ''),
                    'score': chunk.get('score', 0)
                })

            # Assess confidence based on retrieval scores
            avg_score = sum(s['score'] for s in sources) / len(sources) if sources else 0
            confidence = 'high' if avg_score > 0.8 else 'medium' if avg_score > 0.7 else 'low'

            logger.info(f"Generated response - Has answer: {has_answer}, Confidence: {confidence}, Sources: {len(sources)}")

            return {
                'answer': answer_text,
                'sources': sources,
                'has_answer': has_answer,
                'confidence': confidence,
                'num_sources': len(sources)
            }

        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            raise


# Global instance
generation_service = GenerationService()
