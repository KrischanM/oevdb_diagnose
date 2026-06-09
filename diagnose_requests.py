import sys
from datetime import datetime
import json
import requests

jetzt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
print("=== 1. TEST: REQUESTS (mit Brotli) ===")
print(f"[ZEIT] Start um: {jetzt}")

base_api = "https://oeffentlichevergabe.de/api/notice-exports"
params = {"pubDay": "2023-12-24", "format": "ocds.zip"}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de-DE,de;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",  # Brotli-Anforderung
    "Referer": "https://oeffentlichevergabe.de",
    "Origin": "https://oeffentlichevergabe.de",
}

try:
    response = requests.head(base_api, params=params, headers=headers, timeout=20)
    if response.status_code == 405:
        response = requests.get(base_api, params=params, headers=headers, timeout=20, stream=True)

    print(f"[STATUS] HTTP-Code: {response.status_code}")
    print("=== SERVER RESPONSE HEADER ===")
    print(json.dumps(dict(response.headers), indent=2))
except Exception as e:
    print(f"[FEHLER] Requests fehlgeschlagen: {e}")

print("=== TEST REQUESTS ENDE ===\n")
