"""Rate limiting middleware for API endpoints."""
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
import time
from typing import Optional, Callable
from django.http import HttpRequest
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware:
    """Middleware to implement rate limiting for API endpoints."""
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        # Default rate limits (can be overridden in settings)
        self.rate_limit = getattr(settings, 'API_RATE_LIMIT', 100) 
        self.time_window = getattr(settings, 'API_RATE_LIMIT_WINDOW', 3600) 

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/api/v1/search/'):
            if not self._check_rate_limit(request):
                return HttpResponse(
                    'Rate limit exceeded. Please try again later.',
                    status=429
                )
        return self.get_response(request)

    def _check_rate_limit(self, request: HttpRequest) -> bool:
        """
        Check if the request is within rate limits.
        Returns True if request is allowed, False if rate limit exceeded.
        """
        # Use IP address as identifier (can be extended to use API keys/user IDs)
        client_ip = self._get_client_ip(request)
        if not client_ip:
            logger.warning("Could not determine client IP - allowing request")
            return True

        cache_key = f"rate_limit:{client_ip}"
        
        # Get current request count and timestamp
        request_history = cache.get(cache_key)
        current_time = time.time()

        if request_history is None:
            # First request from this IP
            cache.set(
                cache_key,
                {'count': 1, 'window_start': current_time},
                self.time_window
            )
            return True

        # Check if we're in a new time window
        if current_time - request_history['window_start'] > self.time_window:
            cache.set(
                cache_key,
                {'count': 1, 'window_start': current_time},
                self.time_window
            )
            return True

        # Check if rate limit is exceeded
        if request_history['count'] >= self.rate_limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return False

        # Increment request count
        request_history['count'] += 1
        cache.set(cache_key, request_history, self.time_window)
        return True

    def _get_client_ip(self, request: HttpRequest) -> Optional[str]:
        """Get client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
