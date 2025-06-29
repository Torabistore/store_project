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
        # Define the order of fields explicitly
        # UserCreationForm automatically adds 'password' and 'password2'
        fields = ('mobile_number', 'first_name', 'last_name',) # This line is correct.
                                                              # 'password' and 'password2' are implicitly added.
        labels = {
            'mobile_number': 'شماره همراه',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            # 'password' and 'password2' get labels from UserCreationForm by default
        }
        help_texts = {
            'mobile_number': 'شماره همراه ۱۰ رقمی خود را وارد کنید (مثال: 09123456789).',
        }

# If you use a custom authentication form for login based on mobile number
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='شماره همراه') 
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']