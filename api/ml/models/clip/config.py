from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import torch


@dataclass
class CLIPConfig:
    model_name: str = "openai/clip-vit-base-patch32"
    embedding_dim: int = 512
    batch_size: int = 32
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    cache_dir: Optional[Path] = None
    max_length: int = 77  # CLIP's default max token length
