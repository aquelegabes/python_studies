from django.urls import include, path
from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.details, name='details'),
    path('<slug:slug>/inscricao/', views.enrollment, name='enrollment'),
]