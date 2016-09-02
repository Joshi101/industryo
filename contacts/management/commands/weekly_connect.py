from django.core.management.base import BaseCommand, CommandError
from contacts.weekly_mails import weekly_send


class Command(BaseCommand):
    # args
    help = "checks sendmail model"

    def handle(self, *args, **options):
        weekly_send()
        self.stdout.write("The command has been executed")
