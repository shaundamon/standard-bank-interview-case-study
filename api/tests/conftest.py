import pytest
from rest_framework.test import APIClient
from django.conf import settings
import os


@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()


@pytest.fixture
def test_image_path(tmp_path):
    """Fixture to provide a test image path."""
    return tmp_path / "test_image.jpg"


@pytest.fixture
def settings_with_test_data(settings):
    """Fixture to override settings for testing."""
    settings.DATASET_SETTINGS = {
        'DATA_PATH': 'tests/test_data',
        'BATCH_SIZE': 32
    }
    settings.ML_SETTINGS = {
        'TOP_K': 5,
        'EMBEDDING_DIM': 512,
        'HF_API_TOKEN': 'test-token'
    }
    return settings


@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path):
    """Setup test environment for all tests."""
    test_data_dir = tmp_path / "test_data"
    test_data_dir.mkdir(parents=True)

    settings.DATASET_SETTINGS = {
        'DATA_PATH': str(test_data_dir)
    }

    settings.ML_SETTINGS = {
        'TOP_K': 5,
        'MODELS': {
            'clip': {
                'name': 'openai/clip-vit-base-patch32',
                'embedding_dim': 512,
                'batch_size': 32
            }
        }
    }

    yield

    # Cleanup
    import shutil
    shutil.rmtree(test_data_dir)
