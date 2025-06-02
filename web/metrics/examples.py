"""
Examples of how to use custom metrics in your Django views/models.
"""

from .collectors import track_cache_operation, track_db_operation, track_user_action


# Example 1: Track user actions in views
def example_view(request):
    """Example view showing how to track user actions."""
    from django.http import JsonResponse

    # Track user login action
    if request.method == "POST":
        track_user_action("login", "user_login_view")

    return JsonResponse({"status": "ok"})


# Example 3: Track database operations in models
class ExampleModel:
    """Example showing how to track DB operations."""

    def save(self, *args, **kwargs):
        import time

        start_time = time.time()

        # Perform the actual save
        result = super().save(*args, **kwargs)

        # Track the operation
        duration = time.time() - start_time
        track_db_operation("INSERT", self._meta.db_table, duration)

        return result


# Example 4: Track cache operations
def example_cache_usage():
    """Example showing how to track cache operations."""
    from django.core.cache import cache

    # Track cache set
    cache.set("user_data_123", {"name": "John"}, 300)
    track_cache_operation("set", "user_data")

    # Track cache get
    cache.get("user_data_123")
    track_cache_operation("get", "user_data")


# Example 5: Custom decorator for tracking endpoint usage
def track_endpoint_usage(action_type):
    """Decorator to track specific endpoint usage."""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            from django.urls import resolve

            # Get endpoint name
            resolver_match = resolve(request.path_info)
            endpoint_name = resolver_match.view_name or view_func.__name__

            # Track the action
            track_user_action(action_type, endpoint_name)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# Usage example:
@track_endpoint_usage("api_call")
def my_api_view(request):
    """Example API view with tracking."""
    from django.http import JsonResponse

    return JsonResponse({"data": "example"})
