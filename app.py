
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = "cnaps.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dossiers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                lien TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    with sqlite3.connect(DB_NAME) as conn:
        dossiers = conn.execute("SELECT * FROM dossiers").fetchall()
    return render_template("index.html", dossiers=dossiers)

@app.route("/add", methods=["POST"])
def add():
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    lien = request.form["lien"]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO dossiers (nom, prenom, lien) VALUES (?, ?, ?)", (nom, prenom, lien))
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM dossiers WHERE id = ?", (id,))
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")
