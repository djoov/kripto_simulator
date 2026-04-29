# Tim Frontend — Panduan

## Area Kerja Kalian

| Folder / File | Keterangan |
|--------------|------------|
| `resources/views/layouts/` | Shared layout (navbar, footer) |
| `resources/views/home.blade.php` | Landing page |
| `resources/css/` | Stylesheet (jika pakai Vite) |
| `resources/js/` | JavaScript (jika pakai Vite) |
| `public/assets/` | Gambar, icon, font |

## Halaman yang Sudah Ada

| URL | View File | Tim |
|-----|-----------|-----|
| `/` | `home.blade.php` | Frontend (kalian) |
| `/chacha20` | `chacha20/index.blade.php` | Tim ChaCha20 |
| `/caesar` | `caesar/index.blade.php` | Tim Caesar |

## Cara Menjalankan

```bash
cd kripto-simulator
npm install
npm run dev          # Terminal 1 — Vite dev server
php artisan serve    # Terminal 2 — Laravel
```

## Aturan Penting

> ⚠️ **JANGAN hapus atau edit file-file berikut:**
> - `chacha20-api/` (milik tim ChaCha20)
> - `caesar-api/` (milik tim Caesar)
> - `app/Http/Controllers/ChaCha20Controller.php`
> - `app/Http/Controllers/CaesarController.php`
> - `app/Services/` (milik tim backend)
>
> **BOLEH diedit:**
> - `resources/views/layouts/` — layout dan navbar
> - `resources/views/home.blade.php` — landing page
> - `resources/css/`, `resources/js/`, `public/assets/`
> - `routes/web.php` — HANYA menambahkan route baru, jangan hapus yang lama
