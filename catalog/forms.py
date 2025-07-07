# catalog/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label='نام',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام شما' # می‌توانید placeholder را اضافه کنید
        })
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com'
        })
    )
    subject = forms.CharField( # این فیلد را اگر می‌خواهید در فرم باشد، نگه دارید
        label='موضوع',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'موضوع پیام'
        })
    )
    message = forms.CharField(
        label='پیام شما', # نام لیبل را مطابق نیاز تغییر دادم
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'پیام خود را اینجا بنویسید'
        })
    )