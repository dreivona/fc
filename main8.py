import sys
import json
import csv
import pickle
import os
from abc import ABC, abstractmethod
from typing import List, Any, Dict


class FileHandler(ABC):
    """Metoda obsługi plików"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = []

    @abstractmethod
    def read(self) -> List[List[Any]]:
        """Odczytuje dane z pliku"""
        pass

    @abstractmethod
    def write(self, filepath: str, data: List[List[Any]]) -> None:
        """Zapisuje dane do pliku"""
        pass

    def get_data(self) -> List[List[Any]]:
        """Zwraca dane"""
        return self.data


class CSVHandler(FileHandler):
    """Obsługa plików CSV"""

    def read(self) -> List[List[Any]]:
        """Odczytuje dane z pliku CSV"""
        try:
            with open(self.filepath, 'r', encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                self.data = [row for row in reader]
                return self.data
        except FileNotFoundError:
            print(f"Błąd: Nie można znaleźć pliku {self.filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd: odczytu pliku CSV: {e}")
            sys.exit(1)

    def write(self, filepath: str, data: List[List[Any]]) -> None:
        """Zapisuje dane do pliku CSV"""
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        except Exception as e:
            print(f"Błąd: zapisu pliku CSV: {e}")
            sys.exit(1)


class JSONHandler(FileHandler):
    """Obsługa plików JSON"""

    def read(self) -> List[List[Any]]:
        """Odczytuje dane z pliku JSON"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                # Konwersja JSON do listy list
                if isinstance(json_data, list):
                    self.data = json_data
                elif isinstance(json_data, dict):
                    # Jeśli JSON jest bazą, konwertujemy go do listy list
                    self.data = [[key, value] for key, value in json_data.items()]
                else:
                    # Jeśli JSON to pojedyncza wartość, opakowujemy w listę
                    self.data = [[json_data]]
                return self.data
        except FileNotFoundError:
            print(f"Błąd: nie można znaleźć pliku {self.filepath}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Błąd: podczas dekodowania JSON: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd: podczas odczytu pliku JSON: {e}")
            sys.exit(1)

    def write(self, filepath: str, data: List[List[Any]]) -> None:
        """Zapisuje dane do pliku JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Błąd: podczas zapisu pliku JSON: {e}")
            sys.exit(1)


class TXTHandler(FileHandler):
    """Obsługa plików TXT"""

    def read(self) -> List[List[Any]]:
        """Odczytuje dane z pliku TXT"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # Każda linia to osobny wiersz, podzielona przez tabulatory lub spacje
                self.data = []
                for line in lines:
                    line = line.strip()
                    if line:
                        # Dzielimy przez tabulatory, jeśli nie ma - przez spacje
                        if '\t' in line:
                            row = line.split('\t')
                        else:
                            row = line.split()
                        self.data.append(row)
                return self.data
        except FileNotFoundError:
            print(f"Błąd: nie można znaleźć pliku {self.filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd: podczas odczytu pliku TXT: {e}")
            sys.exit(1)

    def write(self, filepath: str, data: List[List[Any]]) -> None:
        """Zapisuje dane do pliku TXT"""
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                for row in data:
                    line = '\t'.join(str(item) for item in row)
                    file.write(line + '\n')
        except Exception as e:
            print(f"Błąd: podczas zapisu pliku TXT: {e}")
            sys.exit(1)


class PickleHandler(FileHandler):
    """Obsługa plików Pickle"""

    def read(self) -> List[List[Any]]:
        """Odczytuje dane z pliku Pickle"""
        try:
            with open(self.filepath, 'rb') as file:
                pickle_data = pickle.load(file)
                # Konwersja do listy list
                if isinstance(pickle_data, list):
                    self.data = pickle_data
                else:
                    self.data = [[pickle_data]]
                return self.data
        except FileNotFoundError:
            print(f"Błąd: Nie można znaleźć pliku {self.filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd: podczas odczytu pliku Pickle: {e}")
            sys.exit(1)

    def write(self, filepath: str, data: List[List[Any]]) -> None:
        """Zapisuje dane do pliku Pickle"""
        try:
            with open(filepath, 'wb') as file:
                pickle.dump(data, file)
        except Exception as e:
            print(f"Błąd: podczas zapisu pliku Pickle: {e}")
            sys.exit(1)


