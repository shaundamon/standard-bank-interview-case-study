import pytest
from django.urls import reverse
from rest_framework import status
import torch
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_clip_model():
    """Fixture for mocked CLIP model."""
    with patch('api.v1.ai_engine.views.get_clip_model') as mock:
        model = MagicMock()
        model.encode_text.return_value = torch.randn(1, 512)
        mock.return_value = model
        yield model


@pytest.fixture
def mock_embedding_store():
    """Fixture for mocked embedding store."""
    with patch('api.v1.ai_engine.views.EmbeddingStore') as mock:
        store = MagicMock()
        store.search.return_value = [
            {"path": "test1.jpg", "similarity": 0.8},
            {"path": "test2.jpg", "similarity": 0.6}
        ]
        mock.return_value = store
        yield store


def test_search_endpoint_success(api_client, mock_clip_model, mock_embedding_store):
    """Test successful image search."""
    url = reverse('image-search')
    data = {"query": "a photo of a dog"}

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert len(response.data['results']) == 2
    assert all(key in response.data['results'][0]
               for key in ["path", "similarity"])


def test_search_endpoint_missing_query(api_client):
    """Test search with missing query."""
    url = reverse('image-search')
    response = api_client.post(url, {}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data


def test_search_endpoint_model_error(api_client, mock_clip_model):
    """Test search when model fails."""
    url = reverse('image-search')
    mock_clip_model.encode_text.side_effect = Exception("Model error")

    response = api_client.post(url, {"query": "test"}, format='json')

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert 'error' in response.data
