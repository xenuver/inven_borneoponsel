#!/bin/bash
set -e

echo "============================================"
echo "  Inventory Borneo Ponsel — Starting..."
echo "============================================"

# --------------------------------------------------
# 1. Wait for PostgreSQL to be ready
# --------------------------------------------------
echo "[1/4] Menunggu PostgreSQL siap..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -q; do
  echo "  PostgreSQL belum siap, retry dalam 2 detik..."
  sleep 2
done
echo "  ✓ PostgreSQL siap!"

# --------------------------------------------------
# 2. Run database migrations
# --------------------------------------------------
echo "[2/4] Menjalankan migrasi database..."
python manage.py migrate --noinput
echo "  ✓ Migrasi selesai!"

# --------------------------------------------------
# 3. Collect static files
# --------------------------------------------------
echo "[3/4] Mengumpulkan static files..."
python manage.py collectstatic --noinput
echo "  ✓ Static files siap!"

# --------------------------------------------------
# 4. Seed initial data (only if empty)
# --------------------------------------------------
echo "[4/4] Mengecek & seed data awal..."
python manage.py seed_initial
echo "  ✓ Seed data selesai!"

echo "============================================"
echo "  Memulai Gunicorn server..."
echo "============================================"

# Start Gunicorn
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
