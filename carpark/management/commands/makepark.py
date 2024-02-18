from django.core.management.base import BaseCommand
from carpark.utils import parking


class Command(BaseCommand):
    def handle(self, *args, **options):
        if parking():
            self.stdout.write(self.style.SUCCESS('Park Status Updated'))
        else:
            self.stdout.write(self.style.ERROR('Unable to park'))
