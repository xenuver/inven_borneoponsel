from django.db import models
from django.conf import settings


class InfoToko(models.Model):
    nama_toko    = models.CharField(max_length=150, default='Toko Saya')
    alamat       = models.TextField(blank=True)
    telepon      = models.CharField(max_length=20, blank=True)
    email        = models.EmailField(blank=True)
    stok_minimum_default = models.IntegerField(default=5)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Info Toko'

    def __str__(self):
        return self.nama_toko

    @classmethod
    def get(cls):
        """Selalu ambil row pertama, buat jika belum ada."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class LogAktivitas(models.Model):
    AKSI_CHOICES = (
        ('login',   'Login'),
        ('logout',  'Logout'),
        ('tambah',  'Tambah Data'),
        ('ubah',    'Ubah Data'),
        ('hapus',   'Hapus / Nonaktifkan'),
    )

    user      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='log_aktivitas'
    )
    aksi      = models.CharField(max_length=20, choices=AKSI_CHOICES)
    keterangan = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    waktu     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-waktu']
        verbose_name = 'Log Aktivitas'

    def __str__(self):
        return f"{self.user} — {self.aksi} — {self.waktu:%d %b %Y %H:%M}"