from distutils.log import debug
from flask import Flask, render_template, url_for

app = Flask("__name__")

@app.route("/")
@app.route("/mru")
def mru():
    return render_template( "mru.html" )

@app.route("/mrua")
def mrua():
    return render_template( "mrua.html" )

@app.route("/fuerzas")
def fuerzas():
    return render_template("fuerzas.html")

@app.route("/fourier")
def fourier():
    return render_template("fourier.html")


@app.route("/satelite")
def satelite():
    return render_template("satelite.html")

if __name__ == "__main__":
    app.run( debug = True )