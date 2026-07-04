from django import forms
from .models import Produk


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = [
            'nama_produk', 'kategori', 'kondisi', 'garansi_hari',
            'harga_beli', 'harga_jual', 'stok_minimum', 'satuan',
        ]
        widgets = {
            'nama_produk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama produk',
            }),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'kondisi': forms.Select(attrs={'class': 'form-select'}),
            'garansi_hari': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': '0', 'min': '0',
            }),
            'harga_beli': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': '0', 'min': '0',
            }),
            'harga_jual': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': '0', 'min': '0',
            }),
            'stok_minimum': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0',
            }),
            'satuan': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'pcs, kg, liter, dll',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        harga_beli = cleaned_data.get('harga_beli')
        harga_jual = cleaned_data.get('harga_jual')

        if harga_beli is not None and harga_beli < 0:
            self.add_error('harga_beli', 'Harga beli tidak boleh negatif.')

        if harga_jual is not None and harga_jual < 0:
            self.add_error('harga_jual', 'Harga jual tidak boleh negatif.')

        return cleaned_data
