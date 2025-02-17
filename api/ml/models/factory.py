from typing import Dict
from .base import BaseModelHandler
from .clip.config import CLIPConfig
from .blip2.config import BLIP2Config
from .clip.model import CLIPModelHandler
from .blip2.model import BLIP2ModelHandler


class ModelFactory:
    """Factory for creating model handlers."""

    @staticmethod
    def create_model(model_type: str, config: Dict) -> BaseModelHandler:
        if model_type == 'clip':
            clip_config = CLIPConfig(
                model_name=config['name'],
                embedding_dim=config['embedding_dim'],
                batch_size=config['batch_size']
            )
            return CLIPModelHandler(clip_config)

        elif model_type == 'blip2':
            blip2_config = BLIP2Config(
                model_name=config['name'],
                embedding_dim=config['embedding_dim'],
                batch_size=config['batch_size']
            )
            return BLIP2ModelHandler(blip2_config)

        else:
            raise ValueError(f"Unknown model type: {model_type}")
