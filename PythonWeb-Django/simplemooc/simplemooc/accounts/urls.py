from django.urls import include, path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('entrar/', LoginView.as_view(template_name='accounts/login.html') , name='login'),
    path('cadastrar/', views.register, name='register'),
]