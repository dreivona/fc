import requests
import datetime
import json
import os

LATITUDE = 52.23
LONGITUDE = 21.01
FILENAME = "pogoda_cache.json"

def pobierz_date():
    s = input("Data (YYYY-MM-DD), ENTER = jutro: ").strip()
    if not s:
        return (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    try:
        datetime.datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        print("Błąd: Nieprawidłowy format, spróbuj ponownie.")
        return pobierz_date()

def wczytaj_cache():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf‑8") as f:
            return json.load(f)
    return {}

def zapisz_cache(d):
    with open(FILENAME, "w", encoding="utf‑8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def pobierz_opady(d):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon"
        f"&start_date={d}&end_date={d}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    rain = data.get("daily", {}).get("rain_sum", [None])[0]
    return rain

def sprawdz(d):
    cache = wczytaj_cache()
    if d in cache:
        print(f"{d}: {cache[d]} (z pliku)")
        return
    rain = pobierz_opady(d)
    if rain is None or rain < 0:
        wynik = "Nie wiem."
    elif rain == 0.0:
        wynik = "Nie będzie padać."
    else:
        wynik = "Będzie padać."
    cache[d] = wynik
    zapisz_cache(cache)
    print(f"{d}: {wynik}")

if __name__ == "__main__":
    date = pobierz_date()
    sprawdz(date)
