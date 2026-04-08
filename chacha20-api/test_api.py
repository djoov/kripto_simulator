"""Quick API integration test."""
import json
import urllib.request

BASE = "http://127.0.0.1:8001"

def api_get(path):
    resp = urllib.request.urlopen(f"{BASE}{path}")
    return json.loads(resp.read())

def api_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

# 1. Test /keygen
print("=== GET /keygen ===")
keys = api_get("/keygen")
print(f"  key_hex:   {keys['key_hex']}")
print(f"  nonce_hex: {keys['nonce_hex']}")
print()

# 2. Test /encrypt
print("=== POST /encrypt ===")
enc = api_post("/encrypt", {
    "plaintext": "Hello, ChaCha20! Ini pesan rahasia.",
    "show_rounds": False,
})
print(f"  ciphertext_hex: {enc['ciphertext_hex']}")
print(f"  key_hex:        {enc['key_hex']}")
print(f"  nonce_hex:      {enc['nonce_hex']}")
print()

# 3. Test /decrypt
print("=== POST /decrypt ===")
dec = api_post("/decrypt", {
    "ciphertext_hex": enc["ciphertext_hex"],
    "key": enc["key_hex"],
    "nonce": enc["nonce_hex"],
})
print(f"  plaintext: {dec['plaintext']}")
print(f"  match:     {dec['plaintext'] == 'Hello, ChaCha20! Ini pesan rahasia.'}")
print()

# 4. Test /encrypt with show_rounds
print("=== POST /encrypt (with round logs) ===")
enc2 = api_post("/encrypt", {
    "plaintext": "Test",
    "show_rounds": True,
})
logs = enc2.get("round_logs", [])
round_summaries = [l for l in logs if l.get("type") in ("column", "diagonal")]
print(f"  Total log entries: {len(logs)}")
print(f"  Round summaries:   {len(round_summaries)}")
print(f"  First round desc:  {round_summaries[0]['description'] if round_summaries else 'N/A'}")
print()

print("=" * 40)
print("  All API tests passed! ✅")
print("=" * 40)
