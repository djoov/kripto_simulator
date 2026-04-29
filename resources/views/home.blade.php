{{--
    NakamotoX — Landing Page

    TODO: Tim Frontend, desain landing page yang menarik di sini!
    Halaman ini tampil saat user membuka http://localhost:8000/
--}}
@extends('layouts.app')

@section('title', 'Home')

@section('content')
    <div style="text-align:center; padding: 80px 20px;">
        <h1 style="font-size: 36px; margin-bottom: 16px;">
            🔐 NakamotoX
        </h1>
        <p style="color: #008800; margin-bottom: 40px;">
            Platform Simulator Kriptografi Edukasional
        </p>

        <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;">
            <a href="/chacha20" style="
                display: block; padding: 24px 32px;
                border: 1px solid #00ff00; color: #00ff00;
                text-decoration: none; min-width: 200px;
            ">
                <div style="font-size: 24px; margin-bottom: 8px;">🔒</div>
                <div style="font-weight: bold;">ChaCha20</div>
                <div style="font-size: 12px; color: #008800; margin-top: 4px;">Stream Cipher · RFC 8439</div>
            </a>

            <a href="/caesar" style="
                display: block; padding: 24px 32px;
                border: 1px solid #00ff00; color: #00ff00;
                text-decoration: none; min-width: 200px;
            ">
                <div style="font-size: 24px; margin-bottom: 8px;">🔤</div>
                <div style="font-weight: bold;">Caesar Cipher</div>
                <div style="font-size: 12px; color: #008800; margin-top: 4px;">Substitution Cipher · Klasik</div>
            </a>
        </div>
    </div>
@endsection
