from django.contrib import admin
from .models import InfoToko, LogAktivitas


@admin.register(InfoToko)
class InfoTokoAdmin(admin.ModelAdmin):
    list_display = ('nama_toko', 'telepon', 'email', 'updated_at')


@admin.register(LogAktivitas)
class LogAktivitasAdmin(admin.ModelAdmin):
    list_display  = ('user', 'aksi', 'keterangan', 'ip_address', 'waktu')
    list_filter   = ('aksi',)
    search_fields = ('user__username', 'keterangan')
    readonly_fields = ('user', 'aksi', 'keterangan', 'ip_address', 'waktu')
