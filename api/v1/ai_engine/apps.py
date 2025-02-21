import sys
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class AIEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'v1.ai_engine'

    def ready(self):
        """Initialize dataset when Django starts."""
        # Skip initialization during manage.py test/migrate
        if 'migrate' in sys.argv or 'test' in sys.argv :
            return

        from .utils import DatasetService
        from ..ml.dataset_handler.dataset import DatasetManager

        try:
            dataset_manager = DatasetManager()
            dataset_service = DatasetService(dataset_manager)
            
            # Check if dataset exists
            images = dataset_service.load_dataset_images()
            if not images:
                logger.info("Dataset not found. Starting download...")
                dataset_service.trigger_download()
                # Check again after download
                images = dataset_service.load_dataset_images()
                if images:
                    logger.info(f"Successfully downloaded {len(images)} images")
                else:
                    logger.error("Download completed but no images found")
        except Exception as e:
            logger.error(f"Failed to initialize dataset: {str(e)}")
            raise