"""
Advanced semantic chunking for MDX/Markdown content.

This module implements intelligent chunking that:
- Preserves code blocks intact (fenced or indented)
- Respects markdown structure (headings, lists, tables)
- Maintains heading hierarchy for context
- Splits at natural semantic boundaries
- Optimizes chunks for RAG retrieval (200-800 tokens)
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from pathlib import Path


@dataclass
class Chunk:
    """Represents a semantic chunk of content with metadata."""
    content: str
    heading_hierarchy: List[str]
    content_type: str  # code_example, explanation, reference, tutorial, etc.
    language: Optional[str]  # For code blocks
    keywords: List[str]
    character_count: int
    token_estimate: int
    has_code: bool
    has_links: bool
    position: int  # Sequence in document
    chunk_id: str  # Unique identifier


class SemanticMDXChunker:
    """
    Intelligent chunker for MDX/Markdown content optimized for RAG systems.

    Implements semantic boundary detection and context preservation strategies
    to create chunks that maximize retrieval accuracy.
    """

    def __init__(
        self,
        min_chunk_size: int = 200,
        max_chunk_size: int = 800,
        target_chunk_size: int = 500
    ):
        """
        Initialize the semantic chunker.

        Args:
            min_chunk_size: Minimum tokens per chunk (avoid orphaned fragments)
            max_chunk_size: Maximum tokens per chunk
            target_chunk_size: Target tokens per chunk
        """
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.target_chunk_size = target_chunk_size

        # Patterns for detecting markdown elements
        self.code_fence_pattern = re.compile(r'^```[\w]*\n.*?^```', re.MULTILINE | re.DOTALL)
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.list_pattern = re.compile(r'^[\s]*[-*+]\s+', re.MULTILINE)
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
        self.jsx_component_pattern = re.compile(r'<[A-Z]\w+.*?(?:/>|>.*?</[A-Z]\w+>)', re.DOTALL)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation: 1 token ≈ 0.75 words).

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        # More accurate: count words and adjust for code/special chars
        words = len(text.split())
        # Code typically has more tokens per word
        code_blocks = len(self.code_fence_pattern.findall(text))
        base_tokens = int(words * 1.3)  # Adjusted for technical content
        code_penalty = code_blocks * 50  # Code blocks add tokens
        return base_tokens + code_penalty

    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """
        Extract YAML frontmatter from MDX content.

        Args:
            content: Full MDX content

        Returns:
            Tuple of (frontmatter_dict, content_without_frontmatter)
        """
        frontmatter_pattern = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
        match = frontmatter_pattern.match(content)

        if match:
            frontmatter_text = match.group(1)
            remaining_content = content[match.end():]

            # Parse YAML (simple key: value pairs)
            frontmatter = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')

            return frontmatter, remaining_content

        return None, content

    def detect_code_blocks(self, content: str) -> List[Tuple[int, int]]:
        """
        Detect all code block boundaries (fenced and indented).

        Args:
            content: Markdown content

        Returns:
            List of (start_pos, end_pos) tuples for code blocks
        """
        code_blocks = []

        # Fenced code blocks
        for match in self.code_fence_pattern.finditer(content):
            code_blocks.append((match.start(), match.end()))

        return sorted(code_blocks, key=lambda x: x[0])

    def extract_heading_hierarchy(self, text_before: str) -> List[str]:
        """
        Extract heading hierarchy from text appearing before current chunk.

        Args:
            text_before: All text before the current position

        Returns:
            List of parent headings (e.g., ["Installation", "Prerequisites"])
        """
        headings = []
        current_levels = {}  # Track headings by level

        for match in self.heading_pattern.finditer(text_before):
            level = len(match.group(1))
            title = match.group(2).strip()

            # Update hierarchy
            current_levels[level] = title
            # Clear deeper levels
            keys_to_remove = [k for k in current_levels.keys() if k > level]
            for k in keys_to_remove:
                del current_levels[k]

        # Return in order
        return [current_levels[level] for level in sorted(current_levels.keys())]

    def classify_content_type(self, content: str) -> str:
        """
        Classify the type of content in the chunk.

        Args:
            content: Chunk content

        Returns:
            Content type classification
        """
        # Check for code blocks
        if self.code_fence_pattern.search(content):
            if any(word in content.lower() for word in ['example', 'demo', 'try']):
                return 'code_example'
            return 'code_reference'

        # Check for explanatory content
        if any(word in content.lower() for word in ['what is', 'introduction', 'overview', 'understand']):
            return 'explanation'

        # Check for tutorial content
        if any(word in content.lower() for word in ['step', 'first', 'next', 'then', 'finally']):
            return 'tutorial'

        # Check for reference content
        if any(word in content.lower() for word in ['api', 'function', 'parameter', 'returns']):
            return 'reference'

        return 'general'

    def extract_keywords(self, content: str, max_keywords: int = 10) -> List[str]:
        """
        Extract key terms and concepts from content.

        Args:
            content: Chunk content
            max_keywords: Maximum keywords to extract

        Returns:
            List of extracted keywords
        """
        # Remove code blocks for keyword extraction
        text_only = self.code_fence_pattern.sub('', content)

        # Extract capitalized terms and technical terms
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text_only)

        # Extract words in backticks (inline code)
        inline_code = re.findall(r'`([^`]+)`', text_only)

        # Extract bold/emphasized terms
        emphasized = re.findall(r'\*\*([^*]+)\*\*|\*([^*]+)\*', text_only)
        emphasized_flat = [item for sublist in emphasized for item in sublist if item]

        # Combine and deduplicate
        keywords = list(set(capitalized + inline_code + emphasized_flat))

        # Filter out common words and sort by frequency
        common_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from'}
        keywords = [k for k in keywords if k.lower() not in common_words]

        return keywords[:max_keywords]

    def split_at_heading(self, content: str) -> List[str]:
        """
        Split content at major heading boundaries (H1, H2).

        Args:
            content: Markdown content

        Returns:
            List of sections split by headings
        """
        sections = []
        current_section = []

        lines = content.split('\n')
        for line in lines:
            # Check if line is H1 or H2 heading
            heading_match = re.match(r'^(#{1,2})\s+(.+)$', line)

            if heading_match and current_section:
                # Save previous section
                sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)

        # Add final section
        if current_section:
            sections.append('\n'.join(current_section))

        return sections

    def chunk_large_section(self, section: str, code_blocks: List[Tuple[int, int]]) -> List[str]:
        """
        Chunk a large section while preserving code blocks.

        Args:
            section: Section content
            code_blocks: List of (start, end) positions for code blocks

        Returns:
            List of chunks
        """
        chunks = []
        current_chunk = []
        current_size = 0

        paragraphs = section.split('\n\n')

        for para in paragraphs:
            para_size = self.estimate_tokens(para)

            # Check if paragraph contains code block
            has_code = any(
                section.find(para) >= start and section.find(para) < end
                for start, end in code_blocks
            )

            # If adding this paragraph exceeds target and we have content, split
            if current_size + para_size > self.target_chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size

            # If code block is too large, it gets its own chunk
            if has_code and para_size > self.max_chunk_size:
                if len(current_chunk) > 1:
                    # Save everything before code
                    chunks.append('\n\n'.join(current_chunk[:-1]))
                # Code block as separate chunk
                chunks.append(para)
                current_chunk = []
                current_size = 0

        # Add remaining content
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))

        return chunks

    def chunk_content(self, content: str, source_file: str) -> List[Chunk]:
        """
        Main chunking algorithm with semantic boundary detection.

        Args:
            content: Full MDX/Markdown content
            source_file: Path to source file (for chunk IDs)

        Returns:
            List of semantically coherent chunks with metadata
        """
        # Extract frontmatter
        frontmatter, main_content = self.extract_frontmatter(content)

        # Detect code blocks
        code_blocks = self.detect_code_blocks(main_content)

        # Split at major headings
        sections = self.split_at_heading(main_content)

        all_chunks = []
        position = 0
        accumulated_text = ""

        for section in sections:
            section_size = self.estimate_tokens(section)

            # If section is small enough, keep as single chunk
            if section_size <= self.max_chunk_size:
                section_chunks = [section]
            else:
                # Split large section while preserving code blocks
                section_chunks = self.chunk_large_section(section, code_blocks)

            # Create chunk objects with metadata
            for chunk_content in section_chunks:
                if not chunk_content.strip():
                    continue

                position += 1

                # Extract metadata
                heading_hierarchy = self.extract_heading_hierarchy(accumulated_text)
                content_type = self.classify_content_type(chunk_content)
                keywords = self.extract_keywords(chunk_content)

                # Detect code language
                language = None
                code_match = re.search(r'^```([\w]+)', chunk_content, re.MULTILINE)
                if code_match:
                    language = code_match.group(1)

                # Create chunk
                chunk = Chunk(
                    content=chunk_content,
                    heading_hierarchy=heading_hierarchy,
                    content_type=content_type,
                    language=language,
                    keywords=keywords,
                    character_count=len(chunk_content),
                    token_estimate=self.estimate_tokens(chunk_content),
                    has_code=bool(self.code_fence_pattern.search(chunk_content)),
                    has_links=bool(self.link_pattern.search(chunk_content)),
                    position=position,
                    chunk_id=f"{Path(source_file).stem}-{position:03d}"
                )

                all_chunks.append(chunk)
                accumulated_text += chunk_content + "\n"

        return all_chunks

    def chunk_file(self, file_path: Path) -> List[Chunk]:
        """
        Read and chunk an MDX/Markdown file.

        Args:
            file_path: Path to MDX/MD file

        Returns:
            List of chunks with metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.chunk_content(content, str(file_path))
