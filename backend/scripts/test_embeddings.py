"""
Test script to verify Gemini embedding generation works correctly.

Usage:
    python scripts/test_embeddings.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend root to path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

from src.services.embeddings import embedding_service


async def test_single_embedding():
    """Test generating a single embedding."""
    print("Testing single embedding generation...")

    test_text = "ROS 2 is a robotic middleware framework for building robot applications."

    try:
        embedding = await embedding_service.generate_embedding(test_text)
        print(f"[OK] Single embedding generated successfully!")
        print(f"   Dimension: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
        return True
    except Exception as e:
        print(f"[FAIL] Single embedding failed: {str(e)}")
        return False


async def test_batch_embeddings():
    """Test generating embeddings in batch."""
    print("\nTesting batch embedding generation...")

    test_texts = [
        "Physical AI combines artificial intelligence with robotics.",
        "URDF is the Unified Robot Description Format for ROS.",
        "Gazebo is a robot simulation environment.",
        "NVIDIA Isaac provides GPU-accelerated robotics tools.",
        "Humanoid robots are designed to mimic human form and movement."
    ]

    try:
        embeddings = await embedding_service.generate_embeddings_batch(test_texts)
        print(f"[OK] Batch embeddings generated successfully!")
        print(f"   Number of embeddings: {len(embeddings)}")
        print(f"   Dimension of each: {len(embeddings[0])}")
        print(f"   First embedding preview: {embeddings[0][:5]}")
        return True
    except Exception as e:
        print(f"[FAIL] Batch embedding failed: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Gemini Embedding Service Test")
    print("=" * 60)

    single_ok = await test_single_embedding()
    batch_ok = await test_batch_embeddings()

    print("\n" + "=" * 60)
    if single_ok and batch_ok:
        print("SUCCESS: All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("WARNING: Some tests failed. Check your configuration:")
        print("   - Ensure GEMINI_API_KEY is set in .env")
        print("   - Verify API key has access to gemini-embedding-001 model")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
