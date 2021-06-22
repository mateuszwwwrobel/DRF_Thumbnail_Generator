from django.urls import path
from core import views


urlpatterns = [
    path('create', views.ImageCreateView.as_view(), name='image-create'),
    path('list', views.ImageListView.as_view(), name='image-list'),
]
