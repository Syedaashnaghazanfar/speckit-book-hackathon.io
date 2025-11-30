"""
Query preprocessing and enhancement for educational RAG.

Handles:
- Acronym expansion
- Query intent classification
- Metadata filter extraction
"""

from typing import Dict, List
import re
import logging

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Preprocesses and enhances user queries for better retrieval."""

    # Domain-specific acronym expansions
    ACRONYMS = {
        'ros': 'Robot Operating System ROS',
        'ros2': 'Robot Operating System 2 ROS2',
        'urdf': 'Unified Robot Description Format URDF',
        'sdf': 'Simulation Description Format SDF',
        'slam': 'Simultaneous Localization and Mapping SLAM',
        'lidar': 'Light Detection and Ranging LIDAR',
        'imu': 'Inertial Measurement Unit IMU',
        'gpu': 'Graphics Processing Unit GPU',
        'vla': 'Vision-Language-Action VLA',
        'ai': 'Artificial Intelligence AI',
        'ml': 'Machine Learning ML',
        'nn': 'Neural Network NN',
        'cnn': 'Convolutional Neural Network CNN',
        'drl': 'Deep Reinforcement Learning DRL',
        'rl': 'Reinforcement Learning RL',
        'sdk': 'Software Development Kit SDK',
        'api': 'Application Programming Interface API',
    }

    def expand_acronyms(self, query: str) -> str:
        """Expand acronyms to full terms for better semantic matching."""
        expanded = query

        # Find potential acronyms (all caps, 2-5 letters)
        acronym_pattern = r'\b([A-Z]{2,5})\b'

        for match in re.finditer(acronym_pattern, query):
            acronym = match.group(1).lower()
            if acronym in self.ACRONYMS:
                expanded = expanded.replace(
                    match.group(0),
                    self.ACRONYMS[acronym]
                )

        return expanded

    def classify_intent(self, query: str) -> str:
        """
        Classify query intent.

        Returns:
        - 'conceptual': Asking "what is", "explain", "why"
        - 'procedural': Asking "how to", "steps", "tutorial"
        - 'code': Asking for code examples, syntax
        - 'troubleshooting': Error messages, debugging
        - 'general': Everything else
        """
        query_lower = query.lower()

        if any(keyword in query_lower for keyword in ['what is', 'define', 'explain', 'difference between', 'why']):
            return 'conceptual'

        if any(keyword in query_lower for keyword in ['how to', 'how do i', 'steps', 'tutorial', 'guide', 'install']):
            return 'procedural'

        if any(keyword in query_lower for keyword in ['code', 'example', 'syntax', 'implementation', 'snippet']):
            return 'code'

        if any(keyword in query_lower for keyword in ['error', 'issue', 'problem', 'not working', 'fix', 'debug']):
            return 'troubleshooting'

        return 'general'

    def extract_filters(self, query: str) -> Dict[str, any]:
        """
        Extract metadata filters from query.

        Examples:
        - "Week 5 material on navigation" → week=5
        """
        filters = {}
        query_lower = query.lower()

        # Week filter
        week_match = re.search(r'week\s*(\d+)', query_lower)
        if week_match:
            filters['week'] = int(week_match.group(1))

        # Module filter
        module_match = re.search(r'module\s*(\d+)', query_lower)
        if module_match:
            filters['module_num'] = int(module_match.group(1))

        return filters

    def process_query(self, query: str) -> Dict:
        """
        Full query preprocessing pipeline.

        Returns:
        {
            'original_query': str,
            'enhanced_query': str,
            'intent': str,
            'filters': Dict
        }
        """
        # Step 1: Expand acronyms
        enhanced = self.expand_acronyms(query)

        # Step 2: Classify intent
        intent = self.classify_intent(enhanced)

        # Step 3: Extract filters
        filters = self.extract_filters(query)

        logger.info(f"Query processed - Original: '{query}', Enhanced: '{enhanced}', Intent: {intent}")

        return {
            'original_query': query,
            'enhanced_query': enhanced,
            'intent': intent,
            'filters': filters
        }


# Global instance
query_processor = QueryProcessor()
