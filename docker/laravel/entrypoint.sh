#!/bin/bash
set -e

echo "🚀 Kripto Simulator — Laravel Entrypoint"
echo "========================================="

# ── Generate APP_KEY jika belum ada ──
if [ -z "$APP_KEY" ] || [ "$APP_KEY" = "base64:" ]; then
    echo "🔑 Generating APP_KEY..."
    php artisan key:generate --force
fi

# ── Tunggu MySQL siap ──
echo "⏳ Waiting for MySQL..."
until php -r "new PDO('mysql:host=${DB_HOST};dbname=${DB_DATABASE}', '${DB_USERNAME}', '${DB_PASSWORD}');" 2>/dev/null; do
    echo "   MySQL not ready, retrying in 3s..."
    sleep 3
done
echo "✅ MySQL is ready."

# ── Migrasi database ──
echo "🗄️  Running migrations..."
php artisan migrate --force --no-interaction

# ── Clear & cache config ──
echo "⚙️  Caching config & routes..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

echo "✅ Laravel ready. Starting PHP-FPM..."
exec php-fpm
