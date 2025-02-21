"""Dataset handling for image retrieval system."""
import logging
from pathlib import Path
from typing import List
import shutil
import kagglehub
from django.conf import settings

logger = logging.getLogger(__name__)


class DatasetManager:
    """Manages dataset operations including download and preprocessing."""

    def __init__(self):
        self.dataset_path = Path(settings.DATASET_SETTINGS['DATA_PATH'])
        self.sample_size = settings.DATASET_SETTINGS['SAMPLE_SIZE']
        self.dataset_name = "alessandrasala79/ai-vs-human-generated-dataset"
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        try:
            self.dataset_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create the actual dataset directory if it doesn't exist
            if not self.dataset_path.exists():
                self.dataset_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created dataset directory at {self.dataset_path}")
        except Exception as e:
            logger.error(f"Failed to create dataset directories: {str(e)}")
            raise

    def download_dataset(self) -> None:
        """Download dataset from Kaggle."""
        try:
            self._ensure_directories()

            # Clear existing files
            if any(self.dataset_path.iterdir()):
                logger.info("Removing existing dataset files")
                for item in self.dataset_path.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)

            # Download dataset
            logger.info("Starting dataset download...")
            base_path = kagglehub.dataset_download(self.dataset_name)
            test_data_path = Path(base_path) / "test_data_v2"
            
            if test_data_path.exists():
                # Copy all files from test_data_v2 to our dataset path
                for file_path in test_data_path.glob("*"):
                    if file_path.is_file():
                        shutil.copy2(file_path, self.dataset_path)
                

            logger.info(f"Dataset downloaded to {self.dataset_path}")
        except Exception as e:
            logger.error(f"Failed to download dataset: {str(e)}")
            raise

    def load_images(self) -> List[Path]:
        """Load image paths from the dataset directory."""
        try:
            if not self.dataset_path.exists():
                logger.warning(f"Dataset path does not exist: {self.dataset_path}")
                return None
                
            image_paths = list(self.dataset_path.glob("*.jpg")) + \
                        list(self.dataset_path.glob("*.jpeg")) + \
                        list(self.dataset_path.glob("*.png"))
            
            if not image_paths:
                logger.warning(f"No images found in {self.dataset_path}")
                return None
                
            # Limit to sample size
            image_paths = image_paths[:self.sample_size]
            logger.info(f"Found {len(image_paths)} images in {self.dataset_path}")
            return image_paths
            
        except Exception as e:
            logger.error(f"Error loading images: {str(e)}")
            return None