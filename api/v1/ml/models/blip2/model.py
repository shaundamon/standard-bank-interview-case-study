import logging
import numpy as np
from typing import List, Union
import torch
from PIL import Image
import requests
from ..base import BaseModelHandler
from .config import BLIP2Config

logger = logging.getLogger(__name__)


class BLIP2ModelHandler(BaseModelHandler):
    """Handles BLIP2 model operations for image-text similarity using HF Inference API."""

    def __init__(self, config: BLIP2Config):
        self.config = config
        self.api_url = "https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b"
        self.headers = {"Authorization": f"Bearer {config.api_token}"}
        logger.info("BLIP2 model initialized with API access")

    def encode_text(self, text: str) -> torch.Tensor:
        """Encode text input into embeddings using BLIP2 model."""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": text,
                    "task": "feature-extraction",
                    "options": {"wait_for_model": True}
                },
                timeout=30
            )

            self._check_response(response, "text")

            features = np.array(response.json())
            if isinstance(features, dict):
                logger.error(f"Unexpected API response format: {features}")
                raise RuntimeError(f"Unexpected API response: {features}")

            # Normalize features
            features = features.squeeze()
            features = features / (np.linalg.norm(features, axis=-1, keepdims=True) + 1e-8)
            return torch.from_numpy(features).float()

        except requests.Timeout:
            logger.error("Request to Hugging Face API timed out after 30 seconds")
            raise RuntimeError("BLIP2 API request timed out")
        except Exception as e:
            logger.error(f"Unexpected error during text encoding: {str(e)}")
            raise

    def encode_image(self, images: Union[List[Image.Image], List[str]]) -> torch.Tensor:
        """Encode image input into embeddings using BLIP2 model."""
        try:
            if not images:
                raise ValueError("Empty image list provided")

            # Convert image to bytes
            if isinstance(images[0], str):
                with open(images[0], "rb") as f:
                    image_bytes = f.read()
            elif isinstance(images[0], Image.Image):
                # Convert PIL Image to bytes in PNG format
                import io
                img_byte_arr = io.BytesIO()
                images[0].save(img_byte_arr, format='PNG')
                image_bytes = img_byte_arr.getvalue()
            else:
                raise ValueError(f"Unsupported image type: {type(images[0])}")

            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=image_bytes,
                timeout=30
            )

            self._check_response(response, "image")

            features = np.array(response.json())
            # Add small epsilon to avoid division by zero
            features = features / (np.linalg.norm(features, axis=1, keepdims=True) + 1e-8)
            return torch.from_numpy(features).float()

        except requests.Timeout:
            logger.error("Request to Hugging Face API timed out after 30 seconds")
            raise RuntimeError("BLIP2 API request timed out")
        except Exception as e:
            logger.error(f"Unexpected error during image encoding: {str(e)}")
            raise

    def _check_response(self, response: requests.Response, mode: str) -> None:
        """Check API response status and handle errors."""
        if response.status_code == 503:
            logger.error("Model is loading. Please try again in a few minutes.")
            raise RuntimeError("Model is still loading on Hugging Face servers")
        elif response.status_code != 200:
            logger.error(f"API request failed with status {response.status_code}: {response.text}")
            raise RuntimeError(f"API request failed: {response.text}")

    @property
    def embedding_dim(self) -> int:
        return self.config.embedding_dim
