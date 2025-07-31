#!/usr/bin/env python3
# reader.py

import sys
import csv
import os.path


def wyświetl_pomoc():
    """Wyświetla instrukcję użycia programu"""
    print("Użycie: python reader.py <plik_wejściowy> <plik_wyjściowy> <zmiana_1> <zmiana_2> ... <zmiana_n>")
    print()
    print("Argumenty:")
    print("  <plik_wejściowy>  - nazwa pliku CSV do odczytania (np. in.csv)")
    print("  <plik_wyjściowy>  - nazwa pliku CSV do zapisania (np. out.csv)")
    print("  <zmiana_x>        - zmiany w formacie 'kolumna,wiersz,wartość'")
    print("                      (kolumny i wiersze liczone od 0)")
    print()
    print("Przykład:")
    print("  python reader.py in.csv out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0")
    print()
    print("To zmieni:")
    print("  - komórkę w kolumnie 0, wiersz 0 na 'gitara'")
    print("  - komórkę w kolumnie 3, wiersz 1 na 'kubek'")
    print("  - komórkę w kolumnie 1, wiersz 2 na '17'")
    print("  - komórkę w kolumnie 3, wiersz 3 na '0'")


def parsuj_zmiany(zmiany_args):
    """
    Parsuje argumenty zmian z formatu 'x,y,wartość' na polecenie

    Args:
        zmiany_args: lista stringów z argumentami zmian

    Returns:
        dict: polecenie gdzie klucz to (kolumna, wiersz), wartość to nowa wartość

    Raises:
        ValueError: gdy format zmiany jest nieprawidłowy
    """
    zmiany = {}

    for i, zmiana in enumerate(zmiany_args):
        try:
            części = zmiana.split(',', 2)  # Dzielimy maks na 3 części

            if len(części) != 3:
                raise ValueError(f"Błąd: Niewłaściwy format zmiany: '{zmiana}'. Oczekiwano 'kolumna,wiersz,wartość'")

            kolumna = int(części[0])
            wiersz = int(części[1])
            wartość = części[2]

            if kolumna < 0 or wiersz < 0:
                raise ValueError(f"Kolumna i wiersz muszą być liczbami dodatnimi w zmianie: '{zmiana}'")

            zmiany[(kolumna, wiersz)] = wartość

        except ValueError as e:
            print(f"Błąd: W argumencie {i+3} ('{zmiana}'): {e}", file=sys.stderr)
            sys.exit(1)

    return zmiany


