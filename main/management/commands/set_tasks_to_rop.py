from django.core.management import BaseCommand

from main.models import Task, User


class Command(BaseCommand):
    help = 'set tasks to ROP'

    def handle(self, *args, **options):
        tasks = Task.objects.filter(is_done=False, date_to__year__gte=2024, date_to__month__gte=1).exclude(
            user__in=User.objects.filter(fired=False))
        for t in tasks:
            print(t.user)
            t.user = User.objects.get(id=64)
            t.save()
        print(tasks.count(), tasks)
