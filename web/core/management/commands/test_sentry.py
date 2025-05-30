"""
Management command to test Sentry integration.
"""

import time

import sentry_sdk
from django.conf import settings
from django.core.management.base import BaseCommand
from settings.components.sentry import (
    sentry_add_breadcrumb,
    sentry_capture_exception,
    sentry_capture_message,
    sentry_start_span,
    sentry_start_transaction,
)


class Command(BaseCommand):
    help = "Test Sentry error tracking and performance monitoring"

    def add_arguments(self, parser):
        parser.add_argument(
            "--error",
            action="store_true",
            help="Trigger a test error",
        )
        parser.add_argument(
            "--message",
            action="store_true",
            help="Send a test message",
        )
        parser.add_argument(
            "--performance",
            action="store_true",
            help="Test performance monitoring",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Run all tests",
        )

    def handle(self, *args, **options):
        # Check if Sentry is configured
        if not hasattr(settings, "SENTRY_DSN") or not settings.SENTRY_DSN:
            self.stdout.write(
                self.style.ERROR(
                    "Sentry is not configured. Set SENTRY_DSN environment variable."
                )
            )
            return

        self.stdout.write("Testing Sentry integration...")

        # Get Sentry info
        hub = sentry_sdk.Hub.current
        if hub.client:
            self.stdout.write(f"Sentry DSN: {hub.client.dsn}")
            self.stdout.write(
                f"Environment: {hub.client.options.get('environment', 'unknown')}"
            )
            self.stdout.write(
                f"Release: {hub.client.options.get('release', 'unknown')}"
            )

        run_all = options["all"]

        # Test message capture
        if options["message"] or run_all:
            self.test_message()

        # Test performance monitoring
        if options["performance"] or run_all:
            self.test_performance()

        # Test error capture (do this last as it raises an exception)
        if options["error"] or run_all:
            self.test_error()

        if not any(
            [options["error"], options["message"], options["performance"], run_all]
        ):
            self.stdout.write(
                self.style.WARNING(
                    "No test specified. Use --error, --message, --performance, or --all"
                )
            )

    def test_message(self):
        """Test message capture."""
        self.stdout.write("\nTesting message capture...")

        # Add breadcrumbs
        sentry_add_breadcrumb(
            message="Test command started",
            category="test",
            level="info",
            data={"command": "test_sentry"},
        )

        # Capture different level messages
        messages = [
            ("debug", "Test debug message from Django"),
            ("info", "Test info message from Django"),
            ("warning", "Test warning message from Django"),
            ("error", "Test error message from Django"),
        ]

        for level, message in messages:
            event_id = sentry_capture_message(message, level=level)
            self.stdout.write(
                self.style.SUCCESS(f"Sent {level} message. Event ID: {event_id}")
            )

        # Set custom context
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("test", "true")
            scope.set_tag("test_type", "management_command")
            scope.set_context(
                "test_info",
                {
                    "command": "test_sentry",
                    "purpose": "verify integration",
                },
            )

        self.stdout.write(self.style.SUCCESS("Message test completed"))

    def test_performance(self):
        """Test performance monitoring."""
        self.stdout.write("\nTesting performance monitoring...")

        # Start a transaction
        with sentry_start_transaction(
            name="test_sentry_command", op="management.command"
        ) as transaction:
            transaction.set_tag("test", "true")

            # Simulate some operations with spans
            with sentry_start_span(op="task", description="simulate_processing"):
                self.stdout.write("Simulating data processing...")
                time.sleep(0.1)  # Simulate work

            with sentry_start_span(
                op="db.query", description="simulate_database_query"
            ):
                self.stdout.write("Simulating database query...")
                time.sleep(0.05)  # Simulate query

            with sentry_start_span(op="http.request", description="simulate_api_call"):
                self.stdout.write("Simulating API call...")
                time.sleep(0.2)  # Simulate API call

        self.stdout.write(self.style.SUCCESS("Performance test completed"))

    def test_error(self):
        """Test error capture."""
        self.stdout.write("\nTesting error capture...")

        # Add context before the error
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("test_error", "true")
            scope.set_context(
                "error_test_info",
                {
                    "purpose": "intentional_test_error",
                    "triggered_by": "management_command",
                },
            )

        # Add breadcrumb
        sentry_add_breadcrumb(
            message="About to trigger test error",
            category="test",
            level="warning",
        )

        self.stdout.write(self.style.WARNING("Triggering test exception..."))

        # Raise a test exception
        try:
            # This will be captured by Sentry
            raise Exception("This is a test error from Django management command")
        except Exception as e:
            event_id = sentry_capture_exception(e)
            self.stdout.write(
                self.style.ERROR(
                    f"Test exception raised and captured. Event ID: {event_id}"
                )
            )
            # Re-raise if you want to see the full traceback
            # raise
