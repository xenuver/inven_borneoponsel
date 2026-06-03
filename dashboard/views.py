from django.shortcuts import render
from django.db.models import Sum, F
from django.utils.timezone import now

from produk.models import Produk
from transaksi.models import Transaksi, DetailTransaksi


def dashboard_index(request):
    # =====================
    # FILTER WAKTU (OPSIONAL)
    # =====================
    filter_waktu = request.GET.get('filter')  # hari | bulan | tahun
    waktu = now()

    transaksi_qs = Transaksi.objects.all()

    if filter_waktu == 'hari':
        transaksi_qs = transaksi_qs.filter(tanggal__date=waktu.date())
    elif filter_waktu == 'bulan':
        transaksi_qs = transaksi_qs.filter(
            tanggal__year=waktu.year,
            tanggal__month=waktu.month
        )
    elif filter_waktu == 'tahun':
        transaksi_qs = transaksi_qs.filter(tanggal__year=waktu.year)

    # =====================
    # CARD STATISTIK
    # =====================
    total_produk = Produk.objects.count()

    total_item = Produk.objects.aggregate(
        total=Sum('stok')
    )['total'] or 0

    nilai_total = Produk.objects.aggregate(
        total=Sum(F('stok') * F('harga_beli'))
    )['total'] or 0

    stok_rendah = Produk.objects.filter(stok__lte=10).count()

    # =====================
    # BARANG MASUK / KELUAR
    # =====================
    barang_masuk = DetailTransaksi.objects.filter(
        transaksi__in=transaksi_qs,
        transaksi__jenis_transaksi='MASUK'
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    barang_keluar = DetailTransaksi.objects.filter(
        transaksi__in=transaksi_qs,
        transaksi__jenis_transaksi='KELUAR'
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    # =====================
    # TRANSAKSI HARI INI
    # =====================
    transaksi_hari_ini = Transaksi.objects.filter(
        tanggal__date=waktu.date()
    ).count()

    # =====================
    # TRANSAKSI TERBARU
    # =====================
    transaksi_terbaru = DetailTransaksi.objects.select_related(
        'transaksi', 'produk'
    ).order_by('-transaksi__tanggal')[:5]

    # =====================
    # PERINGATAN STOK RENDAH
    # =====================
    peringatan_stok = Produk.objects.filter(
        stok__lte=10
    )

    distribusi_kategori = (
        Produk.objects
        .filter(is_active=True)
        .values('kategori__nama_kategori')
        .annotate(
            total_unit=Sum('stok'),
            total_nilai=Sum(F('stok') * F('harga_beli'))
        )
        .order_by('-total_nilai')
    )

    context = {
        'total_produk': total_produk,
        'total_item': total_item,
        'nilai_total': nilai_total,
        'stok_rendah': stok_rendah,
        'barang_masuk': barang_masuk,
        'barang_keluar': barang_keluar,
        'transaksi_hari_ini': transaksi_hari_ini,
        'transaksi_terbaru': transaksi_terbaru,
        'peringatan_stok': peringatan_stok,
        'filter_waktu': filter_waktu,
        'distribusi_kategori': distribusi_kategori,
    }

    return render(request, 'dashboard/index.html', context)
