<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>ChaCha20 Simulator — Kripto Simulator</title>
    <script src="//unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg:       #0d1117;
            --surface:  #161b22;
            --border:   #30363d;
            --accent:   #58a6ff;
            --green:    #3fb950;
            --red:      #f85149;
            --yellow:   #d29922;
            --text:     #e6edf3;
            --muted:    #8b949e;
            --radius:   8px;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-size: 14px;
            min-height: 100vh;
        }

        /* Layout */
        header {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 12px 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        header h1 { font-size: 18px; font-weight: 600; color: var(--accent); }
        header .badge {
            font-size: 11px; background: #1f2d4a; color: var(--accent);
            border: 1px solid var(--accent); border-radius: 20px; padding: 2px 10px;
        }

        .container { max-width: 1100px; margin: 0 auto; padding: 24px 16px; }

        /* Cards */
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 16px;
        }
        .card-title {
            font-size: 13px; font-weight: 600; color: var(--muted);
            text-transform: uppercase; letter-spacing: .05em;
            margin-bottom: 14px;
        }

        /* Form */
        .form-group { margin-bottom: 14px; }
        label { display: block; font-size: 12px; color: var(--muted); margin-bottom: 6px; }
        input[type=text], textarea {
            width: 100%; padding: 8px 12px;
            background: var(--bg); border: 1px solid var(--border);
            border-radius: 6px; color: var(--text); font-size: 13px;
            font-family: 'Consolas', monospace;
            transition: border-color .2s;
        }
        input[type=text]:focus, textarea:focus {
            outline: none; border-color: var(--accent);
        }
        textarea { resize: vertical; min-height: 80px; }

        /* Buttons */
        .btn {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 8px 16px; border-radius: 6px; font-size: 13px;
            font-weight: 500; cursor: pointer; border: none; transition: opacity .2s;
        }
        .btn:disabled { opacity: .5; cursor: not-allowed; }
        .btn:not(:disabled):hover { opacity: .85; }
        .btn-primary  { background: var(--accent); color: #000; }
        .btn-success  { background: var(--green);  color: #000; }
        .btn-danger   { background: var(--red);    color: #fff; }
        .btn-outline  {
            background: transparent; color: var(--accent);
            border: 1px solid var(--accent);
        }
        .btn-sm { padding: 5px 10px; font-size: 12px; }

        /* Toggle tab */
        .tab-group {
            display: flex; border: 1px solid var(--border);
            border-radius: 6px; overflow: hidden; margin-bottom: 16px;
        }
        .tab {
            flex: 1; padding: 9px; text-align: center; cursor: pointer;
            font-size: 13px; transition: background .2s;
            background: var(--bg); color: var(--muted);
        }
        .tab.active { background: var(--accent); color: #000; font-weight: 600; }

        /* Key/nonce row */
        .key-row { display: flex; gap: 8px; align-items: flex-end; }
        .key-row .form-group { flex: 1; margin-bottom: 0; }

        /* Result */
        .result-box {
            font-family: 'Consolas', monospace; font-size: 12px;
            background: var(--bg); border: 1px solid var(--border);
            border-radius: 6px; padding: 12px; word-break: break-all;
            white-space: pre-wrap; color: var(--green); min-height: 48px;
        }
        .result-box.error { color: var(--red); }
        .result-box.muted { color: var(--muted); }

        /* Steps summary */
        .step-summary {
            display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;
        }
        .step-pill {
            background: #1f2d4a; border: 1px solid var(--accent);
            color: var(--accent); border-radius: 20px;
            padding: 3px 12px; font-size: 12px;
        }

        /* State matrix grid */
        .state-matrix {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 4px; margin-bottom: 8px;
        }
        .state-cell {
            background: #1f2d4a; border: 1px solid var(--border);
            border-radius: 4px; padding: 8px 4px;
            font-family: 'Consolas', monospace; font-size: 11px;
            text-align: center; color: var(--accent);
            transition: background .3s, color .3s;
        }
        .state-cell.changed {
            background: #2d1f1f; border-color: var(--red); color: var(--red);
        }
        .state-cell.index { color: var(--muted); font-size: 10px; }

        /* Round nav */
        .round-nav { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
        .round-dot {
            width: 20px; height: 20px; border-radius: 50%;
            background: var(--border); border: 1px solid var(--border);
            cursor: pointer; transition: .2s;
        }
        .round-dot.col { background: #1f3a5f; }
        .round-dot.diag { background: #1f3a2d; }
        .round-dot.active { border-color: var(--accent); transform: scale(1.3); }

        /* Notice */
        .notice {
            background: #161d2f; border: 1px solid #264a8f;
            border-radius: 6px; padding: 10px 14px; font-size: 12px;
            color: #79b8ff; margin-bottom: 12px;
        }

        /* Spinner */
        .spinner {
            width: 16px; height: 16px; border: 2px solid transparent;
            border-top-color: currentColor; border-radius: 50%;
            animation: spin .6s linear infinite; display: inline-block;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* Responsive */
        @media (min-width: 768px) {
            .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        }
    </style>
</head>
<body x-data="chacha20App()" x-init="init()">

<header>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2">
        <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
    <h1>ChaCha20 Simulator</h1>
    <span class="badge">RFC 8439 · Pure Python</span>
    <span class="badge" style="margin-left:auto; border-color: var(--green); color: var(--green); background: #1f3a2d"
          x-text="serviceStatus">checking…</span>
</header>

<div class="container">
    <div class="notice">
        ⚡ Microservice Python berjalan di <code x-text="apiUrl">{{ $apiUrl }}</code>.
        Semua operasi kriptografi diproses di server Python tanpa library eksternal.
    </div>

    <div class="two-col">
        <!-- ─── LEFT: Input Panel ─── -->
        <div>
            <!-- Mode Tab -->
            <div class="card">
                <div class="card-title">Mode Operasi</div>
                <div class="tab-group">
                    <div class="tab" :class="{ active: mode === 'encrypt' }" @click="mode = 'encrypt'; resetResult()">
                        🔒 Enkripsi
                    </div>
                    <div class="tab" :class="{ active: mode === 'decrypt' }" @click="mode = 'decrypt'; resetResult()">
                        🔓 Dekripsi
                    </div>
                    <div class="tab" :class="{ active: mode === 'steps' }" @click="mode = 'steps'; resetResult()">
                        🔬 Visualisasi
                    </div>
                </div>

                <!-- Plaintext (Encrypt/Steps) -->
                <div class="form-group" x-show="mode !== 'decrypt'">
                    <label>Plaintext</label>
                    <textarea x-model="plaintext" placeholder="Masukkan teks yang akan dienkripsi…"></textarea>
                </div>

                <!-- Ciphertext (Decrypt) -->
                <div class="form-group" x-show="mode === 'decrypt'">
                    <label>Ciphertext (hex)</label>
                    <textarea x-model="ciphertextInput" placeholder="Masukkan ciphertext dalam format hex…"></textarea>
                </div>
            </div>

            <!-- Key & Nonce -->
            <div class="card">
                <div class="card-title">Key & Nonce</div>

                <div class="form-group">
                    <label>Key (256-bit · 64 karakter hex)</label>
                    <div class="key-row">
                        <div class="form-group">
                            <input type="text" x-model="key" placeholder="Kosongkan untuk auto-generate…" maxlength="64">
                        </div>
                        <button class="btn btn-outline btn-sm" @click="generateKey()" :disabled="loading">
                            <span x-show="loading" class="spinner"></span>
                            🎲 Generate
                        </button>
                    </div>
                    <p x-show="keyError" x-text="keyError" style="color:var(--red); font-size:11px; margin-top:4px;"></p>
                </div>

                <div class="form-group">
                    <label>Nonce (96-bit · 24 karakter hex)</label>
                    <input type="text" x-model="nonce" placeholder="Kosongkan untuk auto-generate…" maxlength="24">
                    <p x-show="nonceError" x-text="nonceError" style="color:var(--red); font-size:11px; margin-top:4px;"></p>
                </div>

                <div class="form-group">
                    <label>Block Counter (default: 1)</label>
                    <input type="text" x-model="counter" placeholder="1" style="width:100px">
                </div>

                <!-- Show rounds toggle (Encrypt only) -->
                <div x-show="mode === 'encrypt'" style="display:flex; align-items:center; gap:8px; margin-top:4px;">
                    <input type="checkbox" id="showRounds" x-model="showRounds" style="width:auto">
                    <label for="showRounds" style="margin-bottom:0; cursor:pointer;">
                        Sertakan round logs (slow ⚠️)
                    </label>
                </div>
            </div>

            <!-- Action Button -->
            <button class="btn btn-primary" style="width:100%; justify-content:center"
                    @click="run()" :disabled="loading">
                <span x-show="loading" class="spinner"></span>
                <span x-show="mode === 'encrypt'">🔒 Enkripsi</span>
                <span x-show="mode === 'decrypt'">🔓 Dekripsi</span>
                <span x-show="mode === 'steps'">🔬 Lihat State Matrix</span>
            </button>
        </div>

        <!-- ─── RIGHT: Result Panel ─── -->
        <div>
            <!-- Error -->
            <div class="card" x-show="error">
                <div class="card-title" style="color:var(--red)">⛔ Error</div>
                <div class="result-box error" x-text="error"></div>
            </div>

            <!-- Encrypt / Decrypt Result -->
            <div class="card" x-show="result && mode !== 'steps'">
                <div class="card-title" x-text="mode === 'encrypt' ? '🔒 Hasil Enkripsi' : '🔓 Hasil Dekripsi'"></div>

                <template x-if="mode === 'encrypt' && result">
                    <div>
                        <div class="form-group">
                            <label>Ciphertext (hex)</label>
                            <div class="result-box" x-text="result.ciphertext_hex"></div>
                        </div>
                        <div class="form-group">
                            <label>Ciphertext (base64)</label>
                            <div class="result-box" x-text="result.ciphertext_base64"></div>
                        </div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px;">
                            <div style="font-size:12px; color:var(--muted)">Key: <code x-text="result.key_hex" style="color:var(--accent)"></code></div>
                        </div>
                        <div style="font-size:12px; color:var(--muted); margin-top:4px;">
                            Nonce: <code x-text="result.nonce_hex" style="color:var(--accent)"></code>
                        </div>
                        <div style="font-size:11px; color:var(--muted); margin-top:8px;">
                            Panjang: <span x-text="result.plaintext_length"></span> byte → <span x-text="result.ciphertext_length"></span> byte
                        </div>
                    </div>
                </template>

                <template x-if="mode === 'decrypt' && result">
                    <div>
                        <div class="form-group">
                            <label>Plaintext</label>
                            <div class="result-box" x-text="result.plaintext"></div>
                        </div>
                        <div class="form-group">
                            <label>Plaintext (hex)</label>
                            <div class="result-box" x-text="result.plaintext_hex"></div>
                        </div>
                    </div>
                </template>

                <!-- Inline round logs (jika show_rounds aktif) -->
                <template x-if="result && result.round_logs && result.round_logs.length">
                    <div style="margin-top:12px;">
                        <div class="card-title">📋 Round Logs (<span x-text="result.round_logs.length"></span> entries)</div>
                        <p style="font-size:12px; color:var(--muted)">
                            Gunakan tab <strong>🔬 Visualisasi</strong> untuk melihat state matrix interaktif.
                        </p>
                    </div>
                </template>
            </div>

            <!-- Steps / State Matrix Viewer -->
            <div class="card" x-show="mode === 'steps' && stepsData">
                <div class="card-title">🔬 State Matrix Viewer</div>

                <template x-if="stepsData">
                    <div>
                        <!-- Summary pills -->
                        <div class="step-summary">
                            <span class="step-pill">20 Rounds</span>
                            <span class="step-pill" x-text="stepsData.summary.quarter_rounds_total + ' Quarter Rounds'"></span>
                            <span class="step-pill" x-text="stepsData.total_steps + ' Log Entries'"></span>
                            <span class="step-pill" style="border-color:var(--green); color:var(--green)">
                                Ciphertext: <span x-text="stepsData.ciphertext_hex.substring(0,16) + '…'"></span>
                            </span>
                        </div>

                        <!-- Round navigation dots -->
                        <div style="margin-bottom: 12px;">
                            <label style="margin-bottom:8px; display:block;">Pilih Ronde (biru = column, hijau = diagonal):</label>
                            <div class="round-nav">
                                <div class="round-dot" style="background:var(--border); border-color:var(--accent);"
                                     :class="{active: currentRound === -1}"
                                     @click="goToRound(-1)" title="Initial State"></div>
                                <template x-for="summary in stepsData.round_summaries" :key="summary.round">
                                    <div class="round-dot"
                                         :class="{
                                             col:    summary.type === 'column',
                                             diag:   summary.type === 'diagonal',
                                             active: currentRound === summary.round
                                         }"
                                         @click="goToRound(summary.round)"
                                         :title="`Round ${summary.round}: ${summary.type}`">
                                    </div>
                                </template>
                                <div class="round-dot" style="background:var(--yellow); border-color:var(--yellow);"
                                     :class="{active: currentRound === 'final'}"
                                     @click="goToRound('final')" title="Final State"></div>
                            </div>
                        </div>

                        <!-- Current round info -->
                        <div style="font-size:12px; color:var(--muted); margin-bottom:8px;"
                             x-text="currentRoundLabel"></div>

                        <!-- 4×4 State Matrix -->
                        <div class="state-matrix">
                            <template x-for="(word, idx) in currentStateWords" :key="idx">
                                <div class="state-cell" :class="{changed: changedIndices.includes(idx)}">
                                    <div class="index" x-text="idx"></div>
                                    <div x-text="word"></div>
                                </div>
                            </template>
                        </div>

                        <!-- Navigation buttons -->
                        <div style="display:flex; gap:8px; margin-top:8px;">
                            <button class="btn btn-outline btn-sm" @click="prevRound()" :disabled="currentRoundIndex <= 0">← Prev</button>
                            <button class="btn btn-outline btn-sm" @click="nextRound()" :disabled="currentRoundIndex >= allRounds.length - 1">Next →</button>
                            <span style="font-size:12px; color:var(--muted); align-self:center;"
                                  x-text="`Ronde ${currentRoundIndex + 1} / ${allRounds.length}`"></span>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</div>

<script>
function chacha20App() {
    return {
        // Config
        apiUrl: '{{ $apiUrl }}',
        csrfToken: document.querySelector('meta[name=csrf-token]').content,

        // State
        mode: 'encrypt',
        loading: false,
        serviceStatus: 'Checking…',

        // Form
        plaintext: '',
        ciphertextInput: '',
        key: '',
        nonce: '',
        counter: 1,
        showRounds: false,

        // Errors
        error: null,
        keyError: null,
        nonceError: null,

        // Results
        result: null,
        stepsData: null,

        // State Matrix Viewer
        allRounds: [],
        currentRoundIndex: 0,
        currentRound: -1,
        currentStateWords: [],
        currentRoundLabel: '',
        changedIndices: [],

        async init() {
            await this.checkService();
        },

        async checkService() {
            try {
                const res = await fetch('{{ route("chacha20.keygen") }}');
                this.serviceStatus = res.ok ? '● Service Online' : '⚠ Service Error';
            } catch {
                this.serviceStatus = '✕ Service Offline';
            }
        },

        resetResult() {
            this.result = null;
            this.stepsData = null;
            this.error = null;
        },

        validate() {
            this.keyError = null;
            this.nonceError = null;

            if (this.key && !/^[0-9a-fA-F]{64}$/.test(this.key)) {
                this.keyError = 'Key harus tepat 64 karakter hexadecimal (256-bit).';
                return false;
            }
            if (this.nonce && !/^[0-9a-fA-F]{24}$/.test(this.nonce)) {
                this.nonceError = 'Nonce harus tepat 24 karakter hexadecimal (96-bit).';
                return false;
            }
            return true;
        },

        async run() {
            if (!this.validate()) return;
            this.loading = true;
            this.error = null;
            this.result = null;
            this.stepsData = null;

            try {
                if (this.mode === 'encrypt') await this.doEncrypt();
                else if (this.mode === 'decrypt') await this.doDecrypt();
                else await this.doSteps();
            } catch (err) {
                this.error = err.message || 'Terjadi error tidak terduga.';
            } finally {
                this.loading = false;
            }
        },

        async generateKey() {
            this.loading = true;
            try {
                const res = await fetch('{{ route("chacha20.keygen") }}');
                const data = await res.json();
                this.key = data.key_hex;
                this.nonce = data.nonce_hex;
            } catch {
                this.error = 'Gagal generate key. Pastikan microservice berjalan.';
            } finally {
                this.loading = false;
            }
        },

        async doEncrypt() {
            const body = {
                plaintext: this.plaintext,
                counter: parseInt(this.counter) || 1,
                show_rounds: this.showRounds,
            };
            if (this.key) body.key = this.key;
            if (this.nonce) body.nonce = this.nonce;

            const data = await this.apiPost('{{ route("chacha20.encrypt") }}', body);
            this.result = data;
            // Simpan key/nonce yang dipakai untuk kemudahan dekripsi
            this.key = data.key_hex;
            this.nonce = data.nonce_hex;
        },

        async doDecrypt() {
            if (!this.ciphertextInput) throw new Error('Ciphertext tidak boleh kosong.');
            if (!this.key) throw new Error('Key wajib diisi untuk dekripsi.');
            if (!this.nonce) throw new Error('Nonce wajib diisi untuk dekripsi.');

            const data = await this.apiPost('{{ route("chacha20.decrypt") }}', {
                ciphertext_hex: this.ciphertextInput.trim(),
                key: this.key,
                nonce: this.nonce,
                counter: parseInt(this.counter) || 1,
                show_rounds: this.showRounds,
            });
            this.result = data;
        },

        async doSteps() {
            if (!this.plaintext) throw new Error('Plaintext diperlukan untuk visualisasi.');

            const body = {
                plaintext: this.plaintext,
                counter: parseInt(this.counter) || 1,
            };
            if (this.key) body.key = this.key;
            if (this.nonce) body.nonce = this.nonce;

            const data = await this.apiPost('{{ route("chacha20.steps") }}', body);
            this.stepsData = data;
            this.key = data.key_hex;
            this.nonce = data.nonce_hex;
            this.buildRoundList(data);
        },

        buildRoundList(data) {
            this.allRounds = [
                data.initial_state,
                ...data.round_summaries,
                data.final_state,
            ].filter(Boolean);

            this.currentRoundIndex = 0;
            this.displayRound(0);
        },

        displayRound(idx) {
            const entry = this.allRounds[idx];
            if (!entry) return;

            this.currentRound = entry.round;
            this.currentStateWords = entry.state_words ?? [];
            this.currentRoundLabel = entry.description ?? '';

            // Highlight kata yang berubah dibanding ronde sebelumnya
            if (idx > 0) {
                const prev = this.allRounds[idx - 1].state_words ?? [];
                this.changedIndices = this.currentStateWords
                    .map((w, i) => w !== prev[i] ? i : -1)
                    .filter(i => i >= 0);
            } else {
                this.changedIndices = [];
            }
        },

        goToRound(round) {
            const idx = this.allRounds.findIndex(r => r?.round === round);
            if (idx >= 0) {
                this.currentRoundIndex = idx;
                this.displayRound(idx);
            }
        },

        prevRound() {
            if (this.currentRoundIndex > 0) {
                this.currentRoundIndex--;
                this.displayRound(this.currentRoundIndex);
            }
        },

        nextRound() {
            if (this.currentRoundIndex < this.allRounds.length - 1) {
                this.currentRoundIndex++;
                this.displayRound(this.currentRoundIndex);
            }
        },

        async apiPost(url, body) {
            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': this.csrfToken,
                    'Accept': 'application/json',
                },
                body: JSON.stringify(body),
            });
            const data = await res.json();

            if (!res.ok) {
                // Tampilkan pesan validasi Laravel jika ada
                if (data.errors) {
                    const msgs = Object.values(data.errors).flat().join(' ');
                    throw new Error(msgs);
                }
                throw new Error(data.message || data.error || 'API Error');
            }
            return data;
        },
    };
}
</script>
</body>
</html>
