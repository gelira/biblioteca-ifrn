from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask

class Command(BaseCommand):
    def handle(self, *args, **options):
        PeriodicTask.objects.filter(enabled=True, one_off=True)\
            .update(last_run_at=None, total_run_count=0)
