"""
One-time script to generate and store embeddings for all textbook content.

This script:
1. Reads all MDX files from frontend/docs/
2. Splits content using advanced semantic chunking (preserves code blocks, markdown structure)
3. Generates embeddings using Gemini (gemini-embedding-001, 3072 dimensions)
4. Stores embeddings in Qdrant Cloud with rich metadata

Usage:
    python scripts/generate_embeddings.py
"""

import asyncio
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Dict, List

# Add backend root to path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

from src.services.embeddings import embedding_service
from src.services.vector_db import qdrant_service
from semantic_chunker import SemanticMDXChunker, Chunk


def extract_metadata_from_path(file_path: Path) -> Dict[str, str]:
    """
    Extract module, week information from file path.

    Args:
        file_path: Path to MDX file

    Returns:
        Metadata dictionary
    """
    parts = file_path.parts
    module = "Unknown"
    week = 0

    # Extract module (e.g., Module-1-ROS2)
    for part in parts:
        if part.lower().startswith("module-"):
            module = part.replace("-", " ").title()

        # Extract week number (e.g., week-01-intro.mdx)
        if part.lower().startswith("week-"):
            week_match = re.search(r"week-(\d+)", part, re.IGNORECASE)
            if week_match:
                week = int(week_match.group(1))

    return {"module": module, "week": week, "file_path": str(file_path)}


async def process_mdx_files():
    """Main function to process all MDX files and generate embeddings."""
    print("=" * 70, flush=True)
    print("Starting Advanced Semantic Embedding Generation", flush=True)
    print("=" * 70, flush=True)

    # Initialize semantic chunker
    print("[DEBUG] Initializing semantic chunker...", flush=True)
    chunker = SemanticMDXChunker(
        min_chunk_size=200,
        max_chunk_size=800,
        target_chunk_size=500
    )
    print("[DEBUG] Chunker initialized", flush=True)

    # Find frontend docs directory
    frontend_docs = Path(__file__).parent.parent.parent / "frontend" / "my-website" / "docs"

    if not frontend_docs.exists():
        print(f"[!] Error: Frontend docs directory not found at {frontend_docs}")
        print("Please ensure you have MDX content in frontend/docs/")
        return

    # Create Qdrant collection
    print("\n[+] Creating Qdrant collection...")
    await qdrant_service.create_collection()

    # Find all MDX files
    mdx_files = list(frontend_docs.glob("**/*.mdx")) + list(
        frontend_docs.glob("**/*.md")
    )
    print(f"[+] Found {len(mdx_files)} MDX/MD files\n")

    if len(mdx_files) == 0:
        print("[!] No MDX files found. Please add content to frontend/docs/ first.")
        return

    all_embeddings = []
    total_chunks = 0
    global_chunk_id = 0

    # Statistics tracking
    stats = {
        'total_files': len(mdx_files),
        'total_chunks': 0,
        'total_tokens': 0,
        'chunks_with_code': 0,
        'avg_chunk_size': 0,
        'content_types': {}
    }

    for file_path in mdx_files:
        print(f"\n{'-' * 70}")
        print(f"[*] Processing: {file_path.name}")
        print(f"{'-' * 70}")

        # Extract path metadata
        path_metadata = extract_metadata_from_path(file_path)

        # Use semantic chunker
        try:
            chunks: List[Chunk] = chunker.chunk_file(file_path)
            print(f"  [+] Created {len(chunks)} semantic chunks")

            if not chunks:
                print(f"  [!] No chunks generated for {file_path.name}")
                continue

            # Display chunk statistics
            total_tokens_file = sum(c.token_estimate for c in chunks)
            avg_tokens = total_tokens_file / len(chunks) if chunks else 0
            code_chunks = sum(1 for c in chunks if c.has_code)

            print(f"  [*] Statistics:")
            print(f"     - Total tokens: {total_tokens_file}")
            print(f"     - Avg tokens/chunk: {avg_tokens:.0f}")
            print(f"     - Chunks with code: {code_chunks}")

            # Generate embeddings for all chunks
            chunk_texts = [chunk.content for chunk in chunks]
            print(f"  [~] Generating embeddings (this may take a while)...")

            chunk_embeddings = await embedding_service.generate_embeddings_batch(chunk_texts)

            # Prepare for Qdrant with rich metadata
            for chunk, embedding in zip(chunks, chunk_embeddings):
                global_chunk_id += 1

                # Build comprehensive payload
                payload = {
                    # Path metadata
                    "module": path_metadata["module"],
                    "week": path_metadata["week"],
                    "file_path": str(file_path),
                    "file_name": file_path.name,

                    # Chunk content and metadata
                    "content": chunk.content,
                    "chunk_id": chunk.chunk_id,
                    "position": chunk.position,

                    # Semantic metadata
                    "heading_hierarchy": chunk.heading_hierarchy,
                    "content_type": chunk.content_type,
                    "keywords": chunk.keywords,

                    # Code metadata
                    "has_code": chunk.has_code,
                    "language": chunk.language if chunk.language else "none",
                    "has_links": chunk.has_links,

                    # Size metadata
                    "character_count": chunk.character_count,
                    "token_estimate": chunk.token_estimate,

                    # Section title (for display)
                    "section": file_path.stem.replace("-", " ").title(),
                }

                all_embeddings.append({
                    "id": str(uuid.uuid4()),  # Use UUID instead of integer
                    "vector": embedding,
                    "payload": payload
                })

                # Update statistics
                stats['total_tokens'] += chunk.token_estimate
                stats['chunks_with_code'] += 1 if chunk.has_code else 0
                stats['content_types'][chunk.content_type] = stats['content_types'].get(
                    chunk.content_type, 0
                ) + 1

            total_chunks += len(chunks)
            print(f"  [+] Generated {len(chunks)} embeddings")

        except Exception as e:
            print(f"  [!] Error processing {file_path.name}: {str(e)}")
            continue

    # Update final statistics
    stats['total_chunks'] = total_chunks
    stats['avg_chunk_size'] = stats['total_tokens'] / total_chunks if total_chunks else 0

    # Upload to Qdrant
    if all_embeddings:
        print(f"\n{'=' * 70}")
        print(f"[>>] Uploading {len(all_embeddings)} embeddings to Qdrant...")
        print(f"{'=' * 70}")

        await qdrant_service.upsert_embeddings(all_embeddings)

        print(f"\n[SUCCESS] Embedding generation complete!")
        print(f"\n{'=' * 70}")
        print(f"[STATS] Final Statistics:")
        print(f"{'=' * 70}")
        print(f"  Files processed: {stats['total_files']}")
        print(f"  Total chunks: {stats['total_chunks']}")
        print(f"  Total tokens: {stats['total_tokens']}")
        print(f"  Avg tokens/chunk: {stats['avg_chunk_size']:.0f}")
        print(f"  Chunks with code: {stats['chunks_with_code']}")
        print(f"\n  Content type distribution:")
        for content_type, count in sorted(stats['content_types'].items()):
            print(f"    - {content_type}: {count}")
        print(f"{'=' * 70}\n")
    else:
        print("[!] No embeddings generated. Check your content files.")


if __name__ == "__main__":
    print("[DEBUG] Script starting...", flush=True)
    print("[DEBUG] Running async process...", flush=True)
    asyncio.run(process_mdx_files())
    print("[DEBUG] Process completed", flush=True)
