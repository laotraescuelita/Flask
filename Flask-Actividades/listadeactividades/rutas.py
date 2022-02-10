from flask import Flask, render_template, request, redirect, url_for
from listadeactividades import app,db
from listadeactividades.modelos import MiListaDeActividades

@app.route("/")
def inicio():
	#return "Hola mundo!"
	listadeactividades = MiListaDeActividades.query.all()
	return render_template("inicio.html", lista=listadeactividades)

@app.route("/acercade")
def acercade():
	return "Página acerca de... "

@app.route("/agregar", methods=["POST"])
def agregar():
	titulo = request.form.get("titulo")
	nueva_actividad = MiListaDeActividades( titulo= titulo, completado= False)
	db.session.add( nueva_actividad )
	db.session.commit()
	return redirect( url_for("inicio"))

@app.route("/actualizar/<int:id_actividad>")
def actualizar(id_actividad):
	actividad = MiListaDeActividades.query.filter_by(id=id_actividad).first()
	actividad.completado = not actividad.completado
	db.session.commit()
	return redirect(url_for("inicio"))

@app.route("/borrar/<int:id_actividad>")
def borrar(id_actividad):
	actividad = MiListaDeActividades.query.filter_by(id=id_actividad).first()
	db.session.delete(actividad)
	db.session.commit()
	return redirect(url_for("inicio"))

