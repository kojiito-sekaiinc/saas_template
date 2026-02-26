from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.billing.models import ProcessedEvent


class Command(BaseCommand):
    help = "Delete ProcessedEvent records older than 90 days"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Delete records older than this many days (default: 90)",
        )

    def handle(self, *args, **options):
        days = options["days"]
        cutoff = timezone.now() - timedelta(days=days)
        count, _ = ProcessedEvent.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(f"Deleted {count} ProcessedEvent records older than {days} days.")
