from unittest.mock import Mock, patch

from django.test import RequestFactory, TestCase
from metrics.middleware import (
    DatabaseMetricsMiddleware,
    PrometheusAfterMiddleware,
    PrometheusBeforeMiddleware,
)


class PrometheusMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.before_middleware = PrometheusBeforeMiddleware(get_response=Mock())
        self.after_middleware = PrometheusAfterMiddleware(get_response=Mock())

    def test_before_middleware_adds_start_time(self):
        """Test that before middleware adds start time to request."""
        request = self.factory.get("/test/")
        self.before_middleware.process_request(request)

        self.assertTrue(hasattr(request, "_prometheus_start_time"))
        self.assertIsInstance(request._prometheus_start_time, float)

    @patch("metrics.middleware.http_requests_in_progress")
    def test_before_middleware_increments_counter(self, mock_counter):
        """Test that before middleware increments in-progress counter."""
        request = self.factory.get("/test/")
        self.before_middleware.process_request(request)

        mock_counter.inc.assert_called_once()

    @patch("metrics.middleware.http_requests_in_progress")
    def test_after_middleware_decrements_counter(self, mock_counter):
        """Test that after middleware decrements in-progress counter."""
        request = self.factory.get("/test/")
        response = Mock(status_code=200, content=b"test")

        self.after_middleware.process_response(request, response)

        mock_counter.dec.assert_called_once()

    @patch("metrics.middleware.http_requests_total")
    @patch("metrics.middleware.http_request_duration_seconds")
    def test_after_middleware_tracks_metrics(self, mock_duration, mock_total):
        """Test that after middleware tracks request metrics."""
        request = self.factory.get("/test/")
        request._prometheus_start_time = 1000.0
        response = Mock(status_code=200, content=b"test response")

        with patch("time.time", return_value=1001.0):
            self.after_middleware.process_response(request, response)

        # Check that metrics were tracked
        mock_total.labels.assert_called()
        mock_duration.labels.assert_called()

    def test_after_middleware_handles_exception(self):
        """Test that after middleware handles exceptions gracefully."""
        request = self.factory.get("/test/")
        response = Mock(status_code=200)
        # Remove content attribute to cause exception
        delattr(response, "content")

        # Should not raise exception
        result = self.after_middleware.process_response(request, response)
        self.assertEqual(result, response)


class DatabaseMetricsMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DatabaseMetricsMiddleware(get_response=Mock())

    @patch("django.db.connection.queries", [])
    def test_tracks_query_count(self):
        """Test that middleware tracks database query count."""
        request = self.factory.get("/test/")
        response = Mock()

        # Process request
        self.middleware.process_request(request)
        self.assertEqual(request._db_queries_start, 0)

        # Simulate some queries
        from django.db import connection

        with patch.object(
            connection,
            "queries",
            [
                {"sql": "SELECT * FROM users"},
                {"sql": "INSERT INTO logs VALUES (1)"},
                {"sql": "UPDATE users SET active=true"},
            ],
        ):
            with patch("metrics.middleware.db_queries_total") as mock_queries:
                self.middleware.process_response(request, response)

                # Check that queries were counted by type
                calls = mock_queries.labels.call_args_list
                self.assertEqual(len(calls), 3)  # SELECT, INSERT, UPDATE
