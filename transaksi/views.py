from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from django.db.models import Sum, Q
from django.core.paginator import Paginator
from .models import Transaksi, DetailTransaksi, LogStok
from .forms import BarangMasukForm, BarangKeluarForm



@transaction.atomic
def barang_masuk(request):
    if request.method == "POST":
        form = BarangMasukForm(request.POST)
        if form.is_valid():
            produk = form.cleaned_data['produk']
            jumlah = form.cleaned_data['jumlah']
            keterangan = form.cleaned_data.get('keterangan')

            stok_sebelum = produk.stok

            transaksi = Transaksi.objects.create(
                jenis_transaksi='MASUK',
                keterangan=keterangan,
                user=request.user
            )

            DetailTransaksi.objects.create(
                transaksi=transaksi,
                produk=produk,
                jumlah=jumlah
            )

            produk.stok += jumlah
            produk.save()

            LogStok.objects.create(
                produk=produk,
                perubahan=jumlah,
                stok_sebelum=stok_sebelum,
                stok_sesudah=produk.stok,
                keterangan="Barang masuk"
            )

            messages.success(request, "Barang masuk berhasil disimpan")
            return redirect('transaksi_list')

    return redirect('transaksi_list')

@transaction.atomic
def barang_keluar(request):
    if request.method == "POST":
        form = BarangKeluarForm(request.POST)
        if form.is_valid():
            produk = form.cleaned_data['produk']
            jumlah = form.cleaned_data['jumlah']
            keterangan = form.cleaned_data.get('keterangan')

            if produk.stok < jumlah:
                messages.error(
                    request,
                    f"Stok tidak mencukupi. Stok tersedia: {produk.stok}"
                )
                return redirect('transaksi_list')

            stok_sebelum = produk.stok

            transaksi = Transaksi.objects.create(
                jenis_transaksi='KELUAR',
                keterangan=keterangan,
                user=request.user
            )

            DetailTransaksi.objects.create(
                transaksi=transaksi,
                produk=produk,
                jumlah=jumlah
            )

            produk.stok -= jumlah
            produk.save()

            LogStok.objects.create(
                produk=produk,
                perubahan=-jumlah,
                stok_sebelum=stok_sebelum,
                stok_sesudah=produk.stok,
                keterangan="Barang keluar"
            )

            messages.success(request, "Barang keluar berhasil disimpan")
            return redirect('transaksi_list')

    return redirect('transaksi_list')

def transaksi_list(request):
    filter_tab = request.GET.get('filter', 'semua')

    # queryset utama
    transaksi_qs = DetailTransaksi.objects.select_related(
        'transaksi',
        'produk',
        'transaksi__user'
    ).order_by('-transaksi__tanggal')

    # filter tab
    if filter_tab == 'masuk':
        transaksi_qs = transaksi_qs.filter(
            transaksi__jenis_transaksi='MASUK'
        )
    elif filter_tab == 'keluar':
        transaksi_qs = transaksi_qs.filter(
            transaksi__jenis_transaksi='KELUAR'
        )

    # ===== SUMMARY CARD =====
    total_masuk = DetailTransaksi.objects.filter(
        transaksi__jenis_transaksi='MASUK'
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    total_keluar = DetailTransaksi.objects.filter(
        transaksi__jenis_transaksi='KELUAR'
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    total_transaksi = Transaksi.objects.count()

    # pagination (optional tapi bagus buat performa)
    paginator = Paginator(transaksi_qs, 10)
    page_number = request.GET.get('page')
    transaksi_page = paginator.get_page(page_number)

    context = {
        'transaksi_list': transaksi_page,
        'total_masuk': total_masuk,
        'total_keluar': total_keluar,
        'total_transaksi': total_transaksi,
        'filter_tab': filter_tab,
        'form_masuk': BarangMasukForm(),
        'form_keluar': BarangKeluarForm(),
    }

    return render(request, 'transaksi/transaksi_list.html', context)