from django import forms
from .models import Transaksi, DetailTransaksi
from produk.models import Produk
from supplier.models import Supplier


class BarangMasukForm(forms.Form):
    produk = forms.ModelChoiceField(
        queryset=Produk.objects.filter(is_active=True),
        label="Produk",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(is_active=True),
        label="Supplier",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    jumlah = forms.IntegerField(
        min_value=1,
        label="Jumlah",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan jumlah barang'
        })
    )

    keterangan = forms.CharField(
        required=False,
        label="Keterangan",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tambahkan keterangan (opsional)'
        })
    )


class BarangKeluarForm(forms.Form):
    produk = forms.ModelChoiceField(
        queryset=Produk.objects.filter(is_active=True),
        label="Produk",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    jumlah = forms.IntegerField(
        min_value=1,
        label="Jumlah",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan jumlah barang'
        })
    )

    keterangan = forms.CharField(
        required=False,
        label="Keterangan",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tambahkan keterangan (opsional)'
        })
    )

class StokOpnameForm(forms.Form):
    produk = forms.ModelChoiceField(
        queryset=Produk.objects.filter(is_active=True),
        label="Produk",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    stok_fisik = forms.IntegerField(
        min_value=0,
        label="Stok Fisik (hasil hitung)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Jumlah stok hasil hitung fisik'
        })
    )

    keterangan = forms.CharField(
        required=False,
        label="Keterangan",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Misal: hasil stok opname bulanan'
        })
    )
