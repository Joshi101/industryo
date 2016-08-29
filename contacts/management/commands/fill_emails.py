from django.core.management.base import BaseCommand, CommandError
from contacts.views import fill_emails_daily


class Command(BaseCommand):
    # args
    help = "checks sendmail model"

    def handle(self, *args, **options):
        fill_emails_daily()
        self.stdout.write("The command has been executed")
