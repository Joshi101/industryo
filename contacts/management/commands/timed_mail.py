from django.core.management.base import BaseCommand, CommandError
from contacts.execution import send_marketing


class Command(BaseCommand):
    # args
    help = "checks sendmail model"

    def handle(self, *args, **options):
        send_marketing()
        self.stdout.write("The command has been executed")
