import pytest
import torch
import numpy as np
from pathlib import Path
from ml.models.embeddings.store import EmbeddingStore


@pytest.fixture
def temp_store_dir(tmp_path):
    """Fixture to provide temporary directory for embedding store."""
    store_dir = tmp_path / "embeddings"
    store_dir.mkdir(parents=True, exist_ok=True)
    return store_dir


@pytest.fixture
def embedding_store(temp_store_dir):
    """Fixture to provide embedding store instance."""
    return EmbeddingStore(temp_store_dir)


def test_add_and_search_embeddings(embedding_store):
    """Test adding embeddings and searching."""
    
    embeddings = torch.randn(3, 512)
    image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]

    # Add embeddings
    embedding_store.add_embeddings(embeddings, image_paths)

    assert len(embedding_store.metadata) == 3
    assert all(str(i) in embedding_store.metadata for i in range(3))

    for i in range(3):
        assert embedding_store.metadata[str(i)]["path"] == image_paths[i]
        assert embedding_store.metadata[str(i)]["index"] == i

    # Test search 
    query = torch.randn(1, 512)
    results = embedding_store.search(query, top_k=2)

    assert len(results) == 2
    assert all(key in results[0] for key in ["path", "similarity"])
    assert isinstance(results[0]["similarity"], float)


def test_empty_store_search(embedding_store):
    """Test searching an empty store."""
    query = torch.randn(1, 512)
    results = embedding_store.search(query, top_k=2)
    assert len(results) == 0
