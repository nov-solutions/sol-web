from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from metrics.models import MetricEvent, ServiceHealthCheck


class Command(BaseCommand):
    help = "Clean up old metric records from the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=getattr(settings, "METRICS_RETENTION_DAYS", 7),
            help="Number of days to retain metrics (default: 7)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )

    def handle(self, *args, **options):
        retention_days = options["days"]
        dry_run = options["dry_run"]

        cutoff_date = timezone.now() - timedelta(days=retention_days)

        self.stdout.write(
            f"Cleaning up metrics older than {retention_days} days "
            f"(before {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')})"
        )

        # Clean up MetricEvent records
        old_events = MetricEvent.objects.filter(timestamp__lt=cutoff_date)
        events_count = old_events.count()

        if events_count > 0:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f"Would delete {events_count} metric event records"
                    )
                )
            else:
                old_events.delete()
                self.stdout.write(
                    self.style.SUCCESS(f"Deleted {events_count} metric event records")
                )
        else:
            self.stdout.write("No old metric events to delete")

        # Clean up ServiceHealthCheck records
        old_health_checks = ServiceHealthCheck.objects.filter(
            checked_at__lt=cutoff_date
        )
        health_checks_count = old_health_checks.count()

        if health_checks_count > 0:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f"Would delete {health_checks_count} health check records"
                    )
                )
            else:
                old_health_checks.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Deleted {health_checks_count} health check records"
                    )
                )
        else:
            self.stdout.write("No old health check records to delete")

        # Summary
        total_deleted = events_count + health_checks_count
        if total_deleted > 0 and not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"\nTotal records deleted: {total_deleted}")
            )
        elif dry_run and total_deleted > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"\nTotal records that would be deleted: {total_deleted}"
                )
            )
