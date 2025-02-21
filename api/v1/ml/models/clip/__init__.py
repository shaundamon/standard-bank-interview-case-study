import logging
from pathlib import Path
import torch

from django.conf import settings
from .config import CLIPConfig
from .model import CLIPModelHandler

logger = logging.getLogger(__name__)

_model_instance = None


def initialize_clip_model() -> CLIPModelHandler:
    """Initialize and return CLIP model singleton instance."""
    global _model_instance

    if _model_instance is None:
        config = CLIPConfig(
            model_name=settings.ML_SETTINGS['MODELS']['clip']['name'],
            embedding_dim=settings.ML_SETTINGS['MODELS']['clip']['embedding_dim'],
            batch_size=settings.ML_SETTINGS['MODELS']['clip']['batch_size'],
            device="cuda" if torch.cuda.is_available() else "cpu",
            cache_dir=Path(settings.BASE_DIR) / "ml" / "models" / "cache"
        )

        _model_instance = CLIPModelHandler(config)
        logger.info("CLIP model initialized successfully")

    return _model_instance


def get_clip_model() -> CLIPModelHandler:
    """Get the initialized CLIP model instance."""
    if _model_instance is None:
        raise RuntimeError(
            "CLIP model not initialized. Call initialize_clip_model first.")
    return _model_instance
