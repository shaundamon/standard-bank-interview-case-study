from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from v1.ai_engine.views import ImageFileView
from v1.swagger import urlpatterns as swagger_urls 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('v1.ai_engine.urls')),
    path('api/v1/images/<str:filename>', ImageFileView.as_view(), name='serve-image'),
    path('api/', include(swagger_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

