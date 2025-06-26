from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        label="نام کامل"
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'full_name', 'password1', 'password2')
        labels = {
            'phone_number': 'شماره همراه',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user
