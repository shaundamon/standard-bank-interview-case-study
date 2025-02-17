import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Dict
import logging

from ml.data.dataset import DatasetManager
import torch

logger = logging.getLogger(__name__)


class FaissVectorStore:
    """Vector store using FAISS for efficient similarity search.
       If a model_handler is provided on initialization, this class will automatically
       load image paths from the dataset and create embeddings for them.
    """

    def __init__(self, dimension: int, store_dir: Path, model_handler=None):
        self.dimension = dimension
        self.store_dir = store_dir
        self.model_handler = model_handler 
        self.index_file = store_dir / "faiss.index"
        self.metadata_file = store_dir / "faiss_metadata.json"
        self.metadata = {}

        # Create the store directory if it does not exist.
        store_dir.mkdir(parents=True, exist_ok=True)
        self._load_store()

        if self.index.ntotal == 0 and self.model_handler is not None:
            logger.info(
                "FAISS index is empty. Initializing embeddings from dataset.")
            self._initialize_embeddings()

    def _load_store(self) -> None:
        """Load the FAISS index and metadata from disk."""
        if self.index_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            try:
                self.metadata = json.loads(self.metadata_file.read_text())
            except Exception:
                self.metadata = {}
            logger.info(
                f"Loaded FAISS index with {self.index.ntotal} vectors.")
        else:
            self.index = faiss.IndexFlatIP(self.dimension)
            logger.info("Created new FAISS index.")


    def _initialize_embeddings(self) -> None:
        """Initialize embeddings from dataset in batches."""
        dataset = DatasetManager()
        image_paths = dataset.load_images()
        if not image_paths:
            logger.warning(
                "No images found in dataset; cannot initialize embeddings.")
            return

        logger.info(
            f"Initializing embeddings for {len(image_paths)} images from {dataset.dataset_path}")

        # Process images in batches of 32
        batch_size = 32
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i + batch_size]
            logger.info(
                f"Processing batch {i//batch_size + 1} of {len(image_paths)//batch_size + 1}")

            # Get embeddings for the batch
            embeddings = self.model_handler.encode_image(
                [str(path) for path in batch_paths])
            embeddings_np = embeddings.squeeze().cpu().numpy()

            # Normalize embeddings
            norms = np.linalg.norm(embeddings_np, axis=1, keepdims=True)
            embeddings_np = embeddings_np / norms

            metadata_items = []
            for idx, path in enumerate(batch_paths):
                metadata_items.append({
                    "path": str(path),
                    "index": i + idx
                })

            self.add_embeddings(embeddings_np, metadata_items)

        self._save_store()

    def add_embeddings(self, embeddings: np.ndarray, metadata_items: List[Dict]) -> None:
        """
        Add embeddings to the FAISS index.
        
        Args:
            embeddings: A numpy array of shape (n, dimension) containing normalized embeddings.
            metadata_items: A list of dictionaries with metadata for each embedding.
        """
        n = embeddings.shape[0]
        self.index.add(embeddings)
        start_idx = self.index.ntotal - n
        for i, item in enumerate(metadata_items):
            self.metadata[str(start_idx + i)] = item

    def search(self, query_embedding: np.ndarray, top_k: int = 5, threshold: float = 0.0) -> List[Dict]:
        """
        Search for similar embeddings in the FAISS index.
        
        Args:
            query_embedding: A numpy array of shape (1, dimension), normalized.
            top_k: Number of top results to return.
            threshold: Minimum similarity score.
        Returns:
            A list of dictionaries with metadata and similarity scores.
        """
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for sim, idx in zip(distances[0], indices[0]):
            if sim >= threshold:
                results.append({
                    "path": self.metadata.get(str(idx), {}).get("path", "Unknown"),
                    "similarity": float(sim)
                })
        return results

    def _save_store(self) -> None:
        """Save the FAISS index and metadata to disk."""
        faiss.write_index(self.index, str(self.index_file))
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)
        logger.info("Saved FAISS index to disk.")
