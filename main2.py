konto = 0
magazyn = {}
historia = []

def pokaz_polecenia():
    print("\n Dostępne polecenia:")
    print("saldo - sprzedaż - zakup - konto - lista - magazyn - przegląd - koniec")

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
        produkt = input("Podaj nazwę produku: ").strip()
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

            if od < 0  or do > len(historia) or od >= do:
                print(f"Nieprawidłowy zakres. Liczba zapisanych operacji: {len(historia)}.")
            else:
                for i, wpis in enumerate(historia[od:do], start=od):
                    print(f"{i}: {wpis}")
        except ValueError:
            print("Błąd: Liczby muszą być całkowite bądź zakresy puste.")

    elif polecenie == "koniec":
        print("Zakończono działanie programu.")
        break

    else:
        print("Błąd: Nieznane polecenie.")





