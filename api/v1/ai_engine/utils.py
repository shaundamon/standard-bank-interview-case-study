import logging
import torch
import time
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import SearchInteraction, ImageInteraction
from .serializers import (
    ImageSearchRequestSerializer,
    ImageSearchResponseSerializer
)

logger = logging.getLogger(__name__)


class ImageSearchService:
    """Service class containing logic for image searches."""

    def __init__(self, model_handler, vectorstore):
        self.model_handler = model_handler
        self.vectorstore = vectorstore

    def validate_search_request(self, request_data):
        """Validate search request data using serializer."""
        serializer = ImageSearchRequestSerializer(data=request_data)
        if not serializer.is_valid():
            return None, Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return serializer.validated_data, None

    def preprocess_query(self, query: str) -> list:
        """Enhance query with descriptive context."""
        logger.info(f"Preprocessing query: {query}")
        context_templates = [
            f"a photograph of {query}",
            f"a photo showing {query}",
            f"a clear image of {query}",
            f"a scene with {query}",
        ]
        logger.debug(f"Generated templates: {context_templates}")
        return context_templates

    def track_search_interaction(self, request, query, results, processing_time):
        """Track search interaction and results."""
        try:
            interaction = SearchInteraction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                query=query,
                results_count=len(results),
                top_similarity=max([r['similarity']
                                   for r in results]) if results else 0.0,
                model_used=settings.ML_SETTINGS["DEFAULT_MODEL"],
                processing_time=processing_time,
                client_ip=request.META.get('REMOTE_ADDR')
            )

            # Track individual image interactions
            for rank, result in enumerate(results):
                ImageInteraction.objects.create(
                    search=interaction,
                    image_path=result['path'],
                    similarity_score=result['similarity'],
                    rank_position=rank + 1
                )

            return interaction
        except Exception as e:
            logger.error(f"Failed to track interaction: {str(e)}")
            return None

    def search_images(self, request) -> Response:
        """
        Handle image search flow with request validation, query processing, and interaction tracking.

        Args:
            request: HTTP request object containing search query

        Returns:
            Response: JSON response containing search results or error details
        """
        try:
            logger.info("Starting new image search request")
            start_time = time.time()

            logger.debug("Validating search request data")
            validated_data, error_response = self.validate_search_request(
                request.data)
            if error_response:
                logger.warning("Search request validation failed")
                return error_response

            query = validated_data['query']
            top_k = validated_data.get('top_k', settings.ML_SETTINGS["TOP_K"])
            logger.info(f"Processing search for query: '{query}' with top_k={top_k}")

            logger.debug("Generating query templates for semantic search")
            query_templates = self.preprocess_query(query)
            all_embeddings = []
            for template in query_templates:
                logger.debug(f"Encoding template: {template}")
                embedding = self.model_handler.encode_text(template)
                all_embeddings.append(embedding)

            logger.debug("Computing averaged query embedding")
            query_embedding = torch.mean(torch.stack(all_embeddings), dim=0)
            query_embedding = query_embedding / torch.norm(query_embedding)

            logger.info("Searching for similar images...")
            results = self.vectorstore.search(
                query_embedding, top_k=top_k, threshold=0.0)
            logger.info(f"Found {len(results)} matching images")
            logger.debug(f"Search results: {results}")

            processing_time = time.time() - start_time
            logger.info(f"Search completed in {processing_time:.2f} seconds")

            logger.debug("Tracking search interaction in database")
            self.track_search_interaction(
                request, query, results, processing_time)

            logger.debug("Serializing response data")
            response_serializer = ImageSearchResponseSerializer(
                data={'results': results})
            response_serializer.is_valid(raise_exception=True)
            return Response(response_serializer.data)

        except Exception as e:
            logger.error(f"Search failed: {str(e)}", exc_info=True)
            return Response(
                {"error": "Search failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DatasetService:
    """
    Service class containing logic for dataset management.
    """

    def __init__(self, dataset_manager):
        self.dataset_manager = dataset_manager

    def load_dataset_images(self):
        """Load images for dataset info endpoint."""
        try:
            images = self.dataset_manager.load_images()
            if not images:
                logger.warning("No images found in dataset")
                return None
            return images
        except FileNotFoundError as e:
            logger.error(f"Dataset not found: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error loading dataset images: {str(e)}")
            raise

    def trigger_download(self):
        """Trigger dataset download and processing."""
        try:
            logger.info("Starting dataset download")
            self.dataset_manager.download_dataset()
            logger.info("Dataset download completed successfully")
        except Exception as e:
            logger.error(f"Dataset download failed: {str(e)}")
            raise Exception(f"Failed to download dataset: {str(e)}")

    def download_with_progress_generator(self):
        """
        Generator that streams download progress for SSE (Server-Sent Events).
        """
        import json
        yield f"data: {json.dumps({'progress': 0})}\n\n"
        self.dataset_manager.download_dataset()
        yield f"data: {json.dumps({'progress': 100})}\n\n"
        yield f"data: {json.dumps({'status': 'completed'})}\n\n"
