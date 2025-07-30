#Lista uczniów {"imię_nazwisko": ..., "klasa": ...}
uczniowie = []
#Lista nauczycieli {"imię_nazwisko": ..., "przedmiot": ..., "klasy": [...]}
nauczyciele = []
#Lista wychowawców {"klasa": "imię_nazwisko"}
wychowawcy = {}

def utwórz_użytkownika():
    while True:
        print("\nUtworzenie listy użytkowników: uczeń - nauczyciel - wychowawca - koniec")
        polecenie = input("Wybierz polecenie: ").strip().lower()

        if polecenie == "uczeń":
            imię_nazwisko = input("Podaj imię i nazwisko ucznia: ").strip()
            klasa = input("Podaj nazwę klasy ucznia (przykładowo 3C): ").strip().lower()
            uczniowie.append({"imię_nazwisko": imię_nazwisko, "klasa": klasa})
            print(f"Uczeń {imię_nazwisko} został dodany do klasy {klasa}.")

        elif polecenie == "nauczyciel":
            imię_nazwisko = input("Podaj imię i nazwisko nauczyciela: ").strip()
            przedmiot = input("Podaj nazwę nauczanego przedmiotu: ").strip()
            klasy = []
            print("Podaj nazwy klas, które są prowadzone przez nauczyciela (ENTER dla koniec):")
            while True:
                klasa = input().strip()
                if klasa == "":
                    break
                klasy.append(klasa.lower())
            nauczyciele.append({"imię_nazwisko": imię_nazwisko, "przedmiot": przedmiot, "klasy": klasy})
            print(f"Nauczyciel {imię_nazwisko} został dodany.")

        elif polecenie == "wychowawca":
            imię_nazwisko = input("Podaj imię i nazwisko wychowawcy: ").strip()
            klasa = input("Podaj nazwę klasy, którą prowadzi wychowawca: ").strip().lower()
            wychowawcy[klasa] = imię_nazwisko
            print(f"Wychowawca {imię_nazwisko} został dodany do klasy {klasa}.")

        elif polecenie == "koniec":
            break

        else:
            print("Błąd: nieznane polecenie.")

def zarządzaj_użytkownikami():
    while True:
        print("\nZarządzanie: uczeń - nauczyciel - wychowawca - klasa - koniec")
        polecenie = input("Wybierz polecenie: ").strip().lower()

        if polecenie == "klasa":
            klasa = input("Podaj nazwę klasy: ").strip().lower()
            print(f"\nLista uczniów klasy {klasa}: ")
            uczniowie_klasy = [u["imię_nazwisko"] for  u in uczniowie if u["klasa"] == klasa]
            if uczniowie_klasy:
                for uczeń in uczniowie_klasy:
                 print(f"- {uczeń}")
            else:
                print("Brak uczniów w danej klasie.")
            print("Wychowawca:", wychowawcy.get(klasa, "Brak przypisanego wychowawcy."))

        elif polecenie == "uczeń":
            imię_nazwisko = input("Podaj imię i nazwisko ucznia: ").strip()
            klasa_ucznia = next((u["klasa"] for u in uczniowie if u["imię_nazwisko"].lower() == imię_nazwisko.lower()), None)
            if klasa_ucznia:
                print(f"Uczeń {imię_nazwisko} klasy {klasa_ucznia} ma takie lekcje: ")
                znaleziono = False
                for nauczyciel in nauczyciele:
                    if klasa_ucznia in nauczyciel["klasy"]:
                        print(f"- {nauczyciel['przedmiot']} (prowadzi {nauczyciel['imię_nazwisko']})")
                        znaleziono = True

                if not znaleziono:
                    print("Brak przypisanych przedmiotów.")
            else:
                print("Nie ma takiego ucznia.")

        elif polecenie == "wychowawca":
            imię_nazwisko = input("Podaj imię i nazwisko wychowawcy: ").strip()
            klasy = [kl for kl, wych in wychowawcy.items() if wych.lower() == imię_nazwisko.lower()]
            if klasy:
                for klasa in klasy:
                    print(f"\nKlasa {klasa}, uczniowie: ")
                    uczniowie_klasy = [u["imię_nazwisko"] for u in uczniowie if u["klasa"] == klasa]
                    for uczeń in uczniowie_klasy:
                        print(f"- {uczeń}")
            else:
                print("Nie znaleziono klas, które by prowadził ten wychowawca.")

        elif polecenie == "koniec":
            break

        else:
            print("Nieznane polecenie.")

#Menu

while True:
    print("\nMenu: utwórz - zarządzaj - koniec")
    komenda = input("Wybierz polecenie: ").strip().lower()

    if komenda == "utwórz":
        utwórz_użytkownika()

    elif komenda == "zarządzaj":
        zarządzaj_użytkownikami()

    elif komenda == "koniec":
        print("Wyjście.")
        break

    else:
        print("Nieznane polecenie.")


