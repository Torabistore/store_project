from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'phone_number', 'message']
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'phone_number': 'شماره تماس',
            'message': 'توضیحات'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09123456789'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'پیام خود را بنویسید...'
            }),
        }
