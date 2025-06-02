from django.core.management.base import BaseCommand
from metrics.collectors import collect_db_metrics
from prometheus_client import push_to_gateway


class Command(BaseCommand):
    help = "Export metrics to Prometheus Pushgateway or display them"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pushgateway",
            type=str,
            help="Prometheus Pushgateway URL (e.g., localhost:9091)",
        )
        parser.add_argument(
            "--job",
            type=str,
            default="django_metrics",
            help="Job name for Pushgateway",
        )
        parser.add_argument(
            "--instance",
            type=str,
            help="Instance name for Pushgateway",
        )
        parser.add_argument(
            "--print",
            action="store_true",
            help="Print metrics to stdout instead of pushing",
        )

    def handle(self, *args, **options):
        self.stdout.write("Collecting metrics...")

        # Collect current metrics
        collect_db_metrics()

        if options["print"]:
            # Print metrics to stdout
            from prometheus_client import REGISTRY, generate_latest

            metrics_output = generate_latest(REGISTRY)
            self.stdout.write(metrics_output.decode("utf-8"))
        elif options["pushgateway"]:
            # Push to Prometheus Pushgateway
            try:
                from prometheus_client import REGISTRY

                grouping_key = {"job": options["job"]}
                if options["instance"]:
                    grouping_key["instance"] = options["instance"]

                push_to_gateway(
                    options["pushgateway"], job=options["job"], registry=REGISTRY
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully pushed metrics to {options['pushgateway']}"
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to push metrics: {str(e)}"))
        else:
            self.stdout.write(
                self.style.WARNING("No action specified. Use --print or --pushgateway")
            )
