from django.urls import path

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('update', views.update_tab, name='update_tab'),
    path('', views.index, name='index')
]
