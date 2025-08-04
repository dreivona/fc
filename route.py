from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Saldo, Magazyn, Historia

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    saldo_obj = Saldo.query.first()
    if saldo_obj is None:
        saldo_obj = Saldo(wartosc=0)
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
                    flash("Brak produktu w magazynie lub niewystarczająca ilość.")

            elif akcja == "saldo":
                zmiana = float(request.form["zmiana"])
                saldo_obj.wartosc += zmiana
                db.session.add(Historia(opis=f"Zmiana salda o {zmiana} zł"))
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash(f"Błąd: {e}")

        return redirect(url_for("main.index"))

    return render_template("index.html", saldo=saldo_obj.wartosc, magazyn=magazyn)


@bp.route("/historia/")
@bp.route("/historia/<int:start>/<int:end>/")
def historia(start=None, end=None):
    wszystkie = Historia.query.order_by(Historia.id).all()
    if start is not None and end is not None:
        if 0 <= start < end <= len(wszystkie):
            wycinek = wszystkie[start:end]
        else:
            return f"Nieprawidłowy zakres. Dostępne: 0 - {len(wszystkie)}"
    else:
        wycinek = wszystkie

    return render_template("historia.html", historia=wycinek)