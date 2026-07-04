"""
Management command: seed_initial
Mengisi data awal ke database jika masih kosong.
Aman dipanggil berulang kali — TIDAK akan overwrite data yang sudah ada.
"""
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed data awal (superuser, info toko, kategori) jika database masih kosong.'

    def handle(self, *args, **options):
        self._seed_superuser()
        self._seed_info_toko()
        self._seed_kategori()
        self.stdout.write(self.style.SUCCESS('Seed data awal selesai.'))

    # ──────────────────────────────────────────────
    # 1. Superuser admin
    # ──────────────────────────────────────────────
    def _seed_superuser(self):
        from accounts.models import User

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('  ↳ Superuser sudah ada, skip.')
            return

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='admin',
        )
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Superuser "{username}" berhasil dibuat.'
        ))

    # ──────────────────────────────────────────────
    # 2. Info Toko
    # ──────────────────────────────────────────────
    def _seed_info_toko(self):
        from pengaturan.models import InfoToko

        if InfoToko.objects.exists():
            self.stdout.write('  ↳ Info toko sudah ada, skip.')
            return

        InfoToko.objects.create(
            pk=1,
            nama_toko='Toko Borneo Ponsel',
            alamat='Jl. Contoh No. 1',
            telepon='08xxxxxxxxxx',
            email='info@borneoponsel.com',
            stok_minimum_default=5,
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Info toko default berhasil dibuat.'))

    # ──────────────────────────────────────────────
    # 3. Kategori produk
    # ──────────────────────────────────────────────
    def _seed_kategori(self):
        from kategori.models import Kategori

        if Kategori.objects.exists():
            self.stdout.write('  ↳ Kategori sudah ada, skip.')
            return

        kategori_list = [
            {'nama_kategori': 'Handphone', 'deskripsi': 'Smartphone dan feature phone'},
            {'nama_kategori': 'Aksesoris HP', 'deskripsi': 'Earphone, holder, ring, dll'},
            {'nama_kategori': 'Sparepart', 'deskripsi': 'LCD, baterai, flexibel, dll'},
            {'nama_kategori': 'Charger & Kabel', 'deskripsi': 'Charger, kabel data, adaptor'},
            {'nama_kategori': 'Casing & Pelindung', 'deskripsi': 'Softcase, hardcase, tempered glass'},
        ]

        created = []
        for item in kategori_list:
            obj = Kategori.objects.create(**item)
            created.append(obj.nama_kategori)

        self.stdout.write(self.style.SUCCESS(
            f'  ✓ {len(created)} kategori berhasil dibuat: {", ".join(created)}'
        ))
