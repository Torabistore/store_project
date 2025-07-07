# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, AuthenticationForm # AuthenticationForm را اضافه کنید
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['mobile_number', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'mobile_number': 'شماره موبایل',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }

class PasswordResetForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل', max_length=15)

class SetNewPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class LoginForm(AuthenticationForm): # این کلاس را اضافه کنید
    # فیلد username را به mobile_number تغییر لیبل می‌دهیم.
    # خود AuthenticationForm فیلدهای username و password را مدیریت می‌کند.
    username = forms.CharField(label='شماره موبایل', max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اگر می‌خواهید placeholder هم اضافه کنید:
        self.fields['username'].widget.attrs.update({'placeholder': 'شماره موبایل خود را وارد کنید'})
        self.fields['password'].widget.attrs.update({'placeholder': 'رمز عبور خود را وارد کنید'})