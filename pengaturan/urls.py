from django.urls import path
from . import views

app_name = 'pengaturan'

urlpatterns = [
    path('',                    views.index,            name='index'),

    # Manajemen user
    path('users/',              views.user_list,        name='user_list'),
    path('users/tambah/',       views.user_tambah,      name='user_tambah'),
    path('users/<int:id>/edit/',        views.user_edit,        name='user_edit'),
    path('users/<int:id>/toggle/',      views.user_toggle_aktif, name='user_toggle'),

    # Profil & password
    path('profil/',             views.profil,           name='profil'),
    path('profil/password/',    views.ganti_password,   name='ganti_password'),

    # Info toko
    path('toko/',               views.info_toko,        name='info_toko'),

    # Log aktivitas
    path('log/',                views.log_aktivitas,    name='log'),
]
