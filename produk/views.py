from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk
from kategori.models import Kategori


def produk_list(request):
    tab = request.GET.get('tab', 'aktif')

    if tab == 'nonaktif':
        produk = Produk.objects.filter(is_active=False).select_related('kategori')
    else:
        produk = Produk.objects.filter(is_active=True).select_related('kategori')

    return render(request, 'produk/list.html', {
        'produk': produk,
        'tab': tab,
    })


def tambah_produk(request):
    if request.method == 'POST':
        Produk.objects.create(
            nama_produk=request.POST['nama_produk'],
            kategori_id=request.POST['kategori'],
            stok_minimum=request.POST.get('stok_minimum', 5),
            harga_beli=request.POST['harga_beli'],
            harga_jual=request.POST['harga_jual'],
            satuan=request.POST.get('satuan', 'pcs')
        )
        return redirect('produk:list')

    return render(request, 'produk/form.html', {
        'kategori': Kategori.objects.filter(is_active=True),
        'title': 'Tambah Produk'
    })


def produk_edit(request, id):
    produk = get_object_or_404(Produk, id=id)

    if request.method == 'POST':
        produk.nama_produk = request.POST.get('nama_produk')
        produk.kategori_id = request.POST.get('kategori')
        produk.stok_minimum = request.POST.get('stok_minimum')
        produk.harga_beli = request.POST.get('harga_beli')
        produk.harga_jual = request.POST.get('harga_jual')
        produk.satuan = request.POST.get('satuan')
        produk.save()

        return redirect('produk:list')

    return render(request, 'produk/form.html', {
        'produk': produk,
        'kategori': Kategori.objects.filter(is_active=True),
        'title': 'Edit Produk'
    })


def produk_nonaktif(request, id):
    produk = get_object_or_404(Produk, id=id)
    produk.is_active = False
    produk.save()
    return redirect('produk:list')


def produk_aktifkan(request, id):
    produk = get_object_or_404(Produk, id=id)
    produk.is_active = True
    produk.save()
    return redirect('/produk/?tab=nonaktif')