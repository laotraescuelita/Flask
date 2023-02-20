from flask import Flask, render_template , url_for
from app_main import app 


@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/super_elipse")
def super_elipse():
    return render_template("super_elipse.html", titulo="Super Elipse")

@app.route("/super_figuras")
def super_figuras():
    return render_template("super_figuras.html", titulo = "Super Figuras")

@app.route("/julia_set")
def julia_set():
    return render_template("julia_set.html", titulo="Julia Set Fractal")
