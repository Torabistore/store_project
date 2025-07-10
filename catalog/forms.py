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
                'class': 'w-full px-3 py-2 border border-gray-300 rounded text-gray-800',
                'placeholder': 'نام کامل شما'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded text-gray-800',
                'placeholder': 'مثلاً 09123456789'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded text-gray-800',
                'rows': 5,
                'placeholder': 'پیام خود را وارد کنید...'
            }),
        }
