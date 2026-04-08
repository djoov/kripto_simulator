<?php

use App\Http\Controllers\ChaCha20Controller;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => redirect()->route('chacha20.index'));

// ─────────────────────────────────────────────
//  ChaCha20 Simulator
// ─────────────────────────────────────────────
Route::prefix('chacha20')->name('chacha20.')->group(function () {

    // Halaman simulator (Blade view)
    Route::get('/', [ChaCha20Controller::class, 'index'])->name('index');

    // JSON endpoints — dikonsumsi Alpine.js di frontend
    Route::get('/keygen',   [ChaCha20Controller::class, 'keygen'])->name('keygen');
    Route::post('/encrypt', [ChaCha20Controller::class, 'encrypt'])->name('encrypt');
    Route::post('/decrypt', [ChaCha20Controller::class, 'decrypt'])->name('decrypt');

    // Khusus untuk State Matrix Viewer — selalu mengembalikan round_logs
    Route::post('/steps',   [ChaCha20Controller::class, 'steps'])->name('steps');

});
