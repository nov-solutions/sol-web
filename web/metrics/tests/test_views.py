from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()


class MetricsViewsTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass123"
        )

    def test_metrics_endpoint_unauthorized(self):
        """Test metrics endpoint returns 401 for unauthorized requests."""
        response = self.client.get(reverse("metrics:prometheus-metrics"))
        self.assertEqual(response.status_code, 401)

    @override_settings(METRICS_ALLOWED_IPS=["127.0.0.1"])
    def test_metrics_endpoint_allowed_ip(self):
        """Test metrics endpoint allows requests from allowed IPs."""
        response = self.client.get(
            reverse("metrics:prometheus-metrics"), HTTP_X_FORWARDED_FOR="127.0.0.1"
        )
        # Should work with default test client IP
        self.assertEqual(response.status_code, 200)
        self.assertIn("django_http_requests_total", response.content.decode())

    @override_settings(METRICS_AUTH_TOKEN="secret-token")
    def test_metrics_endpoint_with_token(self):
        """Test metrics endpoint with authentication token."""
        response = self.client.get(
            reverse("metrics:prometheus-metrics"),
            HTTP_X_METRICS_TOKEN="secret-token",
        )
        self.assertEqual(response.status_code, 200)

    def test_metrics_endpoint_superuser(self):
        """Test metrics endpoint allows authenticated superusers."""
        self.client.login(username="admin", password="testpass123")
        response = self.client.get(reverse("metrics:prometheus-metrics"))
        self.assertEqual(response.status_code, 200)

    def test_health_check_endpoint(self):
        """Test health check endpoint returns proper status."""
        response = self.client.get(reverse("metrics:health-check"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("checks", data)
        self.assertIn("response_time_ms", data)

    def test_readiness_check_endpoint(self):
        """Test readiness check endpoint."""
        response = self.client.get(reverse("metrics:readiness-check"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ready")

    def test_liveness_check_endpoint(self):
        """Test liveness check endpoint."""
        response = self.client.get(reverse("metrics:liveness-check"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "alive")


class MetricsContentTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass123"
        )
        self.client.login(username="admin", password="testpass123")

    def test_metrics_content(self):
        """Test that metrics endpoint returns expected metrics."""
        response = self.client.get(reverse("metrics:prometheus-metrics"))
        content = response.content.decode()

        # Check for expected metrics
        expected_metrics = [
            "django_app_info",
            "django_http_requests_total",
            "django_http_request_duration_seconds",
            "django_process_memory_bytes",
            "django_db_connections_total",
        ]

        for metric in expected_metrics:
            self.assertIn(metric, content, f"Expected metric {metric} not found")

    def test_request_tracking(self):
        """Test that requests are tracked in metrics."""
        # Make some requests
        self.client.get(reverse("metrics:health-check"))
        self.client.get(reverse("metrics:liveness-check"))

        # Get metrics
        response = self.client.get(reverse("metrics:prometheus-metrics"))
        content = response.content.decode()

        # Check that our requests were tracked
        self.assertIn("django_http_requests_total", content)
        self.assertIn('view="health-check"', content)
