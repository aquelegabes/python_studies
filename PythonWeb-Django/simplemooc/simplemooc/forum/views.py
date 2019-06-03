from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ForumView(TemplateView):

    template_name = 'forum/index.html'

index = ForumView.as_view()