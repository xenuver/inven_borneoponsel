from django.db import models
from kategori.models import Kategori

class Produk(models.Model):
    kode_produk = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )
    nama_produk = models.CharField(max_length=150)
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.PROTECT,
        related_name='produk'
    )
    harga_beli = models.DecimalField(max_digits=12, decimal_places=2)
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)
    stok = models.IntegerField(default=0)
    stok_minimum = models.IntegerField(default=5)
    satuan = models.CharField(max_length=20, default='pcs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.kode_produk:
            last_produk = Produk.objects.order_by('-id').first()
            if last_produk and last_produk.kode_produk:
                last_number = int(last_produk.kode_produk.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.kode_produk = f"BRN-{new_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kode_produk} - {self.nama_produk}"
