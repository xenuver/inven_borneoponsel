from django.shortcuts import redirect
from django.contrib.auth import signals
from django.dispatch import receiver

EXEMPT_URLS = [
    '/accounts/login/',
    '/accounts/logout/',
    '/admin/',
]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_exempt = any(request.path.startswith(url) for url in EXEMPT_URLS)

        if not is_exempt and not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')

        return self.get_response(request)


def get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


@receiver(signals.user_logged_in)
def log_login(sender, request, user, **kwargs):
    try:
        from pengaturan.models import LogAktivitas
        LogAktivitas.objects.create(
            user=user,
            aksi='login',
            keterangan=f'{user.username} login ke sistem',
            ip_address=get_ip(request),
        )
    except Exception:
        pass


@receiver(signals.user_logged_out)
def log_logout(sender, request, user, **kwargs):
    try:
        from pengaturan.models import LogAktivitas
        if user:
            LogAktivitas.objects.create(
                user=user,
                aksi='logout',
                keterangan=f'{user.username} logout dari sistem',
                ip_address=get_ip(request),
            )
    except Exception:
        pass
