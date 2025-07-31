from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
HISTORIA_FILE = "historia.txt"

# Strona główna
@app.route("/", methods=["GET", "POST"])
def index():
    saldo = 1000
    magazyn = {}

    # Obsługa formularzy (przykład — możesz rozbudować)
    if request.method == "POST":
        operacja = request.form.get("operacja")

        if operacja == "zakup":
            produkt = request.form["produkt"]
            cena = float(request.form["cena"])
            liczba = int(request.form["liczba"])
            koszt = cena * liczba
            saldo -= koszt
            magazyn[produkt] = magazyn.get(produkt, 0) + liczba
            with open(HISTORIA_FILE, "a", encoding="utf-8") as f:
                f.write(f"Zakup: {produkt}, {liczba} szt. po {cena} zł\n")

        elif operacja == "sprzedaz":
            produkt = request.form["produkt"]
            cena = float(request.form["cena"])
            liczba = int(request.form["liczba"])
            przychod = cena * liczba
            saldo += przychod
            magazyn[produkt] = magazyn.get(produkt, 0) - liczba
            with open(HISTORIA_FILE, "a", encoding="utf-8") as f:
                f.write(f"Sprzedaż: {produkt}, {liczba} szt. po {cena} zł\n")

        elif operacja == "saldo":
            komentarz = request.form["komentarz"]
            wartosc = float(request.form["wartosc"])
            saldo += wartosc
            with open(HISTORIA_FILE, "a", encoding="utf-8") as f:
                f.write(f"Zmiana salda: {komentarz}, {wartosc} zł\n")

        return redirect(url_for("index"))

    return render_template("index.html", saldo=saldo, magazyn={})

# Podstrona historii
@app.route("/historia/")
@app.route("/historia/<int:linia_od>/<int:linia_do>/")
def historia_view(linia_od=0, linia_do=None):
    if not os.path.exists(HISTORIA_FILE):
        return render_template("historia.html", wynik=["Brak historii operacji."])

    with open(HISTORIA_FILE, "r", encoding="utf-8") as f:
        wszystkie = f.readlines()

    if linia_do is None:
        wynik = wszystkie[linia_od:]
    else:
        wynik = wszystkie[linia_od:linia_do]

    return render_template("historia.html", wynik=wynik)

if __name__ == "__main__":
    app.run(debug=True)