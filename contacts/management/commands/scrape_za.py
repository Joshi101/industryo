from django.core.management.base import BaseCommand, CommandError
from dummy.views import scrape_za


class Command(BaseCommand):
    # args
    help = "checks sendmail model"

    def handle(self, *args, **options):
        scrape_za()
        self.stdout.write("The command has been executed")
