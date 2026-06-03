from django.shortcuts import render
from django.db.models import Sum, F, Count
from produk.models import Produk
from transaksi.models import Transaksi, DetailTransaksi

def laporan_index(request):


    # =====================
    # A. RINGKASAN INVENTORY
    # =====================
    total_item = Produk.objects.aggregate(
        total=Sum('stok')
    )['total'] or 0

    total_nilai_inventory = Produk.objects.aggregate(
        total=Sum(F('stok') * F('harga_beli'))
    )['total'] or 0


    # =====================
    # B. BARANG MASUK
    # =====================
    transaksi_masuk = Transaksi.objects.filter(jenis_transaksi='MASUK')

    total_transaksi_masuk = transaksi_masuk.count()

    total_unit_masuk = DetailTransaksi.objects.filter(
        transaksi__jenis_transaksi='MASUK'
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    total_nilai_masuk = DetailTransaksi.objects.filter(
        transaksi__jenis_transaksi='MASUK'
    ).aggregate(
        total=Sum(F('jumlah') * F('produk__harga_beli'))
    )['total'] or 0


    # =====================
    # C. BARANG KELUAR
    # =====================
    transaksi_keluar = Transaksi.objects.filter(jenis_transaksi='KELUAR')

    total_transaksi_keluar = transaksi_keluar.count()

    total_unit_keluar = DetailTransaksi.objects.filter(
        transaksi__jenis_transaksi='KELUAR'
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    total_nilai_keluar = DetailTransaksi.objects.filter(
        transaksi__jenis_transaksi='KELUAR'
    ).aggregate(
        total=Sum(F('jumlah') * F('produk__harga_beli'))
    )['total'] or 0


    # =====================
    # D. NILAI INVENTORY PER KATEGORI
    # =====================
    nilai_per_kategori = (
        Produk.objects
        .filter(is_active=True)
        .values('kategori__nama_kategori')
        .annotate(
            total_unit=Sum('stok'),
            total_nilai=Sum(F('stok') * F('harga_beli'))
        )
        .order_by('-total_nilai')
    )


    # =====================
    # E. RINGKASAN PRODUK
    # =====================
    ringkasan_produk = (
        DetailTransaksi.objects
        .values('produk__nama_produk')
        .annotate(
            jumlah_transaksi=Count('id'),
            total_unit=Sum('jumlah'),
            total_nilai=Sum(F('jumlah') * F('produk__harga_beli'))
        )
        .order_by('-total_nilai')
    )


    # =====================
    # F. PRODUK DENGAN NILAI TERTINGGI (TOP 5)
    # =====================
    produk_tertinggi = (
        Produk.objects
        .annotate(
            total_nilai=F('stok') * F('harga_beli')
        )
        .order_by('-total_nilai')[:5]
    )


    context = {
        'total_item': total_item,
        'total_nilai_inventory': total_nilai_inventory,

        'total_transaksi_masuk': total_transaksi_masuk,
        'total_unit_masuk': total_unit_masuk,
        'total_nilai_masuk': total_nilai_masuk,

        'total_transaksi_keluar': total_transaksi_keluar,
        'total_unit_keluar': total_unit_keluar,
        'total_nilai_keluar': total_nilai_keluar,

        'nilai_per_kategori': nilai_per_kategori,
        'ringkasan_produk': ringkasan_produk,
        'produk_tertinggi': produk_tertinggi,
    }

    return render(request, 'laporan/index.html', context)
