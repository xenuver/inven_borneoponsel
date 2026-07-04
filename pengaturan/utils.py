from .models import LogAktivitas


def get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def catat_aktivitas(request, aksi, keterangan):
    """
    Catat satu baris log aktivitas untuk user yang sedang login.
    aksi: 'tambah' | 'ubah' | 'hapus'
    keterangan: deskripsi singkat aksi yang dilakukan
    """
    try:
        LogAktivitas.objects.create(
            user=request.user if request.user.is_authenticated else None,
            aksi=aksi,
            keterangan=keterangan,
            ip_address=get_ip(request),
        )
    except Exception:
        # Jangan sampai kegagalan logging menggagalkan aksi utama user
        pass
