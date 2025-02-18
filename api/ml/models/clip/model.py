import logging
import numpy as np
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

from .config import CLIPConfig

logger = logging.getLogger(__name__)


class CLIPModelHandler:
    """Handles CLIP model operations for image-text similarity."""

    def __init__(self, config: CLIPConfig):
        """Initialize CLIP model with configuration."""
        self.config = config
        self.device = torch.device(config.device)

        try:
            self.model = CLIPModel.from_pretrained(
                config.model_name).to(self.device)
            self.processor = CLIPProcessor.from_pretrained(config.model_name)
            logger.info(f"CLIP model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {str(e)}")
            raise

    def encode_text(self, text: str) -> torch.Tensor:
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        
        # Normalize features
        text_features = text_features.cpu().numpy()
        text_features = text_features / np.linalg.norm(text_features, axis=1, keepdims=True)
        return torch.from_numpy(text_features)

    def encode_image(self, images: list) -> torch.Tensor:
        # If images are file paths, convert them to PIL images. 
        # This is because of the different vectorstore, so if a new vectorestore is linked, 
        # it will pass the image paths as a list
        if isinstance(images[0], str):
            images = [Image.open(img_path).convert("RGB")
                      for img_path in images]
            
        inputs = self.processor(images=images, return_tensors="pt")
        inputs = {key: tensor.to(self.device)
                  for key, tensor in inputs.items()}
        # Get image features and normalize.
        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)
        outputs = outputs / outputs.norm(dim=-1, keepdim=True)
        return outputs
