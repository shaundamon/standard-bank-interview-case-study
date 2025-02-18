"""API URL configuration."""
from django.urls import path
from .views import ImageSearchView, DatasetManagementView

urlpatterns = [
    path('search/', ImageSearchView.as_view(), name='image-search'),
    path('dataset/', DatasetManagementView.as_view(), name='dataset-management'),
    path('dataset/stream/', DatasetManagementView.as_view(
        http_method_names=['get']), name='dataset-stream'),
]
