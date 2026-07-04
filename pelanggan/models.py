from django.db import models


class Pelanggan(models.Model):
    nama = models.CharField(max_length=150)
    telepon = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.telepon})" if self.telepon else self.nama
