"""API views for image retrieval."""

import os
import torch
import logging
from django.conf import settings
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response

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
        logger.info(
            "ImageSearchView initialized with CLIP model and embedding store")

    def preprocess_query(self, query: str) -> list:
        """Enhance query with descriptive context."""
        logger.info(f"Preprocessing query: {query}")
        context_templates = [
            f"a photograph of {query}",
            f"a photo showing {query}",
            f"a clear image of {query}",
            f"a scene with {query}"
        ]
        logger.debug(f"Generated templates: {context_templates}")
        return context_templates

    def post(self, request):
        """Search for images based on text query."""
        try:
            query = request.data.get('query')
            logger.info(f"Received search query: {query}")

            if not query:
                logger.warning("Empty query received")
                return Response(
                    {'error': 'Query is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Process query templates and encode them.
            query_templates = self.preprocess_query(query)
            all_embeddings = []
            for template in query_templates:
                logger.debug(f"Encoding template: {template}")
                embedding = self.clip_model.encode_text(template)
                all_embeddings.append(embedding)

            # Average the embeddings and re-normalize.
            query_embedding = torch.mean(torch.stack(all_embeddings), dim=0)
            query_embedding = query_embedding / torch.norm(query_embedding)

            logger.info("Searching for similar images...")
            results = self.embedding_store.search(
                query_embedding,
                top_k=settings.ML_SETTINGS['TOP_K'],
                threshold=0.0
            )

            logger.info(f"Found {len(results)} matching images")
            logger.debug(f"Search results: {results}")
            return Response({'results': results})

        except Exception as e:
            logger.error(f"Search failed: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Search failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImageFileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, filename):
        try:
            image_path = os.path.join(
                settings.DATASET_SETTINGS['DATA_PATH'], filename)
            return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
        except Exception as e:
            logger.error(f"Failed to serve image: {str(e)}")
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )
