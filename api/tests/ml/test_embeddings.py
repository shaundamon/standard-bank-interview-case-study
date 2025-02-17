"""Tests for embedding store functionality."""
import pytest
import torch
import numpy as np
from pathlib import Path
from ml.models.embeddings.store import EmbeddingStore


@pytest.fixture
def temp_store_dir(tmp_path):
    """Fixture to provide temporary directory for embedding store."""
    return tmp_path / "embeddings"


@pytest.fixture
def embedding_store(temp_store_dir):
    """Fixture to provide embedding store instance."""
    return EmbeddingStore(temp_store_dir)


def test_add_and_search_embeddings(embedding_store):
    """Test adding embeddings and searching."""
    # Create dummy embeddings
    embeddings = torch.randn(3, 512) 
    image_paths = [
        "image1.jpg",
        "image2.jpg",
        "image3.jpg"
    ]

    # Add embeddings
    embedding_store.add_embeddings(embeddings, image_paths)

    # Search with query
    query = torch.randn(1, 512)
    results = embedding_store.search(query, top_k=2)

    assert len(results) == 2
    assert "path" in results[0]
    assert "similarity" in results[0]
    assert isinstance(results[0]["similarity"], float)


def test_persistence(temp_store_dir):
    """Test that embeddings persist between store instances."""
    store1 = EmbeddingStore(temp_store_dir)
    embeddings = torch.randn(2, 512)
    paths = ["test1.jpg", "test2.jpg"]
    store1.add_embeddings(embeddings, paths)

    # Create new instance
    store2 = EmbeddingStore(temp_store_dir)
    assert len(store2.metadata) == 2
