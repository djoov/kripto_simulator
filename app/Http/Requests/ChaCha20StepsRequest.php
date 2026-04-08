<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Form Request untuk endpoint /chacha20/steps.
 *
 * Endpoint ini khusus untuk keperluan visualisasi State Matrix Viewer.
 * Memaksa show_rounds = true agar round_logs selalu dikembalikan.
 */
class ChaCha20StepsRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'plaintext' => ['required', 'string', 'min:1', 'max:10000'],

            // Key: opsional. Jika diberikan, harus tepat 64 karakter hex (256-bit)
            'key'       => ['nullable', 'string', 'regex:/^[0-9a-fA-F]{64}$/'],

            // Nonce: opsional. Jika diberikan, harus tepat 24 karakter hex (96-bit)
            'nonce'     => ['nullable', 'string', 'regex:/^[0-9a-fA-F]{24}$/'],

            'counter'   => ['nullable', 'integer', 'min:0', 'max:4294967295'],
        ];
    }

    public function messages(): array
    {
        return [
            'plaintext.required' => 'Plaintext diperlukan untuk melihat step visualisasi.',
            'key.regex'          => 'Key harus tepat 64 karakter hexadecimal (256-bit).',
            'nonce.regex'        => 'Nonce harus tepat 24 karakter hexadecimal (96-bit).',
        ];
    }
}
