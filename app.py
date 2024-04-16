from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        con = sqlite3.connect("players.db")
        cur = con.cursor()
        if cur.execute("SELECT name FROM current_players WHERE name = ?", (name, )).fetchone():
            return render_template("error.html")

        cur.execute("INSERT INTO current_players (name) VALUES (?)", (name, ))
        con.commit()
        con.close()
        return redirect("/")

    con = sqlite3.connect("players.db")
    cur = con.cursor()
    players = cur.execute("SELECT name FROM players").fetchall()
    current_players = cur.execute("SELECT name FROM current_players").fetchall()
    con.close()
    return render_template("index.html", players=players, current_players=current_players)


@app.route("/clean_up", methods = ["POST"])
def clean_up():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    cur.execute("DELETE FROM current_players")
    con.commit()
    con.close()
    return redirect("/admin")

@app.route("/admin")
def admin():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM players")
    current_players = cur.execute("SELECT name FROM current_players").fetchall()
    players = cur.execute("SELECT name, value FROM players").fetchall()
    con.close()
    return render_template("admin.html", current_players=current_players, players= players)

@app.route("/add_new_player", methods = ["POST"])
def add_new_player():
    new_player = request.form.get("new_player")
    value = float(request.form.get("value"))
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    cur.execute("INSERT INTO players (name, value) VALUES (?, ?)", (new_player, value))
    con.commit()
    con.close()
    return redirect("/admin")

@app.route("/edit_value", methods = ["POST"])
def edit_value():
    player = request.form.get("player")
    new_value = float(request.form.get("new_value"))
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    cur.execute("UPDATE players SET value = ? WHERE name = ?", (new_value, player))
    con.commit()
    con.close()
    return redirect("/admin")

    
