import json
import os
import datetime
from typing import Dict, List, Tuple, Union, Any, Callable
from abc import ABC, abstractmethod


class Command(ABC):
    """Metoda poleceń (Command Pattern)"""

    @abstractmethod
    def execute(self) -> None:
        pass


class FileHandler:
    """Klasa odpowiedzialna za operacje na plikach"""

    def __init__(self):
        self.folder_dane = "dane_firmy"
        self.plik_konto = "konto.txt"
        self.plik_magazyn = "magazyn.json"
        self.plik_historia = "historia.json"

    def stworz_folder_danych(self) -> None:
        """Tworzy folder na dane jeśli taki nie istnieje"""
        if not os.path.exists(self.folder_dane):
            os.makedirs(self.folder_dane)
            print(f"Utworzono folder: {self.folder_dane}")

    def sciezka_pliku(self, nazwa_pliku: str) -> str:
        """Zwraca pełną ścieżkę do pliku w folderze danych"""
        return os.path.join(self.folder_dane, nazwa_pliku)

    def wczytaj_dane(self) -> Tuple[float, Dict, List]:
        """Wczytuje dane z plików"""
        self.stworz_folder_danych()

        konto = 0.0
        magazyn = {}
        historia = []

        # Wczytanie salda konta
        try:
            plik_konto = self.sciezka_pliku(self.plik_konto)
            if os.path.exists(plik_konto):
                with open(plik_konto, 'r', encoding='utf-8') as f:
                    konto = float(f.read().strip())
                    print(f"✅ Wczytano saldo konta: {konto:.2f} zł")
            else:
                print("ℹ️  Brak pliku konta - rozpoczynanie z saldem 0 zł")
        except Exception as e:
            print(f"⚠️  Nie można wczytać salda konta: {e}")
            konto = 0.0

        # Wczytanie magazynu
        try:
            plik_magazyn = self.sciezka_pliku(self.plik_magazyn)
            if os.path.exists(plik_magazyn):
                with open(plik_magazyn, 'r', encoding='utf-8') as f:
                    magazyn = json.load(f)
                    print(f"✅ Wczytano {len(magazyn)} produktów z magazynu.")
            else:
                print("ℹ️  Brak pliku magazynu - rozpoczynanie z pustym magazynem.")
        except Exception as e:
            print(f"⚠️  Nie można wczytać magazynu: {e}")
            magazyn = {}

        # Wczytanie historii
        try:
            plik_historia = self.sciezka_pliku(self.plik_historia)
            if os.path.exists(plik_historia):
                with open(plik_historia, 'r', encoding='utf-8') as f:
                    historia = json.load(f)
                    print(f"✅ Wczytano {len(historia)} operacji z historii.")
            else:
                print("ℹ️  Brak pliku historii - rozpoczynanie z pustą historią.")
        except Exception as e:
            print(f"⚠️  Nie można wczytać historii: {e}.")
            historia = []

        return konto, magazyn, historia

    def zapisz_dane(self, konto: float, magazyn: Dict, historia: List) -> bool:
        """Zapisuje wszystkie dane do plików"""
        try:
            self.stworz_folder_danych()

            # Zapisanie salda konta
            with open(self.sciezka_pliku(self.plik_konto), 'w', encoding='utf-8') as f:
                f.write(f"{konto:.2f}")

            # Zapisanie magazynu
            with open(self.sciezka_pliku(self.plik_magazyn), 'w', encoding='utf-8') as f:
                json.dump(magazyn, f, ensure_ascii=False, indent=2)

            # Zapisanie historii
            with open(self.sciezka_pliku(self.plik_historia), 'w', encoding='utf-8') as f:
                json.dump(historia, f, ensure_ascii=False, indent=2)

            print("✅ Dane zostały zapisane do plików.")
            return True

        except Exception as e:
            print(f"❌ Błąd podczas zapisywania danych: {e}.")
            return False


