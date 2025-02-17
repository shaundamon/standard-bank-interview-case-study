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

        if self.embeddings.size == 0:
            self.embeddings = embeddings_np
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings_np])

        # Update metadata
        for idx, path in enumerate(image_paths):
            self.metadata[str(len(self.metadata) + idx)] = {
                "path": str(path),
                "index": len(self.metadata) + idx
            }

        self._save_store()

    def search(self, query_embedding: torch.Tensor, top_k: int = 5) -> List[Dict]:
        if self.embeddings.size == 0:
            return []

        # Convert query embedding to numpy and ensure it's normalized
        query_np = query_embedding.squeeze().numpy()
        if len(query_np.shape) == 1:
            query_np = query_np.reshape(1, -1)
        
        query_np = query_np / np.linalg.norm(query_np, axis=1, keepdims=True)
        
        embeddings_2d = self.embeddings.reshape(self.embeddings.shape[0], -1)
        embeddings_2d = embeddings_2d / np.linalg.norm(embeddings_2d, axis=1, keepdims=True)
        
        # Calculate similarities using dot product of normalized vectors
        similarities = (query_np @ embeddings_2d.T)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                "path": self.metadata[str(idx)]["path"],
                "similarity": float(similarities[idx])
            })

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
