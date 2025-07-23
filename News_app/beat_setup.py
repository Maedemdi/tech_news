from django_celery_beat.models import IntervalSchedule, PeriodicTask
import json


def scraper_beat_task():

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        name='Run Zoomit Spider',
        defaults={
            'interval': schedule,
            'task': 'News_app.tasks.run_scraper',
            'args': json.dumps([]),
        }
    )