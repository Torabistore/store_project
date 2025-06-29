# accounts/backends.py

from django.contrib.auth.backends import BaseBackend
from .models import User

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        این متد برای احراز هویت با شماره همراه به جای نام کاربری است.
        ورودی 'username' در اینجا همان شماره همراهی است که کاربر وارد می‌کند.
        """
        try:
            # ما چک می‌کنیم که آیا کاربری با این شماره همراه وجود دارد یا نه
            user = User.objects.get(mobile_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        این متد برای گرفتن اطلاعات کاربر بعد از ورود موفقیت‌آمیز است.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None