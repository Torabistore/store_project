# accounts/forms.py

from django import forms

# فرم مرحله اول: گرفتن شماره همراه
class PasswordResetRequestForm(forms.Form):
    mobile_number = forms.CharField(
        label="شماره همراه", 
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09...'})
    )

# فرم مرحله دوم: گرفتن کد تایید
class VerifyOTPForm(forms.Form):
    otp_code = forms.CharField(
        label="کد تایید ۶ رقمی", 
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ارسال شده را وارد کنید'})
    )