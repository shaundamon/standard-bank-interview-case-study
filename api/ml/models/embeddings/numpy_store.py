"""
Embedding store for managing and searching image embeddings.
"""
import logging
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
import json

logger = logging.getLogger(__name__)


class EmbeddingStore:
    """Manages storage and retrieval of image embeddings."""

    def __init__(self, store_dir: Path):
        """Initialize embedding store."""
        self.store_dir = store_dir
        self.embeddings_file = store_dir / "embeddings.npy"
        self.metadata_file = store_dir / "metadata.json"
        self.embeddings = None
        self.metadata = {}

        # Create store directory if it doesn't exist
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self._load_store()

    def _load_store(self) -> None:
        """Load embeddings and metadata from disk."""
        try:
            if self.embeddings_file.exists():
                self.embeddings = np.load(str(self.embeddings_file))
                self.metadata = json.loads(self.metadata_file.read_text())
                logger.info(
                    f"Loaded {len(self.metadata)} embeddings from store")
            else:
                self.embeddings = np.array([])
                logger.info("Created new embedding store")
        except Exception as e:
            logger.error(f"Failed to load embedding store: {str(e)}")
            raise

    def add_embeddings(self, embeddings: torch.Tensor, image_paths: List[str]) -> None:
        """Add new embeddings to the store."""

        embeddings_np = embeddings.squeeze().numpy()
        if len(embeddings_np.shape) == 1:
            embeddings_np = embeddings_np.reshape(1, -1)
        
        # normalize before storing
        embeddings_np = embeddings_np / \
            np.linalg.norm(embeddings_np, axis=1, keepdims=True)

        if self.embeddings.size == 0:
            self.embeddings = embeddings_np
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings_np])

        # Update metadata
        for idx, path in enumerate(image_paths):
            current_idx = str(idx)  
            self.metadata[current_idx] = {
                "path": str(path),
                "index": idx
            }

        self._save_store()

    def search(self, query_embedding: torch.Tensor, top_k: int = 5, threshold: float = 0.0) -> List[Dict]:
        """
        Retrieve the top_k images whose embeddings are most similar to the query embedding.

        Args:
            query_embedding: Text embedding from your model (should be normalized,
                             but we add an explicit check).
            top_k: Number of top results to return.
            threshold: Minimal similarity score to include a result.
                       Setting this to 0.0 will simply return the top_k.
        Returns:
            A list of dictionaries each containing image path and similarity score.
        """
        if self.embeddings.size == 0:
            logger.warning("Empty embedding store - no images to search")
            return []

        logger.debug(
            f"Searching through {self.embeddings.shape[0]} embeddings")

        # Squeeze and reshape query embedding to (1, -1) and normalize.
        query_np = query_embedding.squeeze().numpy().reshape(1, -1)
        query_norm = np.linalg.norm(query_np, axis=1, keepdims=True)
        if (query_norm == 0).any():
            logger.error("Query embedding norm is zero!")
            return []
        query_np = query_np / query_norm

        # enforce or ensure embeddings are 2D and normalized.
        embeddings_2d = self.embeddings.reshape(self.embeddings.shape[0], -1)
        embeddings_norm = np.linalg.norm(embeddings_2d, axis=1, keepdims=True)
        embeddings_2d = embeddings_2d / embeddings_norm

        # Calculate cosine similarity 
        similarities = cosine_similarity(query_np, embeddings_2d)[0]
        sorted_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in sorted_indices:
            if similarities[idx] >= threshold:
                results.append({
                    "path": self.metadata[str(idx)]["path"],
                    "similarity": float(similarities[idx])
                })
            if len(results) >= top_k:
                break

        logger.info(
            f"Found {len(results)} results above threshold {threshold}")
        return results

    def _save_store(self) -> None:
        """Save embeddings and metadata to disk."""
        try:
            np.save(str(self.embeddings_file), self.embeddings)
            self.metadata_file.write_text(json.dumps(self.metadata, indent=2))
            logger.info("Saved embedding store to disk")
        except Exception as e:
            logger.error(f"Failed to save embedding store: {str(e)}")
            raise
