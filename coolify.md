# 🚀 Panduan Deploy ke Coolify (Docker Compose)

Panduan lengkap untuk deploy **Inventory Borneo Ponsel** ke VPS menggunakan [Coolify](https://coolify.io) dengan buildpack **Docker Compose**.

---

## 📋 Prasyarat

- **VPS** dengan minimal 1 GB RAM, 1 vCPU (rekomendasi 2 GB RAM)
- **OS**: Ubuntu 22.04+ / Debian 12+
- **Domain** (opsional, Coolify bisa generate subdomain sementara)
- **Repository GitHub**: `https://github.com/xenuver/inven_borneoponsel.git`

---

## 1️⃣ Install Coolify di VPS

SSH ke VPS kamu, lalu jalankan satu perintah ini:

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

Setelah instalasi selesai:
1. Buka browser, akses `http://<IP-VPS>:8000`
2. Buat akun admin Coolify
3. Ikuti setup wizard (pilih **Localhost** sebagai server)

> **💡 Tips**: Jika port 8000 tidak bisa diakses, pastikan firewall VPS membuka port `8000`, `80`, dan `443`.

---

## 2️⃣ Connect Repository GitHub

### A. Buat Project Baru
1. Di dashboard Coolify, klik **"+ Add New Resource"**
2. Pilih **"Public Repository"** (atau Private jika repository private)
3. Masukkan URL repository:
   ```
   https://github.com/xenuver/inven_borneoponsel.git
   ```
4. Branch: `main` (atau sesuaikan dengan branch utama kamu)

### B. Pilih Buildpack
1. Saat diminta memilih buildpack, pilih: **"Docker Compose"**
2. Coolify akan otomatis mendeteksi file `docker-compose.yml` di root project

---

## 3️⃣ Setting Environment Variables

Di halaman resource yang baru dibuat, masuk ke tab **"Environment Variables"**, lalu tambahkan variable berikut:

### Wajib (Production)

| Variable | Contoh Nilai | Keterangan |
|----------|-------------|------------|
| `DJANGO_SECRET_KEY` | `abc123xyz...` (random string panjang) | Generate dengan: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DJANGO_DEBUG` | `False` | **Harus False** di production! |
| `DJANGO_ALLOWED_HOSTS` | `inventory.domain.com,www.domain.com` | Domain yang dipakai |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://inventory.domain.com` | **Wajib pakai https://** |

### Database (sudah ada default, tapi bisa diganti)

| Variable | Default | Keterangan |
|----------|---------|------------|
| `DB_NAME` | `inventory_borneo` | Nama database PostgreSQL |
| `DB_USER` | `borneo` | Username database |
| `DB_PASSWORD` | `borneo_secret_db_2024` | **Ganti dengan password kuat!** |

### Superuser (opsional)

| Variable | Default | Keterangan |
|----------|---------|------------|
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Username admin pertama |
| `DJANGO_SUPERUSER_PASSWORD` | `admin123` | **Ganti dengan password kuat!** |
| `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | Email admin |

> **⚠️ PENTING**: Ganti `DB_PASSWORD` dan `DJANGO_SUPERUSER_PASSWORD` dengan password yang kuat!

---

## 4️⃣ Setting Domain & SSL

### Jika Punya Domain:
1. Di tab **"General"** / **"Settings"**, masukkan domain di field **"Domains"**:
   ```
   https://inventory.domain.com
   ```
2. Arahkan DNS A Record domain ke IP VPS kamu
3. Coolify akan otomatis generate SSL certificate via Let's Encrypt

### Jika Belum Punya Domain:
- Coolify akan generate random subdomain (contoh: `abc123.sslip.io`)
- Kamu bisa pakai ini untuk testing dulu

### Konfigurasi Port
Karena kita menggunakan Nginx di dalam Docker Compose yang listen di port **80**, setting di Coolify:
- **Ports Mappings**: `80:80` (ini sudah didefinisikan di `docker-compose.yml`)

> **💡 Note**: Jika Coolify juga pakai Traefik sebagai proxy, maka port mapping di `docker-compose.yml` mungkin perlu disesuaikan. Coolify biasanya akan otomatis menangani routing via Traefik.

---

## 5️⃣ Deploy Pertama Kali

1. Klik tombol **"Deploy"** 🚀
2. Pantau log build di tab **"Deployments"**
3. Proses yang terjadi secara otomatis:
   ```
   ✓ Build Docker image (install dependencies)
   ✓ Start PostgreSQL
   ✓ Wait for PostgreSQL ready
   ✓ Run database migrations
   ✓ Collect static files
   ✓ Seed data awal (superuser + kategori + info toko)
   ✓ Start Gunicorn server
   ✓ Start Nginx reverse proxy
   ```
4. Setelah semua hijau ✅, akses domain/URL kamu
5. Login dengan:
   - Username: `admin` (atau sesuai env var)
   - Password: `admin123` (atau sesuai env var)
6. **Segera ganti password** setelah login pertama!

---

## 6️⃣ Update / Rebuild

### Otomatis (Webhook):
1. Di Coolify, aktifkan **"Auto Deploy"** di tab Settings
2. Setiap push ke branch `main`, Coolify otomatis rebuild

### Manual:
1. Push perubahan ke GitHub:
   ```bash
   git add .
   git commit -m "update fitur XYZ"
   git push origin main
   ```
2. Di dashboard Coolify, klik **"Redeploy"**

> **✅ Data Aman**: Saat rebuild, data di database PostgreSQL **TIDAK hilang** karena disimpan di Docker Volume (`postgres_data`). Script seed juga tidak akan overwrite data yang sudah ada.

---

## 🔧 Troubleshooting

### 1. "CSRF verification failed"
**Penyebab**: `DJANGO_CSRF_TRUSTED_ORIGINS` belum diset atau salah.
**Solusi**: Tambahkan di environment variable:
```
DJANGO_CSRF_TRUSTED_ORIGINS=https://inventory.domain.com
```
> Pastikan pakai `https://` di depan!

### 2. "DisallowedHost"
**Penyebab**: Domain belum masuk di `DJANGO_ALLOWED_HOSTS`.
**Solusi**: Tambahkan domain:
```
DJANGO_ALLOWED_HOSTS=inventory.domain.com,www.domain.com
```

### 3. Static files (CSS/JS) tidak muncul
**Penyebab**: Volume static belum ter-sync antara `web` dan `nginx`.
**Solusi**:
1. Masuk ke container web: `docker exec -it <container_web> bash`
2. Jalankan: `python manage.py collectstatic --noinput`
3. Restart service nginx

### 4. Database connection error
**Penyebab**: Service `db` belum siap saat `web` start.
**Solusi**: Script `entrypoint.sh` sudah menangani ini dengan `pg_isready` loop. Jika masih bermasalah, cek log container `db`.

### 5. Mau reset database (mulai dari awal)
**⚠️ Hati-hati, semua data hilang!**
```bash
# SSH ke VPS, lalu:
docker compose down -v   # hapus semua volume (termasuk data DB)
# Redeploy dari Coolify
```

### 6. Cara akses shell Django di production
```bash
# SSH ke VPS
docker exec -it <container_web> python manage.py shell
```

### 7. Cara buat superuser baru secara manual
```bash
docker exec -it <container_web> python manage.py createsuperuser
```

---

## 📁 Struktur File Docker

```
inventory_borneo/
├── Dockerfile              # Build image Django + Gunicorn
├── docker-compose.yml      # Orchestrasi 3 service (db, web, nginx)
├── entrypoint.sh           # Script startup (migrate, seed, gunicorn)
├── nginx/
│   └── default.conf        # Konfigurasi Nginx reverse proxy
├── requirements.txt        # Dependencies Python (+ gunicorn, psycopg)
├── config/
│   ├── settings.py         # Settings Django (support PostgreSQL)
│   └── management/
│       └── commands/
│           └── seed_initial.py  # Auto-seed data awal
└── .env.example            # Template environment variables
```

---

## 🔄 Alur Deploy (Ringkasan)

```
Push ke GitHub → Coolify detect → Build Dockerfile
                                      ↓
                              docker-compose up
                                      ↓
                    ┌─────────────────────────────────────┐
                    │  db (PostgreSQL)  ──  Ready?        │
                    │         ↓                           │
                    │  web (Django)                       │
                    │    ├── migrate                      │
                    │    ├── collectstatic                │
                    │    ├── seed_initial (jika kosong)   │
                    │    └── gunicorn :8000               │
                    │         ↓                           │
                    │  nginx (:80) ── reverse proxy       │
                    └─────────────────────────────────────┘
                                      ↓
                           Aplikasi Online! 🎉
```
