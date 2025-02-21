import logging
import os
from django.conf import settings
from django.http import FileResponse, StreamingHttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..ml.dataset_handler.dataset import DatasetManager
from ..ml.models.store_handlers.numpy_store import EmbeddingStore
from ..ml.models.clip import initialize_clip_model
from ..ml.models.store_handlers.faiss_store import FaissVectorStore
from .utils import ImageSearchService, DatasetService

logger = logging.getLogger(__name__)


class ImageSearchView(APIView):
    """
    API endpoint for performing image searches based on text queries.
    
    Provides functionality to search through an image dataset using text descriptions
    and return relevant matches based on semantic similarity.
    """
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        """Initialize the ImageSearchView with required services."""
        super().__init__(*args, **kwargs)
        self.search_service = self._initialize_search_service()

    def _initialize_search_service(self) -> ImageSearchService:
        """
        Initialize the search service with appropriate vector store.
        
        Returns:
            ImageSearchService: Configured service for handling image searches
        """
        model_handler = initialize_clip_model() 
        
        if settings.ML_SETTINGS.get("VECTORSTORE", "numpy") == "faiss":
            vectorstore = FaissVectorStore(
                dimension=settings.ML_SETTINGS['MODELS']['clip']['embedding_dim'],
                store_dir=settings.BASE_DIR / "vectorstore" / "faiss_store",
                model_handler=model_handler,
            )
            logger.info("Using FAISS vector store for similarity search")
        else:
            vectorstore = EmbeddingStore(
                settings.BASE_DIR / "vectorstore" / "embeddings")
            logger.info("Using Numpy-based embedding store for similarity search")

        return ImageSearchService(model_handler, vectorstore)


    @swagger_auto_schema(
        tags=['search'],
        operation_summary="Search images by text description",
        operation_description="Search for images based on a text query using semantic similarity",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['query'],
            properties={
                'query': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Text description to search for'
                ),
                'top_k': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Number of results to return (default: 5)'
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description='Successful search results',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'path': openapi.Schema(type=openapi.TYPE_STRING),
                                    'similarity': openapi.Schema(type=openapi.TYPE_NUMBER)
                                }
                            )
                        )
                    }
                )
            ),
            400: 'Invalid request parameters',
            500: 'Server error during search'
        }
    )
    def post(self, request):
        """
        Search for images based on text query.
        
        Accepts a text query and returns matching images based on semantic similarity.
        """
        return self.search_service.search_images(request)


class DatasetManagementView(APIView):
    """
    API endpoint for managing the image dataset.
    
    Provides functionality to check dataset status, trigger downloads,
    and monitor download progress.
    """
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        """Initialize the DatasetManagementView with required services."""
        super().__init__(*args, **kwargs)
        dataset_manager = DatasetManager()
        self.dataset_service = DatasetService(dataset_manager)

    def get(self, request):
        """
        Get current dataset status.
        
        Returns information about dataset existence, image count, and storage location.
        """        
        try:
            images = self.dataset_service.load_dataset_images()
            return Response(
                {
                    "status": "success",
                    "exists": images is not None,
                    "image_count": len(images) if images else 0,
                    "data_path": str(settings.DATASET_SETTINGS["DATA_PATH"]),
                }
            )
        except Exception as e:
            logger.error(f"Error getting dataset status: {str(e)}")
            return Response(
                {
                    "status": "error",
                    "exists": False,
                    "image_count": 0,
                    "data_path": str(settings.DATASET_SETTINGS["DATA_PATH"]),
                }
            )

    def post(self, request):
        """
        Trigger dataset download and processing.
        
        Initiates the download of the image dataset and starts processing.
        """
        try:
            self.dataset_service.trigger_download()
            return Response({"status": "success", "message": "Dataset download started"})
        except Exception as e:
            logger.error(f"Failed to start dataset download: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_stream(self, request, *args, **kwargs):
        """
        Handle streaming of download progress.
        
        Returns a streaming response with real-time download progress updates.
        """
        response = StreamingHttpResponse(
            streaming_content=self.dataset_service.download_with_progress_generator(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response


class ImageFileView(APIView):
    """
    API endpoint for serving individual image files from the dataset.
    """
    permission_classes = [AllowAny]

    def get(self, request, filename):
        """
        Serve an individual image file.
        
        Args:
            filename (str): Name of the image file to retrieve
            
        Returns:
            FileResponse: The requested image file
        """
        try:
            image_path = os.path.join(
                settings.DATASET_SETTINGS["DATA_PATH"], filename)
            return FileResponse(open(image_path, "rb"), content_type="image/jpeg")
        except Exception as e:
            logger.error(f"Failed to serve image: {str(e)}")
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
