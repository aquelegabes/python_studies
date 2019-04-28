from django.urls import include, path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contact, name='contact'),
]