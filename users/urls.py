from django.urls import path
from .views import RegisterView, CustomLoginView, ProfileView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:homepage'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
