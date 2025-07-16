from django import forms
from django.contrib.auth.forms import SetPasswordForm
from users.models import CustomUser
from core.models import PaymentRequest
from django.contrib.auth.forms import AuthenticationForm


# ✅ فرم ورود با شماره همراه
class TrabiLoginForm(AuthenticationForm):
    phone_number = forms.CharField(label='شماره همراه')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)

    def authenticate(self):
        from django.contrib.auth import authenticate
        return authenticate(
            phone_number=self.cleaned_data['phone_number'],
            password=self.cleaned_data['password']
        )


# ✅ فرم بازیابی رمز عبور با شماره همراه
class PasswordResetForm(forms.Form):
    phone_number = forms.CharField(label='شماره همراه')

    def clean_phone_number(self):
        number = self.cleaned_data['phone_number']
        try:
            user = CustomUser.objects.get(phone_number=number)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('کاربری با این شماره پیدا نشد ❌')
        self.cleaned_data['user'] = user
        return number


# ✅ فرم تأیید کد یکبار مصرف (OTP)
class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(label='کد تأیید')


# ✅ فرم ثبت رمز جدید
class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewPasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = 'رمز جدید'
        self.fields['new_password2'].label = 'تکرار رمز جدید'
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''


# ✅ فرم تماس با ما
class ContactForm(forms.Form):
    full_name = forms.CharField(label='نام کامل')
    email = forms.EmailField(label='ایمیل')
    phone = forms.CharField(label='شماره تماس', required=False)
    message = forms.CharField(label='پیام شما', widget=forms.Textarea)

    def clean(self):
        cleaned = super().clean()
        if len(cleaned.get('message', '')) < 10:
            raise forms.ValidationError('لطفاً پیام خود را دقیق‌تر و با جزئیات بنویسید.')
        return cleaned


# ✅ فرم درخواست پرداخت بدهی
class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['amount', 'description', 'payment_receipt', 'reference_number']
        labels = {
            'amount': 'مبلغ پرداختی',
            'description': 'توضیحات',
            'payment_receipt': 'تصویر فیش پرداخت',
            'reference_number': 'شماره پیگیری'
        }
        help_texts = {
            'amount': '',
            'description': '',
            'payment_receipt': '',
            'reference_number': ''
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('مبلغ باید بیشتر از صفر باشد ❌')
        return amount


# ✅ فرم ویرایش پروفایل کاربر
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone_number': 'شماره همراه'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره همراه'}),
        }
