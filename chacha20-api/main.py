"""
ChaCha20 Crypto Microservice — FastAPI

Endpoints:
    GET  /          → Service info
    GET  /keygen    → Generate random key + nonce
    POST /encrypt   → Encrypt plaintext with ChaCha20
    POST /decrypt   → Decrypt ciphertext with ChaCha20

All crypto logic is implemented from scratch in chacha20.py
"""

import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Any

from chacha20 import chacha20_crypt, generate_key, generate_nonce


# ─────────────────────────────────────────────
#  FastAPI App
# ─────────────────────────────────────────────

app = FastAPI(
    title="ChaCha20 Crypto Microservice",
    description=(
        "A from-scratch implementation of the ChaCha20 stream cipher (RFC 8439) "
        "with step-by-step round logging for educational visualization.\n\n"
        "**No external cryptographic libraries are used for the core algorithm.**"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
#  Request / Response Schemas
# ─────────────────────────────────────────────

class EncryptRequest(BaseModel):
    plaintext: str = Field(
        ...,
        description="Plaintext to encrypt (UTF-8 string)",
        examples=["Hello, ChaCha20!"],
    )
    key: Optional[str] = Field(
        None,
        description="256-bit key as 64 hex characters. Auto-generated if omitted.",
        examples=["000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"],
    )
    nonce: Optional[str] = Field(
        None,
        description="96-bit nonce as 24 hex characters. Auto-generated if omitted.",
        examples=["000000000000004a00000000"],
    )
    counter: int = Field(
        1,
        description="Initial block counter (default: 1 per RFC 8439)",
    )
    show_rounds: bool = Field(
        False,
        description="If true, include step-by-step round logs (20 rounds) in the response",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "plaintext": "Hello, ChaCha20!",
                    "show_rounds": True,
                }
            ]
        }
    }


class EncryptResponse(BaseModel):
    ciphertext_hex: str
    ciphertext_base64: str
    key_hex: str
    nonce_hex: str
    counter: int
    plaintext_length: int
    ciphertext_length: int
    round_logs: Optional[list[Any]] = None


class DecryptRequest(BaseModel):
    ciphertext_hex: str = Field(
        ...,
        description="Ciphertext as hex string",
    )
    key: str = Field(
        ...,
        description="256-bit key as 64 hex characters (must match encryption key)",
    )
    nonce: str = Field(
        ...,
        description="96-bit nonce as 24 hex characters (must match encryption nonce)",
    )
    counter: int = Field(
        1,
        description="Initial block counter (must match encryption counter)",
    )
    show_rounds: bool = Field(
        False,
        description="If true, include step-by-step round logs in the response",
    )


class DecryptResponse(BaseModel):
    plaintext: str
    plaintext_hex: str
    key_hex: str
    nonce_hex: str
    round_logs: Optional[list[Any]] = None


class KeygenResponse(BaseModel):
    key_hex: str
    key_base64: str
    key_length_bits: int = 256
    nonce_hex: str
    nonce_base64: str
    nonce_length_bits: int = 96


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def _parse_hex(hex_str: str, expected_bytes: int, field_name: str) -> bytes:
    """Parse a hex string and validate its length."""
    hex_str = hex_str.strip().lower()
    try:
        data = bytes.fromhex(hex_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid hex string for '{field_name}': contains non-hex characters",
        )
    if len(data) != expected_bytes:
        raise HTTPException(
            status_code=400,
            detail=(
                f"'{field_name}' must be exactly {expected_bytes} bytes "
                f"({expected_bytes * 2} hex chars), got {len(data)} bytes "
                f"({len(data) * 2} hex chars)"
            ),
        )
    return data


# ─────────────────────────────────────────────
#  Endpoints
# ─────────────────────────────────────────────

