from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import TrabiUserCreationForm, TrabiLoginForm
from .models import CustomUser
from catalog.models import CustomerDebt, PaymentRequest

class RegisterView(CreateView):
    form_class = TrabiUserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('core:login')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = TrabiLoginForm

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['debt'] = CustomerDebt.objects.filter(user=user).first()
        context['payments'] = PaymentRequest.objects.filter(user=user).order_by('-created_at')
        return context
