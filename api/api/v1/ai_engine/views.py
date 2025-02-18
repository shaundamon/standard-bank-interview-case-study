"""API views for image retrieval."""

import os
import torch
import logging
from django.conf import settings
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from ml.models.factory import ModelFactory
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)


class ImageSearchView(APIView):
    """Handle image search requests."""
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Read the default model from settings and obtain its configuration.
        default_model_key = settings.ML_SETTINGS.get('DEFAULT_MODEL')
        model_config = settings.ML_SETTINGS['MODELS'][default_model_key]
        self.model_handler = ModelFactory.create_model(
            default_model_key, model_config)
        logger.info(f"ImageSearchView using model: {default_model_key}")

        # Choose vector store according to settings.
        if settings.ML_SETTINGS.get('VECTORSTORE', 'numpy') == 'faiss':
            from ml.models.vectorstores.faiss_store import FaissVectorStore
            self.vectorstore = FaissVectorStore(
                dimension=model_config['embedding_dim'],
                store_dir=settings.BASE_DIR / "data" / "faiss_store",
                model_handler=self.model_handler
            )
            logger.info("Using FAISS vector store for similarity search")
        else:
            from ml.models.embeddings.store import EmbeddingStore
            self.vectorstore = EmbeddingStore(
                settings.BASE_DIR / "data" / "embeddings")
            logger.info(
                "Using Numpy-based embedding store for similarity search")

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

            # Process query templates and encode
            query_templates = self.preprocess_query(query)
            all_embeddings = []
            for template in query_templates:
                logger.debug(f"Encoding template: {template}")
                embedding = self.model_handler.encode_text(template)
                all_embeddings.append(embedding)

            # Average the embeddings and re-normalize.
            query_embedding = torch.mean(torch.stack(all_embeddings), dim=0)
            query_embedding = query_embedding / torch.norm(query_embedding)

            logger.info("Searching for similar images...")
            results = self.vectorstore.search(
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
