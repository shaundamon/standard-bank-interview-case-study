import logging
from pathlib import Path
import torch

from django.conf import settings
from .config import BLIP2Config
from .model import BLIP2ModelHandler

logger = logging.getLogger(__name__)

_model_instance = None


def initialize_blip2_model() -> BLIP2ModelHandler:
    """Initialize and return BLIP2 model singleton instance."""
    global _model_instance

    if _model_instance is None:
        config = BLIP2Config(
            model_name=settings.ML_SETTINGS['MODELS']['blip2']['name'],
            embedding_dim=settings.ML_SETTINGS['MODELS']['blip2']['embedding_dim'],
            batch_size=settings.ML_SETTINGS['MODELS']['blip2']['batch_size'],
            device="cuda" if torch.cuda.is_available() else "cpu",
            cache_dir=Path(settings.BASE_DIR) / "ml" / "models" / "cache"
        )

        _model_instance = BLIP2ModelHandler(config)
        logger.info("BLIP2 model initialized successfully")

    return _model_instance


def get_blip2_model() -> BLIP2ModelHandler:
    """Get the initialized BLIP2 model instance."""
    if _model_instance is None:
        raise RuntimeError(
            "BLIP2 model not initialized. Call initialize_blip2_model first.")
    return _model_instance
