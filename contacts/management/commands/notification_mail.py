from django.core.management.base import BaseCommand, CommandError
from activities.views import notification_mails


class Command(BaseCommand):
    # args
    help = "Creates Notification Emails"

    def handle(self, *args, **options):
        notification_mails()
        self.stdout.write("The command has been executed")
