import pytest
from PIL import Image
import numpy as np
from ml.models.clip import  initialize_clip_model


@pytest.fixture(autouse=True)
def setup_clip_settings(settings):
    """Setup test settings for CLIP model."""
    settings.ML_SETTINGS = {
        'MODELS': {
            'clip': {
                'name': "openai/clip-vit-base-patch32",
                'embedding_dim': 512,
                'batch_size': 32
            }
        }
    }


@pytest.fixture
def clip_model():
    """Fixture to provide initialized CLIP model."""
    return initialize_clip_model()


def test_text_encoding(clip_model):
    """Test text encoding functionality."""
    text = "a photo of a cat"
    embeddings = clip_model.encode_text(text)

    assert embeddings.shape[1] == 512
    assert embeddings.device.type == 'cpu'


def test_image_encoding(clip_model, tmp_path):
    """Test image encoding functionality."""
    # Create a dummy image for testing


    img = Image.fromarray(np.random.randint(
        0, 255, (224, 224, 3), dtype=np.uint8))
    embeddings = clip_model.encode_image([img])

    assert embeddings.shape[1] == 512
    assert embeddings.device.type == 'cpu'
