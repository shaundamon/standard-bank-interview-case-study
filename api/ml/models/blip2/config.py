import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import torch
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BLIP2Config:
    model_name: str = "Salesforce/blip2-opt-2.7b"
    embedding_dim: int = 768
    batch_size: int = 32
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    cache_dir: Optional[Path] = None
    max_length: int = 77
    api_token: str = os.getenv("HUGGINGFACE_API_TOKEN")
