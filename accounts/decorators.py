from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """
    Hanya user dengan role 'admin' yang bisa akses.
    User 'petugas' akan diarahkan ke dashboard dengan pesan error.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'admin' and not request.user.is_superuser:
            messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return wrapper


def petugas_required(view_func):
    """
    Hanya user yang sudah login (admin & petugas) yang bisa akses.
    Sama dengan @login_required tapi pakai redirect ke accounts:login.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper
