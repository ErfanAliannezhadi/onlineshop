from django.core.management.base import BaseCommand
from accounts.models import OTPcode
from datetime import datetime, timedelta
from pytz import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        expired_time = datetime.now(tz=timezone('Asia/Tehran')) - timedelta(minutes=2)
        OTPcode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('all expired otp codes removed')

