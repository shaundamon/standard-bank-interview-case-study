"""Helper functions for preprocessing image data."""
import logging
from pathlib import Path
from typing import List, Tuple
from PIL import Image
import torch
from torchvision import transforms

logger = logging.getLogger(__name__)

# Standard image preprocessing for CLIP model
CLIP_IMAGE_SIZE = 224
CLIP_TRANSFORM = transforms.Compose([
    transforms.Resize((CLIP_IMAGE_SIZE, CLIP_IMAGE_SIZE), interpolation=transforms.InterpolationMode.BICUBIC),
    transforms.CenterCrop(CLIP_IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
])

def load_and_preprocess_image(image_path: Path) -> Tuple[torch.Tensor, bool]:
    """
    Load and preprocess a single image for CLIP model input.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (preprocessed_tensor, success_flag)
    """
    try:
        # Open image and convert to RGB
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            
        # Apply CLIP preprocessing
        preprocessed = CLIP_TRANSFORM(img)
        return preprocessed, True
        
    except Exception as e:
        logger.error(f"Failed to preprocess image {image_path}: {str(e)}")
        return None, False

def batch_preprocess_images(image_paths: List[Path], batch_size: int = 32) -> List[torch.Tensor]:
    """
    Preprocess a batch of images in parallel.
    
    Args:
        image_paths: List of paths to image files
        batch_size: Number of images to process at once
        
    Returns:
        List of preprocessed image tensors
    """
    preprocessed_images = []
    failed_images = []
    
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        
        for image_path in batch_paths:
            tensor, success = load_and_preprocess_image(image_path)
            if success:
                preprocessed_images.append(tensor)
            else:
                failed_images.append(image_path)
                
        if failed_images:
            logger.warning(f"Failed to process {len(failed_images)} images")
            
    return torch.stack(preprocessed_images) if preprocessed_images else None
