"""Monitoring middleware for API endpoints."""
from django.http import HttpRequest, HttpResponse
import logging
import time
from typing import Callable

logger = logging.getLogger(__name__)

class MonitoringMiddleware:
    """Middleware to monitor API endpoint performance and errors."""

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/api/'):
            start_time = time.time()
            
            response = self.get_response(request)
            
            # Calculate request duration
            duration = time.time() - start_time
            
            log_data = {
                'path': request.path,
                'method': request.method,
                'status_code': response.status_code,
                'duration': f'{duration:.3f}s'
            }
            
            # Log level based on status code
            if response.status_code >= 500:
                logger.error(f'API Error: {log_data}')
            elif response.status_code >= 400:
                logger.warning(f'API Warning: {log_data}')
            else:
                logger.info(f'API Request: {log_data}')
                
            return response
            
        return self.get_response(request)
