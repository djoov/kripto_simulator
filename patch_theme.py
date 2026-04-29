import re

with open('resources/views/chacha20/index.blade.php', 'r', encoding='utf-8') as f:
    content = f.read()

new_html = """    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg:       #000000;
            --surface:  #000000;
            --border:   #00ff00;
            --accent:   #00ff00;
            --green:    #00ff00;
            --red:      #ff003c;
            --yellow:   #ffaa00;
            --text:     #00ff00;
            --muted:    #008800;
            --radius:   0px;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            min-height: 100vh;
            text-shadow: 0 0 2px rgba(0, 255, 0, 0.5);
        }

        ::selection { background: var(--text); color: var(--bg); }

        /* Layout */
        header {
            padding: 16px 24px;
            border-bottom: 1px dashed var(--border);
            margin-bottom: 20px;
        }
        .prompt { color: var(--accent); font-weight: bold; }
        .prompt-dir { color: #008800; }
        .prompt-cmd { color: var(--text); }
        
        .container { max-width: 1100px; margin: 0 auto; padding: 0 16px 40px; }

        /* Cards */
        .card {
            border: 1px solid var(--border);
            padding: 16px;
            margin-bottom: 24px;
            position: relative;
        }
        .card::before {
            content: "+"; position: absolute; top: -7px; left: -5px; background: var(--bg); color: var(--border);
        }
        .card::after {
            content: "+"; position: absolute; top: -7px; right: -5px; background: var(--bg); color: var(--border);
        }
        .card-title {
            font-size: 14px; font-weight: bold; color: var(--accent);
            text-transform: uppercase; margin-bottom: 14px;
            display: inline-block;
            background: var(--bg);
            padding: 0 8px;
            position: absolute;
            top: -10px;
            left: 16px;
        }

        /* Form */
        .form-group { margin-bottom: 16px; margin-top: 10px; }
        label { display: block; font-size: 12px; color: var(--accent); margin-bottom: 6px; }
        input[type=text], textarea {
            width: 100%; padding: 8px 12px;
            background: transparent; border: 1px solid var(--muted);
            color: var(--text); font-size: 14px;
            font-family: inherit;
        }
        input[type=text]:focus, textarea:focus {
            outline: none; border-color: var(--accent);
            box-shadow: 0 0 5px rgba(0,255,0,0.3);
        }
        textarea { resize: vertical; min-height: 80px; }

        /* Buttons */
        .btn {
            display: inline-flex; align-items: center; justify-content: center; gap: 8px;
            padding: 8px 16px; font-size: 14px;
            font-family: inherit; font-weight: bold; text-transform: uppercase;
            cursor: pointer; transition: all .2s;
            background: transparent; color: var(--accent);
            border: 1px solid var(--accent);
        }
        .btn:disabled { opacity: .5; cursor: not-allowed; border-color: var(--muted); color: var(--muted); }
        .btn:not(:disabled):hover { background: var(--accent); color: var(--bg); text-shadow: none; }
        .btn-primary  { /* inherit base btn styles */ }
        .btn-outline  { /* inherit base btn styles */ }
        .btn-sm { padding: 4px 8px; font-size: 12px; }

        /* Toggle tab */
        .tab-group {
            display: flex; gap: 16px; margin-bottom: 24px;
            padding-top: 8px;
        }
        .tab {
            cursor: pointer; font-size: 14px;
            color: var(--muted);
        }
        .tab::before { content: "[ "; }
        .tab::after { content: " ]"; }
        .tab.active { color: var(--accent); font-weight: bold; }
        .tab.active::before { content: "[*"; }
        .tab.active::after { content: "*]"; }
        .tab:hover { color: var(--accent); }

        /* Key/nonce row */
        .key-row { display: flex; gap: 12px; align-items: flex-end; }
        .key-row .form-group { flex: 1; margin-bottom: 0; margin-top:0; }

        /* Result */
        .result-box {
            font-size: 14px;
            background: transparent; border: 1px dashed var(--muted);
            padding: 12px; word-break: break-all;
            white-space: pre-wrap; color: var(--text); min-height: 48px;
        }
        .result-box.error { color: var(--red); border-color: var(--red); }
        .result-box.muted { color: var(--muted); }

        /* Steps summary */
        .step-summary {
            display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; margin-top: 10px;
        }
        .step-pill {
            border-bottom: 1px solid var(--accent);
            padding-bottom: 2px;
            font-size: 12px;
        }

        /* State matrix grid */
        .state-matrix {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 2px; margin-bottom: 16px;
        }
        .state-cell {
            border: 1px dotted var(--muted);
            padding: 8px 4px;
            text-align: center; color: var(--accent);
        }
        .state-cell.changed {
            background: var(--text); color: var(--bg); text-shadow: none; font-weight: bold;
        }
        .state-cell.index { color: var(--muted); font-size: 10px; display:block; margin-bottom: 4px; }

        /* Round nav */
        .round-nav { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 16px;}
        .round-dot {
            width: 24px; height: 24px; display:flex; align-items:center; justify-content:center;
            border: 1px solid var(--muted); color: var(--muted);
            cursor: pointer; font-size: 10px;
        }
        .round-dot.col { color: #00aaaa; border-color: #00aaaa; }
        .round-dot.diag { color: #aaaa00; border-color: #aaaa00; }
        .round-dot.active { 
            background: var(--accent); color: var(--bg); border-color: var(--accent); 
            font-weight: bold; text-shadow: none;
        }

        /* Notice */
        .notice {
            border-left: 4px solid var(--accent);
            padding: 8px 16px; font-size: 12px;
            color: var(--muted); margin-bottom: 24px;
        }

        /* Spinner */
        .spinner {
            display: inline-block;
        }
        .spinner::after {
            content: '|';
            animation: terminal-spin .5s infinite linear;
            display: inline-block;
            width: 10px; text-align: center;
        }
        @keyframes terminal-spin {
            0% { content: '|'; }
            25% { content: '/'; }
            50% { content: '-'; }
            75% { content: '\\'; }
        }
        
        /* Cursor blink */
        .cursor-blink {
            animation: blink 1s step-end infinite;
            background: var(--accent); color: var(--bg);
            display: inline-block; width: 8px; height: 16px; vertical-align: middle;
        }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        /* Responsive */
        @media (min-width: 768px) {
            .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        }
    </style>
</head>
<body x-data="chacha20App()" x-init="init()">

<header>
    <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
        <div>
            <span class="prompt">root@kripto-sim</span>:<span class="prompt-dir">~/chacha20</span>$ <span class="prompt-cmd">./run_simulator.sh</span><span class="cursor-blink"></span>
        </div>
        <div style="font-size: 12px; color: var(--muted);" x-text="serviceStatus">[ checking... ]</div>
    </div>
</header>

<div class="container">
    <div class="notice">
        > SYSTEM BOOT: CHACHA20 STREAM CIPHER (RFC 8439)<br>
        > ENGINE: PYTHON MICROSERVICE @ <span x-text="apiUrl">{{ $apiUrl }}</span><br>
        > STATUS: READY FOR INPUT
    </div>

    <div class="two-col">
        <!-- ─── LEFT: Input Panel ─── -->
        <div>
            <div class="tab-group">
                <div class="tab" :class="{ active: mode === 'encrypt' }" @click="mode = 'encrypt'; resetResult()">ENCRYPT</div>
                <div class="tab" :class="{ active: mode === 'decrypt' }" @click="mode = 'decrypt'; resetResult()">DECRYPT</div>
                <div class="tab" :class="{ active: mode === 'steps' }" @click="mode = 'steps'; resetResult()">VISUALIZE</div>
            </div>

            <!-- Input Data Card -->
            <div class="card">
                <div class="card-title">DATA INPUT</div>

                <!-- Plaintext (Encrypt/Steps) -->
                <div class="form-group" x-show="mode !== 'decrypt'">
                    <label>> PLAINTEXT_</label>
                    <textarea x-model="plaintext" placeholder="Enter string data..."></textarea>
                </div>

                <!-- Ciphertext (Decrypt) -->
                <div class="form-group" x-show="mode === 'decrypt'">
                    <label>> CIPHERTEXT_HEX_</label>
                    <textarea x-model="ciphertextInput" placeholder="Enter hex data..."></textarea>
                </div>
            </div>

            <!-- Parameters Card -->
            <div class="card">
                <div class="card-title">PARAMETERS</div>

                <div class="form-group">
                    <label>> KEY_256BIT_ (64 HEX CHARS)</label>
                    <div class="key-row">
                        <div class="form-group">
                            <input type="text" x-model="key" placeholder="Leave blank for auto-generation..." maxlength="64">
                        </div>
                        <button class="btn btn-outline btn-sm" @click="generateKey()" :disabled="loading">
                            <span x-show="loading" class="spinner"></span>
                            <span x-show="!loading">[GEN]</span>
                        </button>
                    </div>
                    <p x-show="keyError" x-text="keyError" style="color:var(--red); font-size:11px; margin-top:4px;"></p>
                </div>

                <div class="form-group">
                    <label>> NONCE_96BIT_ (24 HEX CHARS)</label>
                    <input type="text" x-model="nonce" placeholder="Leave blank for auto-generation..." maxlength="24">
                    <p x-show="nonceError" x-text="nonceError" style="color:var(--red); font-size:11px; margin-top:4px;"></p>
                </div>

                <div class="form-group">
                    <label>> INITIAL_COUNTER_</label>
                    <input type="text" x-model="counter" placeholder="1" style="width:120px">
                </div>

                <!-- Show rounds toggle (Encrypt only) -->
                <div x-show="mode === 'encrypt'" style="display:flex; align-items:center; gap:8px; margin-top:16px;">
                    <input type="checkbox" id="showRounds" x-model="showRounds" style="width:auto; accent-color: var(--accent);">
                    <label for="showRounds" style="margin-bottom:0; cursor:pointer; color:var(--muted)">
                        --enable-verbose-logs (slow)
                    </label>
                </div>
            </div>

            <!-- Action Button -->
            <button class="btn" style="width:100%; padding:12px;" @click="run()" :disabled="loading">
                <span x-show="loading" class="spinner"></span>
                <span x-show="!loading && mode === 'encrypt'">> EXECUTE: ENCRYPT</span>
                <span x-show="!loading && mode === 'decrypt'">> EXECUTE: DECRYPT</span>
                <span x-show="!loading && mode === 'steps'">> EXECUTE: VISUALIZE MATRIX</span>
            </button>
        </div>

        <!-- ─── RIGHT: Result Panel ─── -->
        <div>
            <!-- Error -->
            <div class="card" x-show="error" style="border-color:var(--red)">
                <div class="card-title" style="color:var(--red)">SYSTEM_ERROR</div>
                <div class="result-box error" x-text="error"></div>
            </div>

            <!-- Encrypt / Decrypt Result -->
            <div class="card" x-show="result && mode !== 'steps'">
                <div class="card-title">EXECUTION_RESULT</div>

                <template x-if="mode === 'encrypt' && result">
                    <div>
                        <div class="form-group">
                            <label>OUTPUT_CIPHERTEXT_HEX:</label>
                            <div class="result-box" x-text="result.ciphertext_hex"></div>
                        </div>
                        <div class="form-group">
                            <label>OUTPUT_CIPHERTEXT_BASE64:</label>
                            <div class="result-box" x-text="result.ciphertext_base64"></div>
                        </div>
                        <div style="font-size:12px; color:var(--muted); margin-top:12px; border-top:1px dashed var(--muted); padding-top:8px;">
                            KEY USED   : <span x-text="result.key_hex" style="color:var(--accent)"></span><br>
                            NONCE USED : <span x-text="result.nonce_hex" style="color:var(--accent)"></span><br>
                            SIZE IN    : <span x-text="result.plaintext_length"></span> BYTES<br>
                            SIZE OUT   : <span x-text="result.ciphertext_length"></span> BYTES
                        </div>
                    </div>
                </template>

                <template x-if="mode === 'decrypt' && result">
                    <div>
                        <div class="form-group">
                            <label>OUTPUT_PLAINTEXT_ASCII:</label>
                            <div class="result-box" x-text="result.plaintext"></div>
                        </div>
                        <div class="form-group">
                            <label>OUTPUT_PLAINTEXT_HEX:</label>
                            <div class="result-box" x-text="result.plaintext_hex"></div>
                        </div>
                    </div>
                </template>

                <!-- Inline round logs -->
                <template x-if="result && result.round_logs && result.round_logs.length">
                    <div style="margin-top:16px;">
                        <label>VERBOSE_LOGS_ENABLED (<span x-text="result.round_logs.length"></span> ENTRIES):</label>
                        <div class="result-box muted" style="max-height:200px; overflow-y:auto;">
                            [LOGS SAVED TO BUFFER. USE VISUALIZE MODE FOR INTERACTIVE INSPECTION]
                        </div>
                    </div>
                </template>
            </div>

            <!-- Steps / State Matrix Viewer -->
            <div class="card" x-show="mode === 'steps' && stepsData">
                <div class="card-title">STATE_MATRIX_VIEWER</div>

                <template x-if="stepsData">
                    <div>
                        <div class="step-summary">
                            <div class="step-pill">ROUNDS: 20</div>
                            <div class="step-pill">Q-ROUNDS: <span x-text="stepsData.summary.quarter_rounds_total"></span></div>
                            <div class="step-pill">LOGS: <span x-text="stepsData.total_steps"></span></div>
                            <div class="step-pill">OUT: <span x-text="stepsData.ciphertext_hex.substring(0,16) + '...'"></span></div>
                        </div>

                        <!-- Round navigation dots -->
                        <div style="margin-bottom: 16px;">
                            <label>> SELECT_TICK:</label>
                            <div class="round-nav">
                                <div class="round-dot" :class="{active: currentRound === -1}" @click="goToRound(-1)" title="Initial State">I</div>
                                <template x-for="summary in stepsData.round_summaries" :key="summary.round">
                                    <div class="round-dot"
                                         :class="{
                                             col:    summary.type === 'column',
                                             diag:   summary.type === 'diagonal',
                                             active: currentRound === summary.round
                                         }"
                                         @click="goToRound(summary.round)"
                                         :title="`Round ${summary.round}: ${summary.type}`"
                                         x-text="summary.round">
                                    </div>
                                </template>
                                <div class="round-dot" :class="{active: currentRound === 'final'}" @click="goToRound('final')" title="Final State">F</div>
                            </div>
                        </div>

                        <div style="font-size:12px; color:var(--accent); margin-bottom:8px;" x-text="'> ' + currentRoundLabel"></div>

                        <!-- 4x4 State Matrix -->
                        <div class="state-matrix">
                            <template x-for="(word, idx) in currentStateWords" :key="idx">
                                <div class="state-cell" :class="{changed: changedIndices.includes(idx)}">
                                    <span class="index" x-text="`[${idx}]`"></span>
                                    <span x-text="word"></span>
                                </div>
                            </template>
                        </div>

                        <!-- Navigation buttons -->
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px;">
                            <button class="btn btn-outline btn-sm" @click="prevRound()" :disabled="currentRoundIndex <= 0">< PREV</button>
                            <span style="font-size:12px; color:var(--muted);" x-text="`TICK ${currentRoundIndex + 1}/${allRounds.length}`"></span>
                            <button class="btn btn-outline btn-sm" @click="nextRound()" :disabled="currentRoundIndex >= allRounds.length - 1">NEXT ></button>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</div>
"""

# Replace content using regex
pattern = re.compile(r'    <style>.*?</style>\s*</head>\s*<body[^>]*>.*?(?=\n<script>)', re.DOTALL)
new_content = pattern.sub(new_html, content)

with open('resources/views/chacha20/index.blade.php', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Patch applied successfully.")
