from django.core.management.base import BaseCommand, CommandError
from contacts.execution import check_executable


class Command(BaseCommand):
    # args
    help = "checks sendmail model"

    def handle(self, *args, **options):
        check_executable()
        self.stdout.write("The command has been executed")