class SaldoCommand(Command):
    """Komenda dla operacji na saldzie"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        try:
            kwota = float(input("Podaj kwotę do dodania (albo ujemną do odjęcia): "))
            stare_saldo = self.manager.konto
            self.manager.konto += kwota

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.manager.historia.append((timestamp, "saldo", kwota, stare_saldo, self.manager.konto))

            if kwota > 0:
                print(f"✅ Dodano {kwota:.2f} zł do konta.")
            else:
                print(f"✅ Odjęto {abs(kwota):.2f} zł z konta.")
            print(f"Nowe saldo: {self.manager.konto:.2f} zł.")

        except ValueError:
            print("❌ Błąd: Podano nieprawidłową kwotę.")


class SprzedazCommand(Command):
    """Komenda dla operacji sprzedaży"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        produkt = input("Podaj nazwę produktu: ").strip()
        if not produkt:
            print("❌ Błąd: Nazwa produktu nie może być pusta.")
            return

        if produkt not in self.manager.magazyn:
            print(f"❌ Błąd: Produkt '{produkt}' nie istnieje w magazynie.")
            return

        try:
            cena = float(input("Podaj cenę za sztukę: "))
            ilosc = int(input("Podaj liczbę sztuk: "))

            if cena <= 0 or ilosc <= 0:
                print("❌ Błąd: Cena i ilość muszą być dodatnie.")
                return

            if self.manager.magazyn[produkt]["ilość"] < ilosc:
                print(f"❌ Błąd: Brak wystarczającej liczby produktów w magazynie.")
                print(f"Dostępne: {self.manager.magazyn[produkt]['ilość']} szt.")
                return

            # Wykonaj sprzedaż
            self.manager.magazyn[produkt]["ilość"] -= ilosc
            zysk = cena * ilosc
            self.manager.konto += zysk

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.manager.historia.append((timestamp, "sprzedaż", produkt, cena, ilosc, zysk))

            print(f"✅ Sprzedano {ilosc} szt. produktu '{produkt}.'")
            print(f"Zysk: {zysk:.2f} zł.")
            print(f"Nowe saldo: {self.manager.konto:.2f} zł.")

            # Usuń produkt z magazynu jeśli ilość = 0
            if self.manager.magazyn[produkt]["ilość"] == 0:
                del self.manager.magazyn[produkt]
                print(f"ℹ️  Produkt '{produkt}' usunięty z magazynu (brak sztuk).")

        except ValueError:
            print("❌ Błąd: Nieprawidłowa cena lub ilość.")


class ZakupCommand(Command):
    """Komenda dla operacji zakupu"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        produkt = input("Podaj nazwę produktu: ").strip()
        if not produkt:
            print("❌ Błąd: Nazwa produktu nie może być pusta.")
            return

        try:
            cena = float(input("Podaj cenę za sztukę: "))
            ilosc = int(input("Podaj liczbę sztuk: "))
            koszt = cena * ilosc

            if cena <= 0 or ilosc <= 0:
                print("❌ Błąd: Cena i ilość muszą być dodatnie.")
                return

            if self.manager.konto < koszt:
                print(f"❌ Błąd: Niewystarczające środki na koncie.")
                print(f"Potrzebne: {koszt:.2f} zł, Dostępne: {self.manager.konto:.2f} zł")
                return

            # Wykonaj zakup
            self.manager.konto -= koszt
            if produkt in self.manager.magazyn:
                self.manager.magazyn[produkt]["ilość"] += ilosc
                self.manager.magazyn[produkt]["cena"] = cena
            else:
                self.manager.magazyn[produkt] = {"cena": cena, "ilość": ilosc}

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.manager.historia.append((timestamp, "zakup", produkt, cena, ilosc, koszt))

            print(f"✅ Zakupiono {ilosc} szt. produktu '{produkt}'")
            print(f"Koszt: {koszt:.2f} zł")
            print(f"Nowe saldo: {self.manager.konto:.2f} zł")

        except ValueError:
            print("❌ Błąd: Nieprawidłowa cena lub ilość.")


class KontoCommand(Command):
    """Komenda dla wyświetlania stanu konta"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        print(f"\n💰 Aktualny stan konta: {self.manager.konto:.2f} zł.")

        # Oblicz wartość magazynu
        wartosc_magazynu = sum(
            dane["cena"] * dane["ilość"]
            for dane in self.manager.magazyn.values()
        )
        print(f"📦 Wartość magazynu: {wartosc_magazynu:.2f} zł.")
        print(f"💎 Łączne aktywa: {self.manager.konto + wartosc_magazynu:.2f} zł.")


class ListaCommand(Command):
    """Komenda dla wyświetlania listy produktów"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        if not self.manager.magazyn:
            print("📦 Magazyn jest pusty.")
            return

        print(f"\n📦 STAN MAGAZYNU ({len(self.manager.magazyn)} produktów):")
        print("-" * 60)
        print(f"{'Produkt':<20} {'Ilość':<10} {'Cena':<10} {'Wartość':<15}")
        print("-" * 60)

        laczna_wartosc = 0
        for produkt, dane in sorted(self.manager.magazyn.items()):
            wartosc = dane["cena"] * dane["ilość"]
            laczna_wartosc += wartosc
            print(f"{produkt:<20} {dane['ilość']:<10} {dane['cena']:<10.2f} {wartosc:<15.2f}")

        print("-" * 60)
        print(f"{'ŁĄCZNIE':<20} {'':<10} {'':<10} {laczna_wartosc:<15.2f}")


class MagazynCommand(Command):
    """Komenda dla sprawdzania konkretnego produktu"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        nazwa = input("Podaj nazwę produktu: ").strip()
        if not nazwa:
            print("❌ Błąd: Nazwa produktu nie może być pusta.")
            return

        if nazwa in self.manager.magazyn:
            dane = self.manager.magazyn[nazwa]
            wartosc = dane["cena"] * dane["ilość"]
            print(f"\n📦 {nazwa}:")
            print(f"   Ilość: {dane['ilość']} szt.")
            print(f"   Cena: {dane['cena']:.2f} zł/szt.")
            print(f"   Wartość: {wartosc:.2f} zł")
        else:
            print(f"❌ Błąd: Produkt '{nazwa}' nie został znaleziony w magazynie.")


