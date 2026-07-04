from django.db import models


class Supplier(models.Model):
    nama_supplier = models.CharField(max_length=150)
    kontak_person = models.CharField(max_length=100, blank=True)
    telepon = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    alamat = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nama_supplier']

    def __str__(self):
        return self.nama_supplier
