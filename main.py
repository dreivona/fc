from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

SALDO_FILE = "saldo.txt"
MAGAZYN_FILE = "magazyn.txt"
HISTORIA_FILE = "historia.txt"


def wczytaj_saldo():
    if os.path.exists(SALDO_FILE):
        with open(SALDO_FILE) as f:
            return float(f.read())
    return 0.0


def zapisz_saldo(saldo):
    with open(SALDO_FILE, "w") as f:
        f.write(str(saldo))


def wczytaj_magazyn():
    magazyn = {}
    if os.path.exists(MAGAZYN_FILE):
        with open(MAGAZYN_FILE) as f:
            for line in f:
                nazwa, ilosc = line.strip().split(",")
                magazyn[nazwa] = int(ilosc)
    return magazyn


def zapisz_magazyn(magazyn):
    with open(MAGAZYN_FILE, "w") as f:
        for nazwa, ilosc in magazyn.items():
            f.write(f"{nazwa},{ilosc}\n")


def zapisz_historie(opis):
    with open(HISTORIA_FILE, "a", encoding="utf-8") as f:
        f.write(opis + "\n")


@app.route("/", methods=["GET", "POST"])
def index():
    saldo = wczytaj_saldo()
    magazyn = wczytaj_magazyn()

    if request.method == "POST":
        if "zakup" in request.form:
            nazwa = request.form["nazwa"]
            cena = float(request.form["cena"])
            ilosc = int(request.form["ilosc"])
            koszt = cena * ilosc

            if saldo >= koszt:
                saldo -= koszt
                magazyn[nazwa] = magazyn.get(nazwa, 0) + ilosc
                zapisz_historie(f"Zakup: {nazwa}, cena: {cena}, ilość: {ilosc}")
            else:
                return "Za mało środków na koncie."

        elif "sprzedaz" in request.form:
            nazwa = request.form["nazwa"]
            ilosc = int(request.form["ilosc"])

            if magazyn.get(nazwa, 0) >= ilosc:
                magazyn[nazwa] -= ilosc
                cena = float(request.form.get("cena", 0))  # fallback cena
                saldo += cena * ilosc
                zapisz_historie(f"Sprzedaż: {nazwa}, ilość: {ilosc}, cena: {cena}")
            else:
                return "Za mało produktów w magazynie."

        elif "saldo" in request.form:
            wartosc = float(request.form["wartosc"])
            saldo += wartosc
            zapisz_historie(f"Zmiana salda: {wartosc}")

        zapisz_saldo(saldo)
        zapisz_magazyn(magazyn)

        return redirect(url_for("index"))

    return render_template("index.html", saldo=saldo, magazyn=magazyn)


@app.route("/historia/")
@app.route("/historia/<int:start>/<int:koniec>/")
def historia(start=None, koniec=None):
    if not os.path.exists(HISTORIA_FILE):
        return "Brak historii"

    with open(HISTORIA_FILE, encoding="utf-8") as f:
        linie = f.readlines()

    if start is None or koniec is None:
        wycinek = linie
    elif 0 <= start < len(linie) and 0 < koniec <= len(linie) and start < koniec:
        wycinek = linie[start:koniec]
    else:
        return f"Nieprawidłowy zakres! Wybierz od 0 do {len(linie)-1}"

    return render_template("historia.html", historia=wycinek)

if __name__ == "__main__":
    app.run(debug=True)