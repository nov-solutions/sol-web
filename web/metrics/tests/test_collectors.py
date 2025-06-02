from unittest.mock import Mock, patch

from django.test import TestCase
from metrics.collectors import (
    collect_db_metrics,
    increment_request_metric,
    observe_request_duration,
    track_cache_operation,
    track_custom_metric,
    track_user_activity,
)


class CollectorsTestCase(TestCase):
    @patch("django.db.connection")
    def test_collect_db_metrics(self, mock_connection):
        """Test database metrics collection."""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [42]  # 42 connections
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        with patch("metrics.collectors.db_connections_total") as mock_connections:
            collect_db_metrics()
            mock_connections.set.assert_called_with(42)

    @patch("metrics.collectors.http_requests_total")
    def test_increment_request_metric(self, mock_counter):
        """Test request metric increment."""
        increment_request_metric("GET", "home_view", 200)
        mock_counter.labels.assert_called_with(
            method="GET", view="home_view", status="200"
        )
        mock_counter.labels.return_value.inc.assert_called_once()

    @patch("metrics.collectors.http_request_duration_seconds")
    def test_observe_request_duration(self, mock_histogram):
        """Test request duration observation."""
        observe_request_duration("POST", "api_view", 0.123)
        mock_histogram.labels.assert_called_with(method="POST", view="api_view")
        mock_histogram.labels.return_value.observe.assert_called_with(0.123)

    @patch("metrics.collectors.cache_hits_total")
    @patch("metrics.collectors.cache_misses_total")
    def test_track_cache_operation_get(self, mock_misses, mock_hits):
        """Test cache operation tracking for get operations."""
        # Test cache hit
        track_cache_operation("get", backend="default", hit=True)
        mock_hits.labels.assert_called_with(backend="default")
        mock_hits.labels.return_value.inc.assert_called_once()

        # Test cache miss
        track_cache_operation("get", backend="default", hit=False)
        mock_misses.labels.assert_called_with(backend="default")
        mock_misses.labels.return_value.inc.assert_called_once()

    @patch("metrics.collectors.cache_sets_total")
    def test_track_cache_operation_set(self, mock_sets):
        """Test cache operation tracking for set operations."""
        track_cache_operation("set", backend="redis")
        mock_sets.labels.assert_called_with(backend="redis")
        mock_sets.labels.return_value.inc.assert_called_once()

    @patch("metrics.collectors.user_registrations_total")
    @patch("metrics.collectors.user_logins_total")
    def test_track_user_activity(self, mock_logins, mock_registrations):
        """Test user activity tracking."""
        # Test registration
        track_user_activity("registration")
        mock_registrations.inc.assert_called_once()

        # Test login
        track_user_activity("login", method="social")
        mock_logins.labels.assert_called_with(method="social")
        mock_logins.labels.return_value.inc.assert_called_once()

    @patch("metrics.collectors.custom_metric_counter")
    @patch("metrics.collectors.custom_metric_gauge")
    def test_track_custom_metric(self, mock_gauge, mock_counter):
        """Test custom metric tracking."""
        track_custom_metric("payment", "processed", value=2, gauge_value=150.50)

        mock_counter.labels.assert_called_with(type="payment", action="processed")
        mock_counter.labels.return_value.inc.assert_called_with(2)

        mock_gauge.labels.assert_called_with(type="payment")
        mock_gauge.labels.return_value.set.assert_called_with(150.50)
