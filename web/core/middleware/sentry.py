"""
Sentry middleware for enhanced error tracking and user context.
"""

from django.utils.deprecation import MiddlewareMixin
from settings.components.sentry import sentry_add_breadcrumb, sentry_set_user_context


class SentryContextMiddleware(MiddlewareMixin):
    """
    Middleware to automatically set Sentry context for each request.
    """

    def process_request(self, request):
        """Set user context at the beginning of each request."""
        if hasattr(request, "user") and request.user.is_authenticated:
            sentry_set_user_context(request.user)

        # Add breadcrumb for the request
        sentry_add_breadcrumb(
            message=f"{request.method} {request.path}",
            category="request",
            level="info",
            data={
                "method": request.method,
                "path": request.path,
                "query_params": dict(request.GET),
                "content_type": request.content_type,
            },
        )

        return None

    def process_exception(self, request, exception):
        """Add additional context when an exception occurs."""
        # The exception will be automatically captured by Sentry Django integration
        # We just add additional breadcrumbs here
        sentry_add_breadcrumb(
            message=f"Exception in {request.method} {request.path}",
            category="exception",
            level="error",
            data={
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
            },
        )

        return None
