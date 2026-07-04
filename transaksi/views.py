from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from django.db.models import Sum, Q
from django.core.paginator import Paginator
from accounts.decorators import petugas_required
from pengaturan.utils import catat_aktivitas
from produk.models import Produk
from .models import Transaksi, DetailTransaksi, LogStok, StokOpname
from .forms import BarangMasukForm, BarangKeluarForm, StokOpnameForm



@petugas_required
@transaction.atomic
def barang_masuk(request):
    if request.method == "POST":
        form = BarangMasukForm(request.POST)
        if form.is_valid():
            produk = form.cleaned_data['produk']
            jumlah = form.cleaned_data['jumlah']
            keterangan = form.cleaned_data.get('keterangan')
            supplier = form.cleaned_data.get('supplier')

            stok_sebelum = produk.stok

            transaksi = Transaksi.objects.create(
                jenis_transaksi='MASUK',
                keterangan=keterangan,
                supplier=supplier,
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

            catat_aktivitas(
                request, 'tambah',
                f'Barang masuk: {produk.nama_produk} +{jumlah} {produk.satuan} '
                f'(stok {stok_sebelum} → {produk.stok})'
                + (f', supplier: {supplier.nama_supplier}' if supplier else '')
            )

            messages.success(request, "Barang masuk berhasil disimpan")
            return redirect('transaksi_list')

    return redirect('transaksi_list')

@petugas_required
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

            catat_aktivitas(
                request, 'tambah',
                f'Barang keluar: {produk.nama_produk} -{jumlah} {produk.satuan} '
                f'(stok {stok_sebelum} → {produk.stok})'
            )

            messages.success(request, "Barang keluar berhasil disimpan")
            return redirect('transaksi_list')

    return redirect('transaksi_list')

@petugas_required
def transaksi_list(request):
    filter_tab = request.GET.get('filter', 'semua')
    q = request.GET.get('q', '').strip()
    tanggal_awal = request.GET.get('tanggal_awal', '').strip()
    tanggal_akhir = request.GET.get('tanggal_akhir', '').strip()

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

    # pencarian nama/kode produk
    if q:
        transaksi_qs = transaksi_qs.filter(
            Q(produk__nama_produk__icontains=q) | Q(produk__kode_produk__icontains=q)
        )

    # filter rentang tanggal
    if tanggal_awal:
        transaksi_qs = transaksi_qs.filter(transaksi__tanggal__date__gte=tanggal_awal)
    if tanggal_akhir:
        transaksi_qs = transaksi_qs.filter(transaksi__tanggal__date__lte=tanggal_akhir)

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
        'q': q,
        'tanggal_awal': tanggal_awal,
        'tanggal_akhir': tanggal_akhir,
        'form_masuk': BarangMasukForm(),
        'form_keluar': BarangKeluarForm(),
    }

    return render(request, 'transaksi/transaksi_list.html', context)


@petugas_required
def stok_opname_list(request):
    riwayat = StokOpname.objects.select_related('produk', 'user').order_by('-tanggal')[:100]
    return render(request, 'transaksi/stok_opname.html', {
        'riwayat': riwayat,
        'form': StokOpnameForm(),
    })


@petugas_required
@transaction.atomic
def stok_opname_simpan(request):
    if request.method == 'POST':
        form = StokOpnameForm(request.POST)
        if form.is_valid():
            produk = form.cleaned_data['produk']
            stok_fisik = form.cleaned_data['stok_fisik']
            keterangan = form.cleaned_data.get('keterangan')

            stok_sistem = produk.stok
            selisih = stok_fisik - stok_sistem

            StokOpname.objects.create(
                produk=produk,
                stok_sistem=stok_sistem,
                stok_fisik=stok_fisik,
                selisih=selisih,
                keterangan=keterangan,
                user=request.user,
            )

            if selisih != 0:
                produk.stok = stok_fisik
                produk.save()

                LogStok.objects.create(
                    produk=produk,
                    perubahan=selisih,
                    stok_sebelum=stok_sistem,
                    stok_sesudah=stok_fisik,
                    keterangan=f"Penyesuaian stok opname ({keterangan or 'tanpa keterangan'})"
                )
                catat_aktivitas(
                    request, 'ubah',
                    f'Stok opname: {produk.nama_produk} disesuaikan dari '
                    f'{stok_sistem} menjadi {stok_fisik} (selisih {selisih:+d})'
                )
                messages.success(
                    request,
                    f"Stok opname disimpan. Stok {produk.nama_produk} disesuaikan dari "
                    f"{stok_sistem} menjadi {stok_fisik}."
                )
            else:
                catat_aktivitas(
                    request, 'tambah',
                    f'Stok opname: {produk.nama_produk} sesuai (tidak ada selisih)'
                )
                messages.success(request, f"Stok opname dicatat, stok {produk.nama_produk} sudah sesuai.")

            return redirect('stok_opname_list')

        messages.error(request, "Data stok opname tidak valid.")

    return redirect('stok_opname_list')