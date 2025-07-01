# D:\store_project\catalog\forms.py

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label='نام و نام خانوادگی', 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'نام کامل خود را وارد کنید'
        })
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'example@domain.com'
        })
    )
    subject = forms.CharField(
        label='موضوع', 
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'موضوع پیام'
        })
    )
    message = forms.CharField(
        label='پیام شما',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 5, 
            'placeholder': 'پیام خود را اینجا بنویسید'
        })
    )