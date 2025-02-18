"""Dataset handling for image retrieval system."""
import logging
from pathlib import Path
from typing import List, Optional
import shutil
import zipfile
import kagglehub
from django.conf import settings

logger = logging.getLogger(__name__)


class DatasetManager:
    """Manages dataset operations including download and preprocessing."""

    def __init__(self):
        self.dataset_path = Path(settings.DATASET_SETTINGS['DATA_PATH'])
        self.sample_size = settings.DATASET_SETTINGS['SAMPLE_SIZE']
        self.dataset_name = "alessandrasala79/ai-vs-human-generated-dataset"

    def download_dataset(self) -> None:
        """Download dataset from Kaggle."""
        try:
            # Create dataset directory if it doesn't exist
            self.dataset_path.parent.mkdir(parents=True, exist_ok=True)

            # Remove existing dataset if any
            if self.dataset_path.exists():
                shutil.rmtree(self.dataset_path)

            # Download dataset using kagglehub
            kagglehub.login()
            dataset = kagglehub.get_kaggle_dataset(self.dataset_name)
            dataset.download(self.dataset_path)

            logger.info(f"Dataset downloaded to {self.dataset_path}")
        except Exception as e:
            logger.error(f"Failed to download dataset: {str(e)}")
            raise

    def load_images(self) -> List[Path]:
        """Load image paths from the dataset directory."""
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset path not found: {self.dataset_path}")
            
        image_paths = list(self.dataset_path.glob("*.jpg"))[:self.sample_size]
        logger.info(f"Found {len(image_paths)} images in {self.dataset_path}")
        return image_paths