class FileProcessor:
    """Główna klasa do przetwarzania plików"""

    def __init__(self):
        self.handler_map = {
            '.csv': CSVHandler,
            '.json': JSONHandler,
            '.txt': TXTHandler,
            '.pickle': PickleHandler
        }

    def get_file_extension(self, filepath: str) -> str:
        """Pobiera rozszerzenie pliku"""
        return os.path.splitext(filepath)[1].lower()

    def create_handler(self, filepath: str) -> FileHandler:
        """Tworzy odpowiedni handler na podstawie rozszerzenia pliku"""
        extension = self.get_file_extension(filepath)
        if extension not in self.handler_map:
            print(f"Błąd: Nieobsługiwane rozszerzenie pliku: {extension}")
            print(f"Obsługiwane formaty: {', '.join(self.handler_map.keys())}")
            sys.exit(1)

        return self.handler_map[extension](filepath)

    def apply_changes(self, data: List[List[Any]], changes: List[str]) -> List[List[Any]]:
        """Aplikuje zmiany do danych"""
        # Tworzymy kopię danych
        modified_data = [row[:] for row in data]

        for change in changes:
            try:
                parts = change.split(',', 2)  # Dzielimy maksymalnie na 3 części
                if len(parts) != 3:
                    print(f"Błąd: nieprawidłowy format zmiany '{change}'. Oczekiwany format: x,y,wartość")
                    sys.exit(1)

                col = int(parts[0])
                row = int(parts[1])
                value = parts[2]

                # Rozszerzamy dane jeśli potrzeba
                while len(modified_data) <= row:
                    modified_data.append([])

                while len(modified_data[row]) <= col:
                    modified_data[row].append('')

                # Aplikujemy zmianę
                modified_data[row][col] = value

            except ValueError as e:
                print(f"Błąd: nieprawidłowe współrzędne w zmianie '{change}': {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Błąd: podczas aplikowania zmiany '{change}': {e}")
                sys.exit(1)

        return modified_data

    def display_data(self, data: List[List[Any]]) -> None:
        """Wyświetla dane w terminalu"""
        print("\nZawartość pliku po modyfikacji:")
        print("-" * 40)
        for i, row in enumerate(data):
            row_str = ','.join(str(item) for item in row)
            print(f"{row_str}")
        print("-" * 40)

    def process(self, input_file: str, output_file: str, changes: List[str]) -> None:
        """Główna metoda przetwarzania"""
        # Odczyt pliku wejściowego
        input_handler = self.create_handler(input_file)
        data = input_handler.read()

        print(f"Odczytano plik: {input_file}")
        print(f"Liczba wierszy: {len(data)}")

        # Aplikowanie zmian
        if changes:
            modified_data = self.apply_changes(data, changes)
            print(f"Zastosowano {len(changes)} zmian(y)")
        else:
            modified_data = data
            print("Brak zmian do zastosowania.")

        # Wyświetlenie danych
        self.display_data(modified_data)

        # Zapis do pliku wyjściowego
        output_handler = self.create_handler(output_file)
        output_handler.write(output_file, modified_data)

        print(f"\nDane zostały zapisane do pliku: {output_file}")


def main():
    """Funkcja główna"""
    if len(sys.argv) < 3:
        print("Użycie: python reader.py <plik_wejściowy> <plik_wyjściowy> [zmiana_1] [zmiana_2] ... [zmiana_n]")
        print("Zmiana w formacie: x,y,wartość")
        print("Przykład: python reader.py in.json out.csv 0,0,gitara 3,1,kubek")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:] if len(sys.argv) > 3 else []

    processor = FileProcessor()
    processor.process(input_file, output_file, changes)


if __name__ == "__main__":
    main()
