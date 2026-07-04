from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.decorators import admin_required, petugas_required
from pengaturan.utils import catat_aktivitas
from .models import Supplier


@petugas_required
def supplier_list(request):
    q = request.GET.get('q', '').strip()
    supplier = Supplier.objects.filter(is_active=True)
    if q:
        supplier = supplier.filter(nama_supplier__icontains=q)
    return render(request, 'supplier/list.html', {'supplier': supplier, 'q': q})


@admin_required
def supplier_tambah(request):
    if request.method == 'POST':
        nama = request.POST.get('nama_supplier', '').strip()
        if not nama:
            messages.error(request, 'Nama supplier wajib diisi.')
        else:
            Supplier.objects.create(
                nama_supplier=nama,
                kontak_person=request.POST.get('kontak_person', '').strip(),
                telepon=request.POST.get('telepon', '').strip(),
                email=request.POST.get('email', '').strip(),
                alamat=request.POST.get('alamat', '').strip(),
            )
            catat_aktivitas(request, 'tambah', f'Tambah supplier: {nama}')
            messages.success(request, f'Supplier "{nama}" berhasil ditambahkan.')
            return redirect('supplier:list')

    return render(request, 'supplier/form.html', {'title': 'Tambah Supplier'})


@admin_required
def supplier_edit(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        nama = request.POST.get('nama_supplier', '').strip()
        if not nama:
            messages.error(request, 'Nama supplier wajib diisi.')
        else:
            supplier.nama_supplier = nama
            supplier.kontak_person = request.POST.get('kontak_person', '').strip()
            supplier.telepon = request.POST.get('telepon', '').strip()
            supplier.email = request.POST.get('email', '').strip()
            supplier.alamat = request.POST.get('alamat', '').strip()
            supplier.save()
            catat_aktivitas(request, 'ubah', f'Edit supplier: {nama}')
            messages.success(request, f'Supplier "{nama}" berhasil diperbarui.')
            return redirect('supplier:list')

    return render(request, 'supplier/form.html', {
        'title': 'Edit Supplier',
        'supplier': supplier,
    })


@admin_required
@require_POST
def supplier_hapus(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.is_active = False
    supplier.save()
    catat_aktivitas(request, 'hapus', f'Nonaktifkan supplier: {supplier.nama_supplier}')
    messages.success(request, f'Supplier "{supplier.nama_supplier}" berhasil dinonaktifkan.')
    return redirect('supplier:list')
