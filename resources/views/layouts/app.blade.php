{{--
    NakamotoX — Shared Layout (Tim Frontend)

    Layout utama yang digunakan oleh semua halaman.
    Tim Frontend, silakan desain layout ini!

    Penggunaan di halaman lain:
    @extends('layouts.app')
    @section('title', 'Judul Halaman')
    @section('content')
        <!-- isi halaman -->
    @endsection
--}}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>@yield('title', 'NakamotoX') — NakamotoX</title>
    <script src="//unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        /* ───────────────────────────────────────────
           TODO: Tim Frontend, desain CSS kalian di sini!
           Bisa juga pakai file CSS terpisah via Vite.
           ─────────────────────────────────────────── */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background: #000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
        }

        /* ── Navbar ── */
        nav {
            background: #111;
            border-bottom: 1px solid #00ff00;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            gap: 24px;
        }
        nav .brand {
            font-size: 18px;
            font-weight: bold;
            color: #00ff00;
            text-decoration: none;
        }
        nav a {
            color: #008800;
            text-decoration: none;
            font-size: 14px;
        }
        nav a:hover, nav a.active {
            color: #00ff00;
        }

        /* ── Main Content ── */
        main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 16px;
        }
    </style>
    @stack('styles')
</head>
<body>

<nav>
    <a href="/" class="brand">NakamotoX</a>
    <a href="/chacha20">ChaCha20</a>
    <a href="/caesar">Caesar Cipher</a>
    {{-- TODO: Tambahkan link navigasi lainnya --}}
</nav>

<main>
    @yield('content')
</main>

@stack('scripts')
</body>
</html>
