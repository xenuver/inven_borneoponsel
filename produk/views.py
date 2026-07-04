from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import models
from accounts.decorators import admin_required, petugas_required
from pengaturan.utils import catat_aktivitas
from .models import Produk
from .forms import ProdukForm
from kategori.models import Kategori


@petugas_required
def produk_list(request):
    tab = request.GET.get('tab', 'aktif')
    q = request.GET.get('q', '').strip()

    if tab == 'nonaktif':
        produk = Produk.objects.filter(is_active=False).select_related('kategori')
    else:
        produk = Produk.objects.filter(is_active=True).select_related('kategori')

    if q:
        produk = produk.filter(
            models.Q(nama_produk__icontains=q) | models.Q(kode_produk__icontains=q)
        )

    return render(request, 'produk/list.html', {
        'produk': produk,
        'tab': tab,
        'q': q,
    })


@admin_required
def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            produk = form.save()
            catat_aktivitas(
                request, 'tambah',
                f'Tambah produk: {produk.nama_produk} ({produk.kode_produk})'
            )
            return redirect('produk:list')
    else:
        form = ProdukForm()

    return render(request, 'produk/form.html', {
        'form': form,
        'kategori': Kategori.objects.filter(is_active=True),
        'title': 'Tambah Produk'
    })


@admin_required
def produk_edit(request, id):
    produk = get_object_or_404(Produk, id=id)

    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            produk = form.save()
            catat_aktivitas(
                request, 'ubah',
                f'Edit produk: {produk.nama_produk} ({produk.kode_produk})'
            )
            return redirect('produk:list')
    else:
        form = ProdukForm(instance=produk)

    return render(request, 'produk/form.html', {
        'form': form,
        'produk': produk,
        'kategori': Kategori.objects.filter(is_active=True),
        'title': 'Edit Produk'
    })


@admin_required
@require_POST
def produk_nonaktif(request, id):
    produk = get_object_or_404(Produk, id=id)
    produk.is_active = False
    produk.save()
    catat_aktivitas(
        request, 'hapus',
        f'Nonaktifkan produk: {produk.nama_produk} ({produk.kode_produk})'
    )
    return redirect('produk:list')


@admin_required
@require_POST
def produk_aktifkan(request, id):
    produk = get_object_or_404(Produk, id=id)
    produk.is_active = True
    produk.save()
    catat_aktivitas(
        request, 'ubah',
        f'Aktifkan kembali produk: {produk.nama_produk} ({produk.kode_produk})'
    )
    return redirect('/produk/?tab=nonaktif')


@petugas_required
def riwayat_harga(request, id):
    produk = get_object_or_404(Produk, id=id)
    riwayat = produk.riwayat_harga.all()
    return render(request, 'produk/riwayat_harga.html', {
        'produk': produk,
        'riwayat': riwayat,
    })