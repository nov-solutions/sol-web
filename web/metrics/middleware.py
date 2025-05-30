import time

from django.conf import settings
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from .collectors import (
    http_request_duration_seconds,
    http_request_size_bytes,
    http_requests_in_progress,
    http_requests_total,
    http_response_size_bytes,
)


class PrometheusBeforeMiddleware(MiddlewareMixin):
    """
    Middleware to track metrics at the beginning of request processing.
    This should be placed early in the middleware stack.
    """

    def process_request(self, request):
        request._prometheus_start_time = time.time()
        http_requests_in_progress.inc()

        # Track request size
        content_length = request.META.get("CONTENT_LENGTH", 0)
        if content_length:
            try:
                view_name = self._get_view_name(request)
                http_request_size_bytes.labels(
                    method=request.method, view=view_name
                ).observe(int(content_length))
            except Exception:
                pass

        return None

    def _get_view_name(self, request):
        """Get the view name for the current request."""
        try:
            resolver_match = resolve(request.path_info)
            if resolver_match.view_name:
                return resolver_match.view_name
            elif resolver_match.func:
                return resolver_match.func.__name__
            else:
                return "unknown"
        except Exception:
            return "unknown"


class PrometheusAfterMiddleware(MiddlewareMixin):
    """
    Middleware to track metrics after request processing.
    This should be placed late in the middleware stack.
    """

    def process_response(self, request, response):
        # Decrement in-progress counter
        http_requests_in_progress.dec()

        # Skip metrics for excluded paths
        excluded_paths = getattr(settings, "METRICS_EXCLUDE_PATHS", ["/metrics/"])
        if any(request.path.startswith(path) for path in excluded_paths):
            return response

        try:
            # Get request duration
            if hasattr(request, "_prometheus_start_time"):
                duration = time.time() - request._prometheus_start_time
            else:
                duration = 0

            # Get view name
            view_name = self._get_view_name(request)

            # Track request metrics
            http_requests_total.labels(
                method=request.method,
                view=view_name,
                status=str(response.status_code),
            ).inc()

            # Track duration
            if duration > 0:
                http_request_duration_seconds.labels(
                    method=request.method, view=view_name
                ).observe(duration)

            # Track response size
            if hasattr(response, "content"):
                content_length = len(response.content)
                http_response_size_bytes.labels(
                    method=request.method,
                    view=view_name,
                    status=str(response.status_code),
                ).observe(content_length)

        except Exception:
            pass  # Don't break the response if metrics fail

        return response

    def process_exception(self, request, exception):
        """Handle exceptions to ensure in-progress counter is decremented."""
        http_requests_in_progress.dec()
        return None

    def _get_view_name(self, request):
        """Get the view name for the current request."""
        try:
            resolver_match = resolve(request.path_info)
            if resolver_match.view_name:
                return resolver_match.view_name
            elif resolver_match.func:
                return resolver_match.func.__name__
            else:
                return "unknown"
        except Exception:
            return "unknown"


class DatabaseMetricsMiddleware(MiddlewareMixin):
    """
    Middleware to track database query metrics.
    """

    def process_request(self, request):
        # Reset query count for this request
        if hasattr(request, "_db_queries_start"):
            del request._db_queries_start

        from django.db import connection

        request._db_queries_start = len(connection.queries)
        return None

    def process_response(self, request, response):
        if hasattr(request, "_db_queries_start"):
            from django.db import connection

            from .collectors import db_queries_total

            # Calculate number of queries for this request
            queries_count = len(connection.queries) - request._db_queries_start

            if queries_count > 0:
                # Analyze query types
                select_count = 0
                insert_count = 0
                update_count = 0
                delete_count = 0

                for query in connection.queries[request._db_queries_start :]:
                    sql = query["sql"].upper()
                    if sql.startswith("SELECT"):
                        select_count += 1
                    elif sql.startswith("INSERT"):
                        insert_count += 1
                    elif sql.startswith("UPDATE"):
                        update_count += 1
                    elif sql.startswith("DELETE"):
                        delete_count += 1

                # Update metrics
                if select_count > 0:
                    db_queries_total.labels(operation="SELECT").inc(select_count)
                if insert_count > 0:
                    db_queries_total.labels(operation="INSERT").inc(insert_count)
                if update_count > 0:
                    db_queries_total.labels(operation="UPDATE").inc(update_count)
                if delete_count > 0:
                    db_queries_total.labels(operation="DELETE").inc(delete_count)

        return response
