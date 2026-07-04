from django.shortcuts import render
from django.db.models import Sum, F
from django.utils.timezone import now, timedelta

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
    # Catatan: total_produk, nilai_total, stok_rendah menggambarkan POSISI STOK
    # SAAT INI (bukan aktivitas dalam periode), jadi sengaja tidak ikut filter
    # waktu - filter waktu hanya berlaku untuk data aktivitas/transaksi.
    # =====================
    total_produk = Produk.objects.filter(is_active=True).count()

    total_item = Produk.objects.filter(is_active=True).aggregate(
        total=Sum('stok')
    )['total'] or 0

    nilai_total = Produk.objects.filter(is_active=True).aggregate(
        total=Sum(F('stok') * F('harga_beli'))
    )['total'] or 0

    stok_rendah = Produk.objects.filter(
        is_active=True, stok__lte=F('stok_minimum')
    ).count()

    # =====================
    # BARANG MASUK / KELUAR (mengikuti filter waktu)
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
    # TRANSAKSI DALAM PERIODE (mengikuti filter waktu)
    # =====================
    transaksi_hari_ini = transaksi_qs.count()

    # =====================
    # TRANSAKSI TERBARU (selalu 5 terbaru, tidak terpengaruh filter
    # supaya dashboard tetap menunjukkan aktivitas paling akhir)
    # =====================
    transaksi_terbaru = DetailTransaksi.objects.select_related(
        'transaksi', 'produk'
    ).order_by('-transaksi__tanggal')[:5]

    # =====================
    # PERINGATAN STOK RENDAH
    # =====================
    peringatan_stok = Produk.objects.filter(
        is_active=True, stok__lte=F('stok_minimum')
    ).select_related('kategori')[:10]

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

    # =====================
    # TREN TRANSAKSI 14 HARI TERAKHIR (untuk grafik)
    # =====================
    hari_range = 14
    tanggal_mulai_tren = (waktu - timedelta(days=hari_range - 1)).date()

    tren_qs = (
        DetailTransaksi.objects
        .filter(transaksi__tanggal__date__gte=tanggal_mulai_tren)
        .values('transaksi__tanggal__date', 'transaksi__jenis_transaksi')
        .annotate(total=Sum('jumlah'))
    )

    tren_map = {}
    for row in tren_qs:
        tanggal = row['transaksi__tanggal__date']
        tren_map.setdefault(tanggal, {'MASUK': 0, 'KELUAR': 0})
        tren_map[tanggal][row['transaksi__jenis_transaksi']] = row['total']

    tren_labels = []
    tren_masuk = []
    tren_keluar = []
    for i in range(hari_range):
        tgl = tanggal_mulai_tren + timedelta(days=i)
        tren_labels.append(tgl.strftime('%d/%m'))
        tren_masuk.append(tren_map.get(tgl, {}).get('MASUK', 0))
        tren_keluar.append(tren_map.get(tgl, {}).get('KELUAR', 0))

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
        'tren_labels': tren_labels,
        'tren_masuk': tren_masuk,
        'tren_keluar': tren_keluar,
    }

    return render(request, 'dashboard/index.html', context)
