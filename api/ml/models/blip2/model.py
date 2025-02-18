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
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": text,
                    "task": "feature-extraction",
                    "options": {"wait_for_model": True}
                },
            )

            if response.status_code == 503:
                logger.error(
                    "Model is loading. Please try again in a few minutes.")
                raise RuntimeError(
                    "Model is still loading on Hugging Face servers")
            elif response.status_code != 200:
                logger.error(
                    f"API request failed with status {response.status_code}: {response.text}")
                raise RuntimeError(f"API request failed: {response.text}")

            features = np.array(response.json())
            if isinstance(features, dict):
                logger.error(f"Unexpected API response format: {features}")
                raise RuntimeError(f"Unexpected API response: {features}")

            features = features.squeeze()
            features = features / np.linalg.norm(features, axis=-1, keepdims=True)
            return torch.from_numpy(features)

        except requests.Timeout:
            logger.error("Request to Hugging Face API timed out after 30 seconds")
            raise RuntimeError("BLIP2 API request timed out")
        except Exception as e:
            logger.error(f"Unexpected error during text encoding: {str(e)}")
            raise


    def encode_image(self, images: Union[List[Image.Image], List[str]]) -> torch.Tensor:
        try:
            if isinstance(images[0], str):
                with open(images[0], "rb") as f:
                    image_bytes = f.read()
            else:
                image_bytes = images[0].tobytes()

            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=image_bytes,
                timeout=30  # 30 second timeout
            )

            if response.status_code == 503:
                logger.error(
                    "Model is loading. Please try again in a few minutes.")
                raise RuntimeError(
                    "Model is still loading on Hugging Face servers")
            elif response.status_code != 200:
                logger.error(
                    f"API request failed with status {response.status_code}: {response.text}")
                raise RuntimeError(f"API request failed: {response.text}")

            features = np.array(response.json())
            features = features / np.linalg.norm(features, axis=1, keepdims=True)
            return torch.from_numpy(features)

        except requests.Timeout:
            logger.error("Request to Hugging Face API timed out after 30 seconds")
            raise RuntimeError("BLIP2 API request timed out")
        except Exception as e:
            logger.error(f"Unexpected error during image encoding: {str(e)}")
            raise

    @property
    def embedding_dim(self) -> int:
        return self.config.embedding_dim
