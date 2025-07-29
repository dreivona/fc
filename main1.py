print("Ile jednostek być wysłanych?")
liczba_jednostek = int(input())

paczki = []
aktualna_paczka = 0
suma_kg = 0

for i in range(liczba_jednostek):
    print(f"Podaj wagę jednostki {i+1}:")
    waga = int(input())

    if waga < 1 or waga > 10:
        print("Waga jednostki poza zakresem (1-10kg). Pakowanie przerwane.")
        if aktualna_paczka > 0:
            paczki.append(aktualna_paczka)
        break

    if aktualna_paczka + waga > 20:
        paczki.append(aktualna_paczka)
        aktualna_paczka = waga
    else:
        aktualna_paczka += waga

    suma_kg += waga

# Zostanie dodana ostatnia paczka jeśli coś pozostało
if aktualna_paczka > 0:
    paczki.append(aktualna_paczka)

#Obliczenie pustego miejsca w każdej paczce
puste_kilogramy = [(20 - waga) for waga in paczki]
suma_pustych = sum(puste_kilogramy)
najwięcej_pustych = max(puste_kilogramy)
nr_paczki_najwięcej_pustych = puste_kilogramy.index(najwięcej_pustych) + 1

#Rezultat
print("\n--- Podsumowanie ---")
print(f"Wysłano {len(paczki)} paczek.")
print(f"Wysłano {suma_kg} kg.")
print(f"Suma pustych kilogramów: {suma_pustych} kg.")
print(f"Najwięcej pustych kilogramów ma paczka {nr_paczki_najwięcej_pustych} ({najwięcej_pustych} kg.)")