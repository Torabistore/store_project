from django import forms
from catalog.models import PaymentRequest
from catalog.models import ContactMessage




# ✅ فرم تماس با ما
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

    def clean_message(self):
        msg = self.cleaned_data.get('message', '')
        if len(msg.strip()) < 10:
            raise forms.ValidationError('لطفاً پیام خود را با جزئیات بیشتری بنویسید.')
        return msg

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
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded',
                'placeholder': 'مثلاً 250000'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded',
                'rows': 3,
                'placeholder': 'توضیح پرداخت...'
            }),
            'payment_receipt': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-600'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded',
                'placeholder': 'مثلاً TRB-4523-X'
            })
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('مبلغ باید بیشتر از صفر باشد ❌')
        return amount
