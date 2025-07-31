from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tajny_klucz'

# Inicjalizacja bazy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MODELE
class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wartosc = db.Column(db.Float, default=0.0)

class Magazyn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), unique=True, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)

class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opis = db.Column(db.Text, nullable=False)

# STRONY
@app.route("/", methods=["GET", "POST"])
def index():
    saldo_obj = Saldo.query.first()
    if not saldo_obj:
        saldo_obj = Saldo(wartosc=0.0)
        db.session.add(saldo_obj)
        db.session.commit()

    magazyn = Magazyn.query.all()

    if request.method == "POST":
        akcja = request.form.get("akcja")

        try:
            if akcja == "zakup":
                nazwa = request.form["nazwa"]
                cena = float(request.form["cena"])
                ilosc = int(request.form["ilosc"])
                koszt = cena * ilosc

                if saldo_obj.wartosc >= koszt:
                    saldo_obj.wartosc -= koszt
                    produkt = Magazyn.query.filter_by(nazwa=nazwa).first()
                    if produkt:
                        produkt.ilosc += ilosc
                    else:
                        db.session.add(Magazyn(nazwa=nazwa, ilosc=ilosc))
                    db.session.add(Historia(opis=f"Zakup {ilosc} x {nazwa} po {cena} zł"))
                    db.session.commit()
                else:
                    flash("Za mało środków na koncie.")

            elif akcja == "sprzedaz":
                nazwa = request.form["nazwa"]
                ilosc = int(request.form["ilosc"])
                cena = float(request.form["cena"])
                produkt = Magazyn.query.filter_by(nazwa=nazwa).first()

                if produkt and produkt.ilosc >= ilosc:
                    produkt.ilosc -= ilosc
                    saldo_obj.wartosc += cena * ilosc
                    db.session.add(Historia(opis=f"Sprzedaż {ilosc} x {nazwa} po {cena} zł"))
                    db.session.commit()
                else:
                    flash("Brak produktu w magazynie lub za mało sztuk.")

            elif akcja == "saldo":
                zmiana = float(request.form["zmiana"])
                saldo_obj.wartosc += zmiana
                db.session.add(Historia(opis=f"Zmiana salda o {zmiana} zł"))
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash(f"Błąd: {e}")

        return redirect(url_for("index"))

    return render_template("index.html", saldo=saldo_obj.wartosc, magazyn=magazyn)

@app.route("/historia/")
@app.route("/historia/<int:start>/<int:end>/")
def historia(start=None, end=None):
    wpisy = Historia.query.order_by(Historia.id).all()
    if start is not None and end is not None:
        if 0 <= start < end <= len(wpisy):
            wpisy = wpisy[start:end]
        else:
            flash("Nieprawidłowy zakres historii.")
            wpisy = []
    return render_template("historia.html", historia=wpisy)

if __name__ == "__main__":
    app.run(debug=True)
