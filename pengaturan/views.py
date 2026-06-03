from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

from accounts.models import User
from accounts.decorators import admin_required, petugas_required
from .models import InfoToko, LogAktivitas


# ============================================================
# HALAMAN UTAMA PENGATURAN
# ============================================================

@petugas_required
def index(request):
    return render(request, 'pengaturan/index.html')


# ============================================================
# MANAJEMEN USER (admin only)
# ============================================================

@admin_required
def user_list(request):
    users = User.objects.all().order_by('role', 'username')
    return render(request, 'pengaturan/user_list.html', {'users': users})


@admin_required
def user_tambah(request):
    if request.method == 'POST':
        username   = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        role       = request.POST.get('role', 'petugas')
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')

        if not username or not password:
            messages.error(request, 'Username dan password wajib diisi.')
        elif password != password2:
            messages.error(request, 'Konfirmasi password tidak cocok.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" sudah digunakan.')
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                role=role,
            )
            LogAktivitas.objects.create(
                user=request.user,
                aksi='tambah',
                keterangan=f'Tambah user: {user.username} ({user.get_role_display()})',
                ip_address=get_ip(request),
            )
            messages.success(request, f'User "{username}" berhasil ditambahkan.')
            return redirect('pengaturan:user_list')

    return render(request, 'pengaturan/user_form.html', {'title': 'Tambah User'})


@admin_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.email      = request.POST.get('email', '').strip()
        user.role       = request.POST.get('role', user.role)
        user.save()

        LogAktivitas.objects.create(
            user=request.user,
            aksi='ubah',
            keterangan=f'Edit user: {user.username}',
            ip_address=get_ip(request),
        )
        messages.success(request, f'Data user "{user.username}" berhasil diperbarui.')
        return redirect('pengaturan:user_list')

    return render(request, 'pengaturan/user_form.html', {
        'title': 'Edit User',
        'obj': user,
    })


@admin_required
def user_toggle_aktif(request, id):
    user = get_object_or_404(User, id=id)

    # Jangan nonaktifkan diri sendiri
    if user == request.user:
        messages.error(request, 'Tidak bisa menonaktifkan akun sendiri.')
        return redirect('pengaturan:user_list')

    user.is_active = not user.is_active
    user.save()

    status = 'diaktifkan' if user.is_active else 'dinonaktifkan'
    LogAktivitas.objects.create(
        user=request.user,
        aksi='hapus',
        keterangan=f'User {user.username} {status}',
        ip_address=get_ip(request),
    )
    messages.success(request, f'User "{user.username}" berhasil {status}.')
    return redirect('pengaturan:user_list')


# ============================================================
# PROFIL & GANTI PASSWORD (semua user)
# ============================================================

@petugas_required
def profil(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name  = request.POST.get('last_name', '').strip()
        request.user.email      = request.POST.get('email', '').strip()
        request.user.save()

        messages.success(request, 'Profil berhasil diperbarui.')
        return redirect('pengaturan:profil')

    return render(request, 'pengaturan/profil.html')


@petugas_required
def ganti_password(request):
    if request.method == 'POST':
        password_lama = request.POST.get('password_lama', '')
        password_baru = request.POST.get('password_baru', '')
        password_baru2 = request.POST.get('password_baru2', '')

        if not check_password(password_lama, request.user.password):
            messages.error(request, 'Password lama tidak benar.')
        elif len(password_baru) < 8:
            messages.error(request, 'Password baru minimal 8 karakter.')
        elif password_baru != password_baru2:
            messages.error(request, 'Konfirmasi password baru tidak cocok.')
        else:
            request.user.set_password(password_baru)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password berhasil diubah.')
            return redirect('pengaturan:profil')

    return render(request, 'pengaturan/ganti_password.html')


# ============================================================
# INFO TOKO (admin only)
# ============================================================

@admin_required
def info_toko(request):
    toko = InfoToko.get()

    if request.method == 'POST':
        toko.nama_toko   = request.POST.get('nama_toko', '').strip()
        toko.alamat      = request.POST.get('alamat', '').strip()
        toko.telepon     = request.POST.get('telepon', '').strip()
        toko.email       = request.POST.get('email', '').strip()
        toko.stok_minimum_default = int(request.POST.get('stok_minimum_default', 5))
        toko.save()

        LogAktivitas.objects.create(
            user=request.user,
            aksi='ubah',
            keterangan='Perbarui info toko',
            ip_address=get_ip(request),
        )
        messages.success(request, 'Info toko berhasil disimpan.')
        return redirect('pengaturan:info_toko')

    return render(request, 'pengaturan/info_toko.html', {'toko': toko})


# ============================================================
# LOG AKTIVITAS (admin only)
# ============================================================

@admin_required
def log_aktivitas(request):
    logs = LogAktivitas.objects.select_related('user').all()[:200]
    return render(request, 'pengaturan/log_aktivitas.html', {'logs': logs})


# ============================================================
# HELPER
# ============================================================

def get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')