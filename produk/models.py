from django.db import models
from kategori.models import Kategori

class Produk(models.Model):
    KONDISI_CHOICES = (
        ('baru', 'Baru'),
        ('second', 'Second'),
        ('refurbished', 'Refurbished'),
    )

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
    kondisi = models.CharField(
        max_length=15,
        choices=KONDISI_CHOICES,
        default='baru'
    )
    garansi_hari = models.PositiveIntegerField(
        default=0,
        help_text="Lama garansi toko dalam hari. Isi 0 kalau produk ini tidak ada garansi."
    )
    harga_beli = models.DecimalField(max_digits=12, decimal_places=2)
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)
    stok = models.IntegerField(default=0)
    stok_minimum = models.IntegerField(default=5)
    satuan = models.CharField(max_length=20, default='pcs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        harga_lama = None

        if not is_new:
            harga_lama = Produk.objects.filter(pk=self.pk).values(
                'harga_beli', 'harga_jual'
            ).first()

        if not self.kode_produk:
            last_produk = Produk.objects.order_by('-id').first()
            if last_produk and last_produk.kode_produk:
                last_number = int(last_produk.kode_produk.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.kode_produk = f"BRN-{new_number:03d}"

        super().save(*args, **kwargs)

        # Catat riwayat harga kalau harga beli/jual berubah (bukan saat produk baru dibuat)
        if harga_lama and (
            harga_lama['harga_beli'] != self.harga_beli
            or harga_lama['harga_jual'] != self.harga_jual
        ):
            RiwayatHarga.objects.create(
                produk=self,
                harga_beli_lama=harga_lama['harga_beli'],
                harga_beli_baru=self.harga_beli,
                harga_jual_lama=harga_lama['harga_jual'],
                harga_jual_baru=self.harga_jual,
            )

    def __str__(self):
        return f"{self.kode_produk} - {self.nama_produk}"


class RiwayatHarga(models.Model):
    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE,
        related_name='riwayat_harga'
    )
    harga_beli_lama = models.DecimalField(max_digits=12, decimal_places=2)
    harga_beli_baru = models.DecimalField(max_digits=12, decimal_places=2)
    harga_jual_lama = models.DecimalField(max_digits=12, decimal_places=2)
    harga_jual_baru = models.DecimalField(max_digits=12, decimal_places=2)
    diubah_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-diubah_pada']
        verbose_name = 'Riwayat Harga'
        verbose_name_plural = 'Riwayat Harga'

    def __str__(self):
        return f"{self.produk.nama_produk} @ {self.diubah_pada:%d-%m-%Y}"
