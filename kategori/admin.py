from django.contrib import admin
from .models import Kategori

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama_kategori', 'is_active')
    list_filter = ('is_active',)
