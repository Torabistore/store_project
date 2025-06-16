# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(UserCreationForm):
    # فیلدهای اضافی برای ثبت نام
    first_name = forms.CharField(label=_('نام'), max_length=30, required=True)
    last_name = forms.CharField(label=_('نام خانوادگی'), max_length=30, required=True)

    class Meta:
        model = User
        fields = ('mobile_number', 'first_name', 'last_name') # فیلدهایی که در فرم ثبت نام ظاهر می‌شوند