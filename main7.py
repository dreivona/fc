import json
import requests
from datetime import datetime, timedelta
import argparse
import os


class WeatherForecast:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _fetch_from_api(self, date):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude=52.23&longitude=21.01"
            f"&hourly=rain&daily=rain_sum"
            f"&timezone=Europe%2FLondon"
            f"&start_date={date}&end_date={date}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            rain_data = result.get("daily", {}).get("rain_sum", [])
            if not rain_data:
                return "Nie wiem."
            rain = rain_data[0]
            if rain > 0:
                return "Będzie padać."
            elif rain == 0:
                return "Nie będzie padać."
            else:
                return "Nie wiem."
        except Exception:
            return "Nie wiem"

    def __getitem__(self, date):
        if date not in self.data:
            self.data[date] = self._fetch_from_api(date)
            self._save()
        return self.data[date]

    def __setitem__(self, date, value):
        self.data[date] = value
        self._save()

    def __iter__(self):
        return iter(self.data.keys())

    def items(self):
        return ((k, v) for k, v in self.data.items())


def main():
    parser = argparse.ArgumentParser(description="Sprawdź, czy będzie padać danego dnia w Warszawie.")
    parser.add_argument("--date", type=str, help="Data w formacie YYYY-mm-dd (domyślnie jutro).")
    args = parser.parse_args()

    if args.date:
        try:
            date = datetime.strptime(args.date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Błąd: Niepoprawny format daty. Użyj formatu: YYYY-MM-DD.")
            return
    else:
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    weather_forecast = WeatherForecast("pogoda.json")
    result = weather_forecast[date]
    print(f"📅 {date}: {result}")

    print("\n📁 Zapisane dane:")
    for d, r in weather_forecast.items():
        print(f"- {d}: {r}")


if __name__ == "__main__":
    main()
