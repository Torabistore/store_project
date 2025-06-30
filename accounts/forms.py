# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User 

# Form for password reset request (mobile number input)
class PasswordResetRequestForm(forms.Form):
    mobile_number = forms.CharField(label='شماره همراه', max_length=11)

# Form for OTP verification
class VerifyOTPForm(forms.Form):
    otp_code = forms.CharField(label='کد تأیید', max_length=6, 
                               widget=forms.TextInput(attrs={'placeholder': 'کد ۶ رقمی را وارد کنید'}))

# Custom User Creation Form for Registration
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User 
        fields = ('mobile_number', 'first_name', 'last_name',) 

        labels = {
            'mobile_number': 'شماره همراه',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }
        help_texts = {
            'mobile_number': 'شماره همراه ۱۰ رقمی خود را وارد کنید (مثال: 09123456789).',
        }

# Custom Authentication Form for login based on mobile number
class CustomAuthenticationForm(AuthenticationForm):
    # Passwords should use PasswordInput widget for security.
    # The labels are handled by the template using field.label
    username = forms.CharField(
        label='شماره همراه', 
        widget=forms.TextInput(attrs={'placeholder': 'شماره همراه خود را وارد کنید'}) # <--- اضافه شد
    )
    password = forms.CharField(
        label='گذرواژه', 
        widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه خود را وارد کنید'}) # <--- اضافه شد
    )

    class Meta:
        fields = ['username', 'password']