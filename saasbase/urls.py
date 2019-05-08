from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('logged_out/',
        TemplateView.as_view(template_name='saasbase/logged_out.html')),
]
