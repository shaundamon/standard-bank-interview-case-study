from abc import ABC, abstractmethod
import torch
from typing import List, Union
from PIL import Image


class BaseModelHandler(ABC):
    """Base class for all model handlers."""

    @abstractmethod
    def encode_text(self, text: str) -> torch.Tensor:
        """Encode text query into embeddings."""
        pass

    @abstractmethod
    def encode_image(self, images: Union[List[Image.Image], List[str]]) -> torch.Tensor:
        """Encode images into embeddings."""
        pass

    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Return embedding dimension."""
        pass
