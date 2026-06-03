from django.urls import path
from . import views

app_name = 'laporan'

urlpatterns = [
    path('', views.laporan_index, name='index'),
]
