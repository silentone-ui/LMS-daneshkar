from celery import shared_task
import time


@shared_task
def send_otp_code(phone,otp_code):
    print(f'ارسال پیامک به {phone}:کد تایید شما :{otp_code}')

    time.sleep(4)
    return f'OTP code {otp_code} sent to {phone}'