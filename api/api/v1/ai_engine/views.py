"""API views for image retrieval."""
from django.http import FileResponse
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

from ml.models.clip import get_clip_model
from ml.models.embeddings.store import EmbeddingStore
from rest_framework.permissions import AllowAny
from ml.data.dataset import DatasetManager

logger = logging.getLogger(__name__)


class ImageSearchView(APIView):
    """Handle image search requests."""
    permission_classes = [AllowAny]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clip_model = get_clip_model()
        self.embedding_store = EmbeddingStore(
            settings.BASE_DIR / "data" / "embeddings"
        )

    def post(self, request):
        """Search for images based on text query."""
        try:
            query = request.data.get('query')
            if not query:
                return Response(
                    {'error': 'Query is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Encode query text
            query_embedding = self.clip_model.encode_text(query)

            # Search for similar images
            results = self.embedding_store.search(
                query_embedding,
                top_k=settings.ML_SETTINGS['TOP_K']
            )

            return Response({'results': results})

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return Response(
                {'error': 'Search failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ImageFileView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, filename):
        try:
            image_path = os.path.join(settings.DATASET_SETTINGS['DATA_PATH'], filename)
            return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
        except Exception as e:
            logger.error(f"Failed to serve image: {str(e)}")
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )