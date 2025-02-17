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
            # Download dataset using kagglehub
            kagglehub.login()
            dataset = kagglehub.get_kaggle_dataset(self.dataset_name)
            dataset.download(self.dataset_path)
            
            # Extract if downloaded as zip
            zip_path = self.dataset_path / f"{self.dataset_name.split('/')[-1]}.zip"
            if zip_path.exists():
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.dataset_path)
                zip_path.unlink()  # Remove zip after extraction
                
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