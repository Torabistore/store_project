import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import PaymentRequest

@receiver(post_save, sender=PaymentRequest)
def handle_payment_status(sender, instance, **kwargs):
    if instance.status in ['approved', 'rejected']:

        # به‌روزرسانی بدهی کاربر در حالت تأیید
        if instance.status == 'approved':
            try:
                from core.models import CustomerDebt
                debt = CustomerDebt.objects.get(user=instance.user)
                debt.total_debt -= instance.amount
                debt.total_debt = max(debt.total_debt, 0)
                debt.save()
            except Exception as e:
                print("❌ خطا در بروزرسانی بدهی:", e)

        # ارسال پیامک اطلاع‌رسانی وضعیت پرداخت
        try:
            status_text = dict(PaymentRequest.STATUS_CHOICES)[instance.status]
            message = f"{instance.user.username} عزیز، پرداخت شما به مبلغ {instance.amount:,} تومان {status_text} شد."
            phone = instance.user.mobile

            send_payment_status_sms(phone, message)  

        except Exception as e:
            print("❌ خطا در ارسال پیامک وضعیت پرداخت:", e)


def send_payment_status_sms(phone, message):
    url = 'https://api.sms.ir/v1/send'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': settings.SMS_API_KEY
    }
    payload = {
        'mobile': phone,
        'message': message
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        print("✅ پیامک وضعیت پرداخت ارسال شد:", result)
        return result
    except Exception as e:
        print("❌ خطا در ارسال پیامک:", e)
        return None
