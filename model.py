# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Produkt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(80), unique=True, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False, default=0)

class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wartosc = db.Column(db.Float, nullable=False, default=0.0)

class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)  # np. "zakup", "sprzedaz", "saldo"
    szczegoly = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Skrypt integracyjny (verify.py)
from models import db, Produkt, Saldo, Historia
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
db.init_app(app)

with app.app_context():
    def verify_database():
        saldo = db.session.query(Saldo).first()
        if saldo is None:
            print("Brak salda w bazie.")
            return

        produkty = Produkt.query.all()
        historia = Historia.query.all()

        print(f"Saldo: {saldo.wartosc} zł")
        print(f"Produkty w magazynie: {[ (p.nazwa, p.ilosc) for p in produkty ]}")
        print(f"Liczba operacji w historii: {len(historia)}")

    verify_database()

# requirements.txt
Flask
Flask-SQLAlchemy

# Komendy migracji (jeśli używasz Flask-Migrate)
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
