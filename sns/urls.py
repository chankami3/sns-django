from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.index, name='post'),
    path('groups', views.index, name='groups'),
]
