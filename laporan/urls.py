from django.urls import path
from . import views

app_name = 'laporan'

urlpatterns = [
    path('', views.laporan_index, name='index'),
    path('export/excel/', views.export_excel, name='export_excel'),
]
