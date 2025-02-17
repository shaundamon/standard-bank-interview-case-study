import pytest
from pathlib import Path
from django.conf import settings

from ml.models.clip import get_clip_model, initialize_clip_model
from ml.models.clip.config import CLIPConfig


@pytest.fixture
def clip_model():
    """Fixture to provide initialized CLIP model."""
    return initialize_clip_model()


def test_text_encoding(clip_model):
    """Test text encoding functionality."""
    text = "a photo of a cat"
    embeddings = clip_model.encode_text(text)

    assert embeddings.shape[1] == settings.ML_SETTINGS['EMBEDDING_DIM']
    assert embeddings.device.type == 'cpu'


def test_model_singleton():
    """Test that model is a singleton."""
    model1 = get_clip_model()
    model2 = get_clip_model()

    assert model1 is model2