@app.get("/", tags=["Info"])
async def root():
    """Service information and algorithm details."""
    return {
        "service": "ChaCha20 Crypto Microservice",
        "version": "1.0.0",
        "implementation": "Pure Python — no external crypto libraries",
        "endpoints": {
            "GET  /keygen":  "Generate random 256-bit key and 96-bit nonce",
            "POST /encrypt": "Encrypt UTF-8 plaintext → hex ciphertext",
            "POST /decrypt": "Decrypt hex ciphertext → UTF-8 plaintext",
            "GET  /docs":    "Interactive Swagger UI documentation",
            "GET  /redoc":   "ReDoc documentation",
        },
        "algorithm": {
            "name": "ChaCha20",
            "specification": "RFC 8439",
            "key_size_bits": 256,
            "nonce_size_bits": 96,
            "counter_size_bits": 32,
            "block_size_bits": 512,
            "rounds": 20,
            "constants": "expand 32-byte k",
            "operations": "ARX (Addition, Rotation, XOR)",
        },
    }


@app.get("/keygen", response_model=KeygenResponse, tags=["Crypto"])
async def keygen():
    """
    Generate a cryptographically secure random key and nonce.

    - **Key**: 256-bit (32 bytes) — suitable for ChaCha20
    - **Nonce**: 96-bit (12 bytes) — must be unique per key usage
    """
    key = generate_key()
    nonce = generate_nonce()

    return KeygenResponse(
        key_hex=key.hex(),
        key_base64=base64.b64encode(key).decode(),
        nonce_hex=nonce.hex(),
        nonce_base64=base64.b64encode(nonce).decode(),
    )


@app.post("/encrypt", response_model=EncryptResponse, tags=["Crypto"])
async def encrypt(req: EncryptRequest):
    """
    Encrypt plaintext using ChaCha20.

    - If `key` or `nonce` are omitted, they will be auto-generated.
    - Set `show_rounds: true` to get step-by-step state matrix logs
      for all 20 rounds (useful for visualization / education).
    """
    # Parse or generate key
    if req.key:
        key = _parse_hex(req.key, 32, "key")
    else:
        key = generate_key()

    # Parse or generate nonce
    if req.nonce:
        nonce = _parse_hex(req.nonce, 12, "nonce")
    else:
        nonce = generate_nonce()

    plaintext_bytes = req.plaintext.encode("utf-8")
    if not plaintext_bytes:
        raise HTTPException(status_code=400, detail="Plaintext cannot be empty")

    ciphertext, logs = chacha20_crypt(
        key, nonce, plaintext_bytes, req.counter, req.show_rounds
    )

    return EncryptResponse(
        ciphertext_hex=ciphertext.hex(),
        ciphertext_base64=base64.b64encode(ciphertext).decode(),
        key_hex=key.hex(),
        nonce_hex=nonce.hex(),
        counter=req.counter,
        plaintext_length=len(plaintext_bytes),
        ciphertext_length=len(ciphertext),
        round_logs=logs,
    )


@app.post("/decrypt", response_model=DecryptResponse, tags=["Crypto"])
async def decrypt(req: DecryptRequest):
    """
    Decrypt ciphertext using ChaCha20.

    The same key, nonce, and counter used during encryption must be provided.
    ChaCha20 is a stream cipher — decryption is identical to encryption (XOR).
    """
    key = _parse_hex(req.key, 32, "key")
    nonce = _parse_hex(req.nonce, 12, "nonce")

    try:
        ciphertext = bytes.fromhex(req.ciphertext_hex.strip())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid hex string for 'ciphertext_hex'",
        )

    if not ciphertext:
        raise HTTPException(status_code=400, detail="Ciphertext cannot be empty")

    plaintext_bytes, logs = chacha20_crypt(
        key, nonce, ciphertext, req.counter, req.show_rounds
    )

    # Attempt UTF-8 decode, fallback to latin-1 for binary data
    try:
        plaintext_str = plaintext_bytes.decode("utf-8")
    except UnicodeDecodeError:
        plaintext_str = plaintext_bytes.decode("latin-1")

    return DecryptResponse(
        plaintext=plaintext_str,
        plaintext_hex=plaintext_bytes.hex(),
        key_hex=key.hex(),
        nonce_hex=nonce.hex(),
        round_logs=logs,
    )
