from accounts.models import OTPcode
from datetime import datetime, timedelta
from pytz import timezone
from celery import shared_task


@shared_task
def remove_expired_otp_codes():
    expired_time = datetime.now(tz=timezone('Asia/Tehran')) - timedelta(minutes=2)
    OTPcode.objects.filter(created__lt=expired_time).delete()
