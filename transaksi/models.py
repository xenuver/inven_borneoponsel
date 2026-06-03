from django.db import models
from accounts.models import User
from produk.models import Produk

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
