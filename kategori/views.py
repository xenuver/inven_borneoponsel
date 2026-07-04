from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.decorators import admin_required, petugas_required
from pengaturan.utils import catat_aktivitas
from .models import Kategori


@petugas_required
def kategori_list(request):
    kategori = Kategori.objects.filter(is_active=True)
    return render(request, 'kategori/list.html', {
        'kategori': kategori
    })


@admin_required
def kategori_tambah(request):
    if request.method == 'POST':
        nama = request.POST.get('nama_kategori', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()

        if not nama:
            messages.error(request, 'Nama kategori wajib diisi.')
            return render(request, 'kategori/form.html')

        Kategori.objects.create(
            nama_kategori=nama,
            deskripsi=deskripsi
        )
        catat_aktivitas(request, 'tambah', f'Tambah kategori: {nama}')
        messages.success(request, f'Kategori "{nama}" berhasil ditambahkan.')
        return redirect('kategori:list')

    return render(request, 'kategori/form.html', {'title': 'Tambah Kategori'})


@admin_required
def kategori_edit(request, id):
    kategori = get_object_or_404(Kategori, id=id)

    if request.method == 'POST':
        nama = request.POST.get('nama_kategori', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()

        if not nama:
            messages.error(request, 'Nama kategori wajib diisi.')
            return render(request, 'kategori/form.html', {
                'title': 'Edit Kategori',
                'kategori': kategori
            })

        kategori.nama_kategori = nama
        kategori.deskripsi = deskripsi
        kategori.save()

        catat_aktivitas(request, 'ubah', f'Edit kategori: {nama}')
        messages.success(request, f'Kategori "{nama}" berhasil diperbarui.')
        return redirect('kategori:list')

    return render(request, 'kategori/form.html', {
        'title': 'Edit Kategori',
        'kategori': kategori
    })


@admin_required
@require_POST
def kategori_hapus(request, id):
    kategori = get_object_or_404(Kategori, id=id)

    # Cek apakah kategori masih dipakai produk aktif
    if kategori.produk.filter(is_active=True).exists():
        messages.error(
            request,
            f'Kategori "{kategori.nama_kategori}" tidak bisa dihapus karena masih digunakan oleh produk aktif.'
        )
        return redirect('kategori:list')

    nama = kategori.nama_kategori
    kategori.is_active = False
    kategori.save()

    catat_aktivitas(request, 'hapus', f'Hapus kategori: {nama}')
    messages.success(request, f'Kategori "{nama}" berhasil dihapus.')
    return redirect('kategori:list')