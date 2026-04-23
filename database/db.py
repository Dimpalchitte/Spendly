import sqlite3

from flask import g
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        );
    """)
    db.commit()
    db.close()


def seed_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")

    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        db.close()
        return

    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    db.commit()

    user_id = db.execute("SELECT id FROM users WHERE email = 'demo@spendly.com'").fetchone()[0]

    expenses = [
        (user_id, 320.00,  "Food",          "2026-04-01", "Breakfast at Cafe"),
        (user_id, 150.00,  "Transport",     "2026-04-05", "Ola cab to office"),
        (user_id, 1200.00, "Bills",         "2026-04-08", "Electricity bill"),
        (user_id, 500.00,  "Health",        "2026-04-12", "Pharmacy purchase"),
        (user_id, 800.00,  "Entertainment", "2026-04-15", "Movie tickets"),
        (user_id, 2500.00, "Shopping",      "2026-04-18", "Clothes from Myntra"),
        (user_id, 200.00,  "Other",         "2026-04-20", "Stationery items"),
        (user_id, 450.00,  "Food",          "2026-04-22", "Dinner with friends"),
    ]
    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    db.commit()
    db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
