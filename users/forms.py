from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import CustomUser


# ✅ فرم ثبت‌نام کاربر
class TrabiUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره همراه',
            'email': 'ایمیل',
            'password1': 'رمز عبور',
            'password2': 'تکرار رمز عبور',
        }
        help_texts = {field: '' for field in fields}


# ✅ فرم ورود با شماره همراه
class TrabiLoginForm(forms.Form):
    phone_number = forms.CharField(label='شماره همراه')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        phone = cleaned.get('phone_number')
        pwd = cleaned.get('password')

        if phone and pwd:
            from django.contrib.auth import authenticate
            user = authenticate(phone_number=phone, password=pwd)
            if not user:
                raise forms.ValidationError('شماره یا رمز نادرست است ❌')
            cleaned['user'] = user
        return cleaned


# ✅ فرم ویرایش پروفایل کاربر
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone_number': 'شماره همراه',
            'profile_image': 'تصویر پروفایل',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ✅ فرم بازیابی رمز با شماره همراه
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


# ✅ فرم تأیید کد یکبار مصرف
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
