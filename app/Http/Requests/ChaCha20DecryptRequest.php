<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ChaCha20DecryptRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            // Ciphertext: wajib ada, harus berupa string hex valid
            'ciphertext_hex' => ['required', 'string', 'regex:/^[0-9a-fA-F]+$/', 'min:2'],

            // Key: WAJIB untuk dekripsi, tepat 64 karakter hex (256-bit)
            'key'            => ['required', 'string', 'regex:/^[0-9a-fA-F]{64}$/'],

            // Nonce: WAJIB untuk dekripsi, tepat 24 karakter hex (96-bit)
            'nonce'          => ['required', 'string', 'regex:/^[0-9a-fA-F]{24}$/'],

            'counter'        => ['nullable', 'integer', 'min:0', 'max:4294967295'],
            'show_rounds'    => ['nullable', 'boolean'],
        ];
    }

    public function messages(): array
    {
        return [
            'ciphertext_hex.required' => 'Ciphertext tidak boleh kosong.',
            'ciphertext_hex.regex'    => 'Ciphertext harus berupa string hexadecimal valid.',
            'key.required'            => 'Key wajib diisi untuk dekripsi.',
            'key.regex'               => 'Key harus tepat 64 karakter hexadecimal (256-bit).',
            'nonce.required'          => 'Nonce wajib diisi untuk dekripsi.',
            'nonce.regex'             => 'Nonce harus tepat 24 karakter hexadecimal (96-bit).',
        ];
    }
}
