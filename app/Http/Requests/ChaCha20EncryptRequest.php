<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ChaCha20EncryptRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'plaintext'   => ['required', 'string', 'min:1', 'max:10000'],

            // Key: opsional. Jika diberikan, harus tepat 64 karakter hex (256-bit)
            'key'         => ['nullable', 'string', 'regex:/^[0-9a-fA-F]{64}$/'],

            // Nonce: opsional. Jika diberikan, harus tepat 24 karakter hex (96-bit)
            'nonce'       => ['nullable', 'string', 'regex:/^[0-9a-fA-F]{24}$/'],

            'counter'     => ['nullable', 'integer', 'min:0', 'max:4294967295'],
            'show_rounds' => ['nullable', 'boolean'],
        ];
    }

    public function messages(): array
    {
        return [
            'plaintext.required' => 'Plaintext tidak boleh kosong.',
            'plaintext.max'      => 'Plaintext maksimal 10.000 karakter.',
            'key.regex'          => 'Key harus tepat 64 karakter hexadecimal (256-bit).',
            'nonce.regex'        => 'Nonce harus tepat 24 karakter hexadecimal (96-bit).',
            'counter.integer'    => 'Counter harus berupa bilangan bulat.',
            'counter.max'        => 'Counter maksimal 2^32 - 1.',
        ];
    }
}
