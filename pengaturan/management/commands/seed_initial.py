"""
Management command: seed_initial
Mengisi data awal ke database jika masih kosong menggunakan file seed_data.json.
Aman dipanggil berulang kali — TIDAK akan overwrite data yang sudah ada.
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from accounts.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Load data awal dari seed_data.json jika database masih kosong.'

    def handle(self, *args, **options):
        # Cek apakah database sudah ada datanya (dengan mengecek tabel User)
        if User.objects.exists():
            self.stdout.write(self.style.WARNING('Data sudah ada di database, skip seed_initial.'))
            return

        seed_file = os.path.join(settings.BASE_DIR, 'seed_data.json')
        if not os.path.exists(seed_file):
            self.stdout.write(self.style.ERROR(f'File {seed_file} tidak ditemukan!'))
            return

        self.stdout.write(self.style.SUCCESS('Database masih kosong, memuat data dari seed_data.json...'))
        
        try:
            call_command('loaddata', seed_file)
            self.stdout.write(self.style.SUCCESS('✓ Berhasil memuat seluruh data awal dari db lokal!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Gagal memuat data: {str(e)}'))
