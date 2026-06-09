import sys
from datetime import datetime
import json
import requests

# Exakte Startzeit protokollieren (wichtig für die Cron-Analyse)
jetzt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
print(f"=== DIAGNOSE START ===")
print(f"[ZEIT] Skript feuert um: {jetzt}")

# Deine Wunsch-URL für den Test
URL = "https://oeffentlichevergabe.de/api/notice-exports?pubDay=2023-12-24"

# Wir bauen einen soliden Browser-Header nach, um nicht sofort aufzufallen
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://oeffentlichevergabe.de",
    "Origin": "https://oeffentlichevergabe.de",
}

try:
    print(f"[INFO] Sende Anfrage an: {URL}")
    response = requests.get(URL, headers=headers, timeout=20)

    print(f"[STATUS] HTTP-Code vom Server: {response.status_code}")

    # Erfolgsfall
    if response.status_code == 200:
        print("[ERFOLG] Daten erfolgreich abgerufen!")
        # Zeige die ersten 200 Zeichen der JSON-Antwort zur Kontrolle
        print(f"[VORSCHAU]: {response.text[:800]}...")

    # Fehlerfall (WAF, Block, Rate-Limit)
    else:
        print(
            f"[ALARM] Fehler festgestellt! Status-Code ist nicht 200."
        )
        print("=== SERVER ANTWORT-HEADER ===")
        print(json.dumps(dict(response.headers), indent=2))
        print("=== BODY VORSCHAU ===")
        print(response.text[:1000])

except requests.exceptions.Timeout:
    print("[FEHLER] Timeout! Der Server hat gar nicht geantwortet (IP-Drop?).")
except requests.exceptions.RequestException as e:
    print(f"[NETZWERKFEHLER] Verbindung fehlgeschlagen: {e}")

print("=== DIAGNOSE ENDE ===")