class PrzegladCommand(Command):
    """Komenda dla przeglądania historii"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        if not self.manager.historia:
            print("📝 Historia operacji jest pusta.")
            return

        try:
            print(f"Dostępne operacje: 0 - {len(self.manager.historia) - 1}")
            od_str = input("Od którego wpisu (ENTER = od początku): ").strip()
            do_str = input("Do którego wpisu (ENTER = do końca): ").strip()

            od = int(od_str) if od_str else 0
            do = int(do_str) if do_str else len(self.manager.historia)

            if od < 0 or do > len(self.manager.historia) or od >= do:
                print(f"❌ Nieprawidłowy zakres. Liczba operacji: {len(self.manager.historia)}")
                return

            print(f"\n📝 HISTORIA OPERACJI ({od} - {do - 1}):")
            print("=" * 80)

            for i, wpis in enumerate(self.manager.historia[od:do], start=od):
                if len(wpis) >= 2:
                    timestamp = wpis[0]
                    operacja = wpis[1]
                    szczegoly = wpis[2:]
                    print(f"{i:3d}. [{timestamp}] {operacja.upper()}: {szczegoly}")
                else:
                    print(f"{i:3d}. {wpis}")

        except ValueError:
            print("❌ Błąd: Wpisy muszą być liczbami całkowitymi.")


class ZapiszCommand(Command):
    """Komenda dla zapisywania danych"""

    def __init__(self, manager):
        self.manager = manager

    def execute(self) -> None:
        self.manager.file_handler.zapisz_dane(
            self.manager.konto,
            self.manager.magazyn,
            self.manager.historia
        )


class Manager:
    """Główna klasa zarządzająca systemem firmy"""

    def __init__(self):
        # Inicjalizacja handlera plików
        self.file_handler = FileHandler()

        # Inicjalizacja danych
        self.konto, self.magazyn, self.historia = self.file_handler.wczytaj_dane()

        # Słownik komend - implementacja wzorca Command Pattern
        self.commands: Dict[str, Command] = {}

        # Słownik funkcji pomocniczych
        self.functions: Dict[str, Callable] = {}

        # Inicjalizacja komend
        self._initialize_commands()
        self._initialize_functions()

    def _initialize_commands(self) -> None:
        """Inicjalizuje wszystkie dostępne komendy"""
        self.commands = {
            "saldo": SaldoCommand(self),
            "sprzedaż": SprzedazCommand(self),
            "zakup": ZakupCommand(self),
            "konto": KontoCommand(self),
            "lista": ListaCommand(self),
            "magazyn": MagazynCommand(self),
            "przegląd": PrzegladCommand(self),
            "zapisz": ZapiszCommand(self)
        }

    def _initialize_functions(self) -> None:
        """Inicjalizuje funkcje pomocnicze"""
        self.functions = {
            "pokaz_polecenia": self._pokaz_polecenia,
            "stats": self._pokaz_statystyki,
            "backup": self._stworz_kopie_zapasowa
        }

    def execute(self, command_name: str) -> bool:
        """
        Metoda execute - wykonuje komendę zgodnie z wzorcem Command Pattern

        Args:
            command_name: nazwa komendy do wykonania

        Returns:
            bool: True jeśli komenda została wykonana, False w przeciwnym przypadku
        """
        if command_name in self.commands:
            try:
                self.commands[command_name].execute()
                return True
            except Exception as e:
                print(f"❌ Błąd: podczas wykonywania komendy '{command_name}': {e}")
                return False
        else:
            print(f"❌ Błąd: Nieznana komenda '{command_name}'")
            return False

    def assign(self, function_name: str, *args, **kwargs) -> Any:
        """
        Metoda assign - przypisuje i wykonuje funkcję pomocniczą

        Args:
            function_name: nazwa funkcji do wykonania
            *args: argumenty pozycyjne
            **kwargs: argumenty nazwane

        Returns:
            Any: wynik funkcji lub None jeśli funkcja nie istnieje
        """
        if function_name in self.functions:
            try:
                return self.functions[function_name](*args, **kwargs)
            except Exception as e:
                print(f"❌ Błąd podczas wykonywania funkcji '{function_name}': {e}")
                return None
        else:
            print(f"❌ Błąd: Nieznana funkcja '{function_name}'")
            return None

    def _pokaz_polecenia(self) -> None:
        """Wyświetla dostępne polecenia"""
        print("\n" + "=" * 60)
        print("🏢 SYSTEM ZARZĄDZANIA FIRMĄ")
        print("=" * 60)
        print("📋 DOSTĘPNE POLECENIA:")
        print("-" * 60)
        print("saldo    - zarządzanie stanem konta")
        print("sprzedaż - sprzedaż produktów z magazynu")
        print("zakup    - zakup produktów do magazynu")
        print("konto    - wyświetl aktualny stan konta")
        print("lista    - wyświetl wszystkie produkty w magazynie")
        print("magazyn  - sprawdź konkretny produkt")
        print("przegląd - przeglądaj historię operacji")
        print("zapisz   - zapisz dane do plików")
        print("stats    - pokaż statystyki firmy")
        print("backup   - utwórz kopię zapasową")
        print("koniec   - zakończ program i zapisz dane")
        print("=" * 60)

    def _pokaz_statystyki(self) -> None:
        """Wyświetla statystyki firmy"""
        print("\n📊 STATYSTYKI FIRMY")
        print("=" * 50)

        # Podstawowe informacje
        print(f"💰 Saldo konta: {self.konto:.2f} zł.")
        print(f"📦 Produkty w magazynie: {len(self.magazyn)}.")
        print(f"📝 Operacje w historii: {len(self.historia)}.")

        # Wartość magazynu
        wartosc_magazynu = sum(dane["cena"] * dane["ilość"] for dane in self.magazyn.values())
        print(f"💎 Wartość magazynu: {wartosc_magazynu:.2f} zł.")
        print(f"🏆 Łączne aktywa: {self.konto + wartosc_magazynu:.2f} zł.")

        # Analiza historii
        if self.historia:
            operacje = {}
            laczny_zysk = 0
            laczny_koszt = 0

            for wpis in self.historia:
                if len(wpis) >= 2:
                    operacja = wpis[1]
                    operacje[operacja] = operacje.get(operacja, 0) + 1

                    if operacja == "sprzedaż" and len(wpis) >= 6:
                        laczny_zysk += wpis[5]  # zysk
                    elif operacja == "zakup" and len(wpis) >= 6:
                        laczny_koszt += wpis[5]  # koszt

            print(f"\n📈 Analiza operacji:")
            for op, liczba in operacje.items():
                print(f"  - {op}: {liczba}")

            print(f"\n💹 Analiza finansowa:")
            print(f"  - Łączny zysk ze sprzedaży: {laczny_zysk:.2f} zł.")
            print(f"  - Łączny koszt zakupów: {laczny_koszt:.2f} zł.")
            print(f"  - Zysk netto: {laczny_zysk - laczny_koszt:.2f} zł.")

    def _stworz_kopie_zapasowa(self) -> None:
        """Tworzy kopię zapasową danych"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_backup = os.path.join(self.file_handler.folder_dane, "backup")

            if not os.path.exists(folder_backup):
                os.makedirs(folder_backup)

            # Kopia wszystkich danych w jednym pliku JSON
            backup_data = {
                "konto": self.konto,
                "magazyn": self.magazyn,
                "historia": self.historia,
                "timestamp": timestamp
            }

            backup_file = os.path.join(folder_backup, f"backup_{timestamp}.json")
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)

            print(f"✅ Utworzono kopię zapasową: backup_{timestamp}.json")

        except Exception as e:
            print(f"⚠️  Nie udało się utworzyć kopii zapasowej: {e}")

    def run(self) -> None:
        """Główna pętla programu"""
        print("🏢 APLIKACJA DO ZARZĄDZANIA FIRMĄ")
        print("Witaj w najlepszej aplikacji do zarządzania firmą!")

        while True:
            # Użycie metody assign do wyświetlenia poleceń
            self.assign("pokaz_polecenia")

            polecenie = input("\n➤ Podaj polecenie: ").strip().lower()

            if polecenie == "koniec":
                print("💾 Zapisywanie danych przed zakończeniem, proszę czekać...")
                if self.execute("zapisz"):
                    print("👋 Zakończono działanie programu. Do widzenia!")
                break
            elif polecenie == "stats":
                self.assign("stats")
            elif polecenie == "backup":
                self.assign("backup")
            else:
                # Użycie metody execute do wykonania komendy
                if not self.execute(polecenie):
                    print("❓ Spróbuj ponownie lub wpisz 'koniec' aby zakończyć.")

            input("\nNaciśnij ENTER, aby kontynuować...")


def main():
    """Funkcja główna"""
    try:
        manager = Manager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Program przerwany przez użytkownika.")
    except Exception as e:
        print(f"\n❌ Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    main()