from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Root → langsung ke dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    path('admin/',      admin.site.urls),
    path('accounts/',   include('accounts.urls')),
    path('dashboard/',  include('dashboard.urls')),
    path('produk/',     include('produk.urls')),
    path('transaksi/',  include('transaksi.urls')),
    path('kategori/',   include('kategori.urls')),
    path('pengaturan/', include('pengaturan.urls')),
    path('laporan/',    include('laporan.urls')),
]
