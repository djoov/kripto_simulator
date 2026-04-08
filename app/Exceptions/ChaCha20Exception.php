<?php

namespace App\Exceptions;

use Exception;

class ChaCha20Exception extends Exception
{
    public function __construct(
        string $message = 'ChaCha20 microservice error',
        private readonly ?array $apiError = null,
        int $code = 0,
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, $code, $previous);
    }

    /**
     * Get the raw API error details returned by the Python microservice.
     */
    public function getApiError(): ?array
    {
        return $this->apiError;
    }
}
