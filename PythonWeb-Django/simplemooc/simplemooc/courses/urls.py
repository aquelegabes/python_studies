from django.urls import include, path
from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.details, name='details'),
    path('<slug:slug>/inscricao/', views.enrollment, name='enrollment'),
    path('<slug:slug>/cancelar-inscricao/', views.undo_enrollment, name='undo_enrollment'),
    path('<slug:slug>/anuncios/', views.announcements, name='announcements'),
    path('<slug:slug>/anuncios/<int:pk>', views.show_announcement, name='show_announcement'),
    path('<slug:slug>/aulas/', views.lessons, name='lessons'),
    path('<slug:slug>/aulas/<int:pk>', views.lesson, name='lesson'),
]