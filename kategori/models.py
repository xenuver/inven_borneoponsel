from django.db import models

class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_kategori
