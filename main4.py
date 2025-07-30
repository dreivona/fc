import json
import os

# Nazwy plików
PLIK_KONTO = "konto.txt"
PLIK_MAGAZYN = "magazyn.txt"
PLIK_HISTORIA = "historia.txt"


def wczytaj_dane():
    """Wczytuje dane z plików przy uruchomieniu programu"""
    konto = 0
    magazyn = {}
    historia = []

    # Wczytanie salda konta
    try:
        if os.path.exists(PLIK_KONTO):
            with open(PLIK_KONTO, 'r', encoding='utf-8') as f:
                konto = float(f.read().strip())
                print(f"Wczytano saldo konta: {konto:.2f} zł")
    except (ValueError, FileNotFoundError):
        print("Nie można wczytać salda konta. Rozpoczynanie z saldem 0.")
        konto = 0

    # Wczytanie magazynu
    try:
        if os.path.exists(PLIK_MAGAZYN):
            with open(PLIK_MAGAZYN, 'r', encoding='utf-8') as f:
                magazyn = json.load(f)
                print(f"Wczytano {len(magazyn)} produktów z magazynu")
    except (json.JSONDecodeError, FileNotFoundError):
        print("Nie można wczytać magazynu. Rozpoczynanie z pustym magazynem.")
        magazyn = {}

    # Wczytanie historii
    try:
        if os.path.exists(PLIK_HISTORIA):
            with open(PLIK_HISTORIA, 'r', encoding='utf-8') as f:
                historia = json.load(f)
                print(f"Wczytano {len(historia)} operacji z historii")
    except (json.JSONDecodeError, FileNotFoundError):
        print("Nie można wczytać historii. Rozpoczynanie z pustą historią.")
        historia = []

    return konto, magazyn, historia


def zapisz_dane(konto, magazyn, historia):
    """Zapisuje wszystkie dane do plików"""
    try:
        # Zapisanie salda konta
        with open(PLIK_KONTO, 'w', encoding='utf-8') as f:
            f.write(str(konto))

        # Zapisanie magazynu
        with open(PLIK_MAGAZYN, 'w', encoding='utf-8') as f:
            json.dump(magazyn, f, ensure_ascii=False, indent=2)

        # Zapisanie historii
        with open(PLIK_HISTORIA, 'w', encoding='utf-8') as f:
            json.dump(historia, f, ensure_ascii=False, indent=2)

        print("Dane zostały zapisane do plików.")
    except Exception as e:
        print(f"Błąd podczas zapisywania danych: {e}")


def pokaz_polecenia():
    print("\n Dostępne polecenia:")
    print("saldo - sprzedaż - zakup - konto - lista - magazyn - przegląd - zapisz - koniec")


# Wczytanie danych przy starcie programu
print("=== SYSTEM ZARZĄDZANIA MAGAZYNEM ===")
print("Wczytywanie danych...")
konto, magazyn, historia = wczytaj_dane()

while True:
    pokaz_polecenia()
    polecenie = input("Podaj polecenie: ").strip().lower()

    if polecenie == "saldo":
        try:
            kwota = float(input("Podaj kwotę do dodania (lub ujemną): "))
            konto += kwota
            historia.append(("saldo", kwota))
        except ValueError:
            print("Błąd. Podano niewłaściwą kwotę.")

    elif polecenie == "sprzedaż":
        produkt = input("Podaj nazwę produktu: ").strip()
        try:
            cena = float(input("Podaj cenę za sztukę: "))
            ilość = int(input("Podaj liczbę sztuk: "))
            if produkt not in magazyn or magazyn[produkt]["ilość"] < ilość:
                print("Błąd: Brak wystarczającej liczby produktów w magazynie.")
            else:
                magazyn[produkt]["ilość"] -= ilość
                konto += cena * ilość
                historia.append(("sprzedaż", produkt, cena, ilość))
        except ValueError:
            print("Błąd: Nieprawidłowa cena lub ilość.")

    elif polecenie == "zakup":
        produkt = input("Podaj nazwę produktu: ").strip()
        try:
            cena = float(input("Podaj cenę za sztukę: "))
            ilość = int(input("Podaj liczbę sztuk: "))
            koszt = cena * ilość
            if cena < 0 or ilość <= 0:
                print("Błąd: Cena oraz ilość muszą być dodatnie.")
            elif konto < koszt:
                print("Błąd: Niewystarczające środki na koncie.")
            else:
                konto -= koszt
                if produkt in magazyn:
                    magazyn[produkt]["ilość"] += ilość
                    magazyn[produkt]["cena"] = cena
                else:
                    magazyn[produkt] = {"cena": cena, "ilość": ilość}
                historia.append(("zakup", produkt, cena, ilość))
        except ValueError:
            print("Błąd: Nieprawidłowa cena bądź ilość.")

    elif polecenie == "konto":
        print(f"Aktualny stan konta: {konto:.2f} zł.")

    elif polecenie == "lista":
        if not magazyn:
            print("Magazyn jest pusty.")
        else:
            print("\nStan magazynu: ")
            for produkt, dane in magazyn.items():
                print(f"- {produkt}: {dane['ilość']} szt. po {dane['cena']} zł.")

    elif polecenie == "magazyn":
        nazwa = input("Podaj nazwę produktu: ").strip()
        if nazwa in magazyn:
            dane = magazyn[nazwa]
            print(f"{nazwa}: {dane['ilość']} szt. po {dane['cena']} zł.")
        else:
            print("Błąd: Nie odnaleziono produktu w magazynie.")

    elif polecenie == "przegląd":
        try:
            od = input("Od którego wpisu (ENTER = od początku): ")
            do = input("DO którego wpisu (ENTER - do końca): ")
            od = int(od) if od else 0
            do = int(do) if do else len(historia)

            if od < 0 or do > len(historia) or od >= do:
                print(f"Nieprawidłowy zakres. Liczba zapisanych operacji: {len(historia)}.")
            else:
                for i, wpis in enumerate(historia[od:do], start=od):
                    print(f"{i}: {wpis}")
        except ValueError:
            print("Błąd: Liczby muszą być całkowite bądź zakresy puste.")

    elif polecenie == "zapisz":
        zapisz_dane(konto, magazyn, historia)

    elif polecenie == "koniec":
        print("Zapisywanie danych przed zakończeniem...")
        zapisz_dane(konto, magazyn, historia)
        print("Zakończono działanie programu.")
        break

    else:
        print("Błąd: Nieznane polecenie.")