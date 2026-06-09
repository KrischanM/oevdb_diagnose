from datetime import datetime
import json
import httpx  # Ersetzt requests für HTTP/2 Support

jetzt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
print(f"=== MODERNISIERTE DIAGNOSE START ===")
print(f"[ZEIT] Skript feuert um: {jetzt}")

base_api = "https://oeffentlichevergabe.de/api/notice-exports"
params = {"pubDay": "2023-12-24", "format": "ocds.zip"}

# Wir fügen die Komprimierungs-Header hinzu, die dein Firefox nutzt
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de-DE,de;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",  # Zwingend für Brotli!
    "Referer": "https://oeffentlichevergabe.de",
    "Origin": "https://oeffentlichevergabe.de",
}

try:
    print(f"[INFO] Sende HEAD-Anfrage via HTTP/2 an: {base_api}")

    # http2=True aktiviert die moderne Browser-Verbindung
    with httpx.Client(http2=True) as client:
        response = client.head(base_api, params=params, headers=headers, timeout=20.0)

        print(f"[STATUS] HTTP-Code vom Server: {response.status_code}")
        print(f"[PROTOKOLL] Genutzte HTTP-Version: {response.http_version}")

        if response.status_code == 200:
            print("[ERFOLG] Daten erfolgreich abgerufen!")
            print("=== SERVER ANTWORT-HEADER ===")
            print(json.dumps(dict(response.headers), indent=2))
        else:
            print(f"[ALARM] Status-Code ist {response.status_code}")
            # Falls HEAD fehlschlägt, holen wir zur Diagnose den GET-Body
            res_get = client.get(base_api, params=params, headers=headers, timeout=20.0)
            print(res_get.text[:500])

except Exception as e:
    print(f"[FEHLER] HTTP/2 Abfrage fehlgeschlagen: {e}")

print("=== DIAGNOSE ENDE ===")