def wczytaj_csv(nazwa_pliku):
    """
    Wczytuje plik CSV do listy list

    Args:
        nazwa_pliku: ścieżka do pliku CSV

    Returns:
        list: lista wierszy, gdzie każdy wiersz to lista komórek

    Raises:
        FileNotFoundError: gdy plik nie istnieje
        Exception: inne błędy przy czytaniu pliku
    """
    try:
        wiersze = []
        with open(nazwa_pliku, 'r', encoding='utf-8', newline='') as plik:
            czytnik = csv.reader(plik)
            for wiersz in czytnik:
                wiersze.append(wiersz)

        print(f"Wczytano {len(wiersze)} wierszy z pliku '{nazwa_pliku}'")
        return wiersze

    except FileNotFoundError:
        print(f"Błąd: Nie można znaleźć pliku '{nazwa_pliku}'", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Błąd: Brak uprawnień do odczytu pliku '{nazwa_pliku}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Błąd: Podczas czytania pliku '{nazwa_pliku}': {e}", file=sys.stderr)
        sys.exit(1)


def zastosuj_zmiany(dane, zmiany):
    """
    Dodaje zmiany do danych CSV

    Args:
        dane: lista list odpowiadająca danym CSV
        zmiany: polecenie zmian gdzie klucz to (kolumna, wiersz)

    Returns:
        list: zmodyfikowane dane CSV
    """
    # Tworzymy kopię danych, żeby nie naruszać oryginału
    zmodyfikowane_dane = [wiersz[:] for wiersz in dane]

    # Znajdź max. potrzebne dane
    max_wiersz = len(zmodyfikowane_dane) - 1
    max_kolumna = max(len(wiersz) - 1 for wiersz in zmodyfikowane_dane) if zmodyfikowane_dane else -1

    zmiany_zastosowane = 0

    for (kolumna, wiersz), wartość in zmiany.items():
        # Sprawdź, czy trzeba rozszerzyć liczbę wierszy
        while wiersz >= len(zmodyfikowane_dane):
            # Dodaj nowy wiersz z odpowiednią liczbą kolumn
            nowy_wiersz = [''] * (max_kolumna + 1)
            zmodyfikowane_dane.append(nowy_wiersz)
            print(f"Dodano nowy wiersz {len(zmodyfikowane_dane)-1}")

        # Sprawdź, czy trzeba rozszerzyć liczbę kolumn w danym wierszu
        while kolumna >= len(zmodyfikowane_dane[wiersz]):
            zmodyfikowane_dane[wiersz].append('')

        # Zapisz starą wartość do logowania
        stara_wartość = zmodyfikowane_dane[wiersz][kolumna]

        # Zastosuj zmianę
        zmodyfikowane_dane[wiersz][kolumna] = wartość
        zmiany_zastosowane += 1

        print(f"Zmiana [{wiersz},{kolumna}]: '{stara_wartość}' → '{wartość}'")

    print(f"Zastosowano {zmiany_zastosowane} zmian")
    return zmodyfikowane_dane


def wyświetl_csv(dane, tytuł="Zawartość CSV"):
    """
    Wyświetla dane CSV w czytelnym formacie

    Args:
        dane: lista list reprezentująca dane CSV
        tytuł: tytuł do wyświetlenia
    """
    print(f"\n=== {tytuł} ===")

    if not dane:
        print("(pusty plik)")
        return

    # Znajdź maksymalną szerokość każdej kolumny
    max_kolumn = max(len(wiersz) for wiersz in dane) if dane else 0
    szerokości = [0] * max_kolumn

    # Rozszerz wszystkie wiersze do tej samej długości i oblicz szerokości
    dane_wyrównane = []
    for wiersz in dane:
        wiersz_wyrównany = wiersz + [''] * (max_kolumn - len(wiersz))
        dane_wyrównane.append(wiersz_wyrównany)

        for i, komórka in enumerate(wiersz_wyrównany):
            szerokości[i] = max(szerokości[i], len(str(komórka)))

    # Wyświetl nagłówek z numerami kolumn
    nagłówek = "  |  ".join(f"Kol.{i:>{szerokości[i]-3}}" for i in range(max_kolumn))
    print(f"   | {nagłówek}")
    print("-" * (len(nagłówek) + 6))

    # Wyświetl dane
    for i, wiersz in enumerate(dane_wyrównane):
        wiersz_str = "  |  ".join(f"{komórka:>{szerokości[j]}}" for j, komórka in enumerate(wiersz))
        print(f"{i:2} | {wiersz_str}")

    print()


def zapisz_csv(dane, nazwa_pliku):
    """
    Zapisuje dane do pliku CSV

    Args:
        dane: lista list reprezentująca dane CSV
        nazwa_pliku: ścieżka do pliku docelowego
    """
    try:
        with open(nazwa_pliku, 'w', encoding='utf-8', newline='') as plik:
            zapisany = csv.writer(plik)
            zapisany.writerows(dane)

        print(f"Zapisano {len(dane)} wierszy do pliku '{nazwa_pliku}'")

    except PermissionError:
        print(f"Błąd: Brak uprawnień do zapisu pliku '{nazwa_pliku}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku '{nazwa_pliku}': {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Główna funkcja programu"""
    # Sprawdź argumenty wiersza poleceń
    if len(sys.argv) < 3:
        print("Błąd: Za mało argumentów", file=sys.stderr)
        print("Wymagane: przynajmniej plik_wejściowy i plik_wyjściowy")
        print()
        wyświetl_pomoc()
        sys.exit(1)

    if sys.argv[1] in ['-h', '--help']:
        wyświetl_pomoc()
        sys.exit(0)

    # Parsuj argumenty
    plik_wejściowy = sys.argv[1]
    plik_wyjściowy = sys.argv[2]
    argumenty_zmian = sys.argv[3:]

    print(f"Program CSV Reader and Modifier")
    print(f"Plik wejściowy: {plik_wejściowy}")
    print(f"Plik wyjściowy: {plik_wyjściowy}")
    print(f"Liczba zmian: {len(argumenty_zmian)}")
    print("-" * 50)

    # Wczytaj plik CSV
    dane_oryginalne = wczytaj_csv(plik_wejściowy)

    # Wyświetl oryginalne dane
    wyświetl_csv(dane_oryginalne, "Oryginalne dane")

    # Parsuj zmiany
    if argumenty_zmian:
        zmiany = parsuj_zmiany(argumenty_zmian)
        print(f"Zmiany do zastosowania:")
        for (kolumna, wiersz), wartość in sorted(zmiany.items()):
            print(f"  [{wiersz},{kolumna}] = '{wartość}'")
        print()

        # Zastosuj zmiany
        dane_zmodyfikowane = zastosuj_zmiany(dane_oryginalne, zmiany)
    else:
        print("Brak zmian do zastosowania")
        dane_zmodyfikowane = dane_oryginalne

    # Wyświetl zmodyfikowane dane
    wyświetl_csv(dane_zmodyfikowane, "Zmodyfikowane dane")

    # Zapisz do pliku wyjściowego
    zapisz_csv(dane_zmodyfikowane, plik_wyjściowy)

    print("Operacja zakończona pomyślnie!")


if __name__ == "__main__":
    main()
