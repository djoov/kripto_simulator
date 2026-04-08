"""
Test suite for the ChaCha20 implementation.

Uses RFC 8439 test vectors to verify correctness.
"""

from chacha20 import (
    quarter_round as qr,
    chacha20_block,
    chacha20_crypt,
    init_state,
    generate_key,
    generate_nonce,
    SIGMA,
)


def test_quarter_round():
    """Test quarter round against RFC 8439 Section 2.1.1 test vector."""
    state = [0x11111111, 0x01020304, 0x9b8d6f43, 0x01234567]
    qr(state, 0, 1, 2, 3)
    assert state[0] == 0xea2a92f4, f"a: expected 0xea2a92f4, got 0x{state[0]:08x}"
    assert state[1] == 0xcb1cf8ce, f"b: expected 0xcb1cf8ce, got 0x{state[1]:08x}"
    assert state[2] == 0x4581472e, f"c: expected 0x4581472e, got 0x{state[2]:08x}"
    assert state[3] == 0x5881c4bb, f"d: expected 0x5881c4bb, got 0x{state[3]:08x}"
    print("✅ Quarter round test passed (RFC 8439 §2.1.1)")


def test_chacha20_block_rfc2_3_2():
    """Test full block against RFC 8439 Section 2.3.2 test vector.

    Key   = 00:01:02:...:1f
    Nonce = 00:00:00:09:00:00:00:4a:00:00:00:00
    Counter = 1
    """
    key = bytes(range(32))
    nonce = bytes([
        0x00, 0x00, 0x00, 0x09,
        0x00, 0x00, 0x00, 0x4a,
        0x00, 0x00, 0x00, 0x00,
    ])
    counter = 1

    keystream, _ = chacha20_block(key, counter, nonce)

    # RFC 8439 §2.3.2 — Serialized block output
    expected = bytes([
        0x10, 0xf1, 0xe7, 0xe4, 0xd1, 0x3b, 0x59, 0x15,
        0x50, 0x0f, 0xdd, 0x1f, 0xa3, 0x20, 0x71, 0xc4,
        0xc7, 0xd1, 0xf4, 0xc7, 0x33, 0xc0, 0x68, 0x03,
        0x04, 0x22, 0xaa, 0x9a, 0xc3, 0xd4, 0x6c, 0x4e,
        0xd2, 0x82, 0x64, 0x46, 0x07, 0x9f, 0xaa, 0x09,
        0x14, 0xc2, 0xd7, 0x05, 0xd9, 0x8b, 0x02, 0xa2,
        0xb5, 0x12, 0x9c, 0xd1, 0xde, 0x16, 0x4e, 0xb9,
        0xcb, 0xd0, 0x83, 0xe8, 0xa2, 0x50, 0x3c, 0x4e,
    ])

    assert keystream == expected, (
        f"Block output mismatch!\n"
        f"  Got:      {keystream.hex()}\n"
        f"  Expected: {expected.hex()}"
    )
    print("✅ ChaCha20 block test passed (RFC 8439 §2.3.2)")


def test_encrypt_decrypt_roundtrip():
    """Test that encrypt → decrypt returns the original plaintext."""
    key = generate_key()
    nonce = generate_nonce()
    plaintext = "Hello, ChaCha20! Ini adalah test enkripsi stream cipher. 🔐"
    plaintext_bytes = plaintext.encode("utf-8")

    ciphertext, _ = chacha20_crypt(key, nonce, plaintext_bytes)
    decrypted, _ = chacha20_crypt(key, nonce, ciphertext)

    assert decrypted == plaintext_bytes, (
        f"Roundtrip failed!\n"
        f"  Original:  {plaintext_bytes.hex()}\n"
        f"  Decrypted: {decrypted.hex()}"
    )
    print("✅ Encrypt/decrypt roundtrip test passed")


def test_encrypt_decrypt_multiblock():
    """Test encryption/decryption with data spanning multiple 64-byte blocks."""
    key = generate_key()
    nonce = generate_nonce()
    plaintext = ("A" * 200).encode("utf-8")  # >3 blocks (200 bytes)

    ciphertext, _ = chacha20_crypt(key, nonce, plaintext)
    assert len(ciphertext) == 200

    decrypted, _ = chacha20_crypt(key, nonce, ciphertext)
    assert decrypted == plaintext
    print("✅ Multi-block encrypt/decrypt test passed")


def test_different_keys_produce_different_output():
    """Different keys must produce different ciphertexts."""
    key1 = generate_key()
    key2 = generate_key()
    nonce = generate_nonce()
    plaintext = b"same plaintext"

    ct1, _ = chacha20_crypt(key1, nonce, plaintext)
    ct2, _ = chacha20_crypt(key2, nonce, plaintext)
    assert ct1 != ct2
    print("✅ Different keys produce different output")


def test_step_logger():
    """Test that step logger records all 20 rounds."""
    key = bytes(range(32))
    nonce = bytes(12)
    _, logs = chacha20_block(key, 0, nonce, enable_logging=True)

    assert logs is not None
    # Should have: 1 initial + 80 QR details + 20 round summaries + 1 final = 102
    # Let's just check we have enough entries and the structure
    initial_logs = [l for l in logs if l["round"] == 0]
    final_logs = [l for l in logs if l["round"] == "final"]
    round_summaries = [
        l for l in logs
        if isinstance(l["round"], int) and l["round"] > 0
        and l.get("type") in ("column", "diagonal")
    ]

    assert len(initial_logs) == 1, f"Expected 1 initial log, got {len(initial_logs)}"
    assert len(final_logs) == 1, f"Expected 1 final log, got {len(final_logs)}"
    assert len(round_summaries) == 20, f"Expected 20 round summaries, got {len(round_summaries)}"
    print(f"✅ Step logger test passed ({len(logs)} total log entries)")


def test_init_state_layout():
    """Verify state matrix layout matches the spec."""
    key = bytes(range(32))
    nonce = bytes([0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x4a, 0x00, 0x00, 0x00, 0x00])
    counter = 1

    state = init_state(key, counter, nonce)

    # Check constants
    assert state[0:4] == SIGMA
    # Check counter
    assert state[12] == 1
    print("✅ State layout test passed")


if __name__ == "__main__":
    print("=" * 50)
    print("  ChaCha20 Test Suite")
    print("=" * 50)
    print()

    test_quarter_round()
    test_chacha20_block_rfc2_3_2()
    test_encrypt_decrypt_roundtrip()
    test_encrypt_decrypt_multiblock()
    test_different_keys_produce_different_output()
    test_step_logger()
    test_init_state_layout()

    print()
    print("=" * 50)
    print("  All tests passed! ✅")
    print("=" * 50)
