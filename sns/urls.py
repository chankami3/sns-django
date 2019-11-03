from django.urls import path
from . import views

app_name = 'sns'

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('groups', views.groups, name='groups'),
    path('add', views.add, name='add'),
    path('creategroup', views.creategroup, name="creategroup"),
    path('share/<int:share_id>', views.share, name='share'),
    path('good/<int:good_id>', views.good, name='good'),
]
