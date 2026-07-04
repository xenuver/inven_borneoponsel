from django.db import models
from accounts.models import User
from produk.models import Produk
from supplier.models import Supplier

class Transaksi(models.Model):
    JENIS_CHOICES = (
        ('MASUK', 'Barang Masuk'),
        ('KELUAR', 'Barang Keluar'),
    )

    tanggal = models.DateTimeField(auto_now_add=True)
    jenis_transaksi = models.CharField(
        max_length=10,
        choices=JENIS_CHOICES
    )
    keterangan = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transaksi'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transaksi'
    )

    def __str__(self):
        return f"{self.jenis_transaksi} - {self.tanggal.strftime('%d-%m-%Y')}"

class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(
        Transaksi,
        on_delete=models.CASCADE,
        related_name='detail'
    )
    produk = models.ForeignKey(
        Produk,
        on_delete=models.PROTECT
    )
    jumlah = models.IntegerField()

    def __str__(self):
        return f"{self.produk.nama_produk} ({self.jumlah})"
    
class LogStok(models.Model):
    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE,
        related_name='log_stok'
    )
    perubahan = models.IntegerField()
    stok_sebelum = models.IntegerField()
    stok_sesudah = models.IntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.produk.nama_produk} ({self.perubahan})"


class StokOpname(models.Model):
    """Pencocokan stok sistem vs stok fisik hasil hitung ulang di gudang."""
    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE,
        related_name='stok_opname'
    )
    stok_sistem = models.IntegerField()
    stok_fisik = models.IntegerField()
    selisih = models.IntegerField()
    keterangan = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='stok_opname'
    )
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal']
        verbose_name = 'Stok Opname'
        verbose_name_plural = 'Stok Opname'

    def __str__(self):
        return f"{self.produk.nama_produk} — selisih {self.selisih}"
