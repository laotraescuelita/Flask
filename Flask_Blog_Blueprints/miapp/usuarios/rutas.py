from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from miapp import db, bcrypt
from miapp.modelos import Usuario, Notas
from miapp.usuarios.formas import (FormaRegistro, FormaIngreso, FormaCuenta,
                                   FormaSolicitarResetear,FormaResetear)
from miapp.usuarios.utils import guardar_foto, enviar_reseteo_correo


usuarios = Blueprint('usuarios', __name__)


@usuarios.route("/registrarse", methods=["POST","GET"])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for("main.inicio"))
    forma = FormaRegistro()
    if forma.validate_on_submit():
        hashed_contraseña = bcrypt.generate_password_hash(forma.contraseña.data).decode("utf-8")
        usuario = Usuario(usuario=forma.usuario.data, correo=forma.correo.data, contraseña=hashed_contraseña)
        db.session.add(usuario)
        db.session.commit()
        flash(f"Tu cuenta ha sido creada. Puedes ingresar", "success")
        return redirect(url_for("usuarios.ingresar"))
    return render_template("registrarse.html", titulo="registrarse", forma=forma)

@usuarios.route("/ingresar", methods=["GET","POST"])
def ingresar():
    if current_user.is_authenticated:
        return redirect(url_for("main.inicio"))
    forma = FormaIngreso()
    if forma.validate_on_submit():
        #if forma.correo.data == "marge@gmail.com" and forma.contraseña.data == "123":
        usuario = Usuario.query.filter_by(correo=forma.correo.data).first()
        if usuario and bcrypt.check_password_hash(usuario.contraseña, forma.contraseña.data):
           login_user(usuario, remember=forma.recordarme.data)
           siguiente_pagina = request.args.get("next")
           return redirect(siguiente_pagina) if siguiente_pagina else redirect(url_for("main.inicio"))
        else:
            flash(f"Ingreso sin exito. Revisa el correo o el usuario", "danger")
    return render_template("ingresar.html", titulo="ingresar", forma=forma)

@usuarios.route("/salir")
def salir():
    logout_user()
    return redirect(url_for("main.inicio"))

@usuarios.route("/cuenta", methods=["GET","POST"])
@login_required
def cuenta():
    forma = FormaCuenta()
    if forma.validate_on_submit():
        if forma.foto.data:
            foto_archivo = guardar_foto(forma.foto.data)
            current_user.imagen = foto_archivo
        current_user.usuario = forma.usuario.data
        current_user.correo = forma.correo.data
        db.session.commit()
        flash("Los datos de la cuenta se actualizaron","success")
        return redirect(url_for("usuarios.cuenta"))
    elif request.method == "GET":
        forma.usuario.data = current_user.usuario
        forma.correo.data = current_user.correo
    imagen = url_for("static", filename='fotos/' + current_user.imagen)
    return render_template("cuenta.html", titulo="cuenta", imagen = imagen, forma=forma)

@usuarios.route("/usuario/<string:usuario>")
def notas_usuario(usuario):
    pagina = request.args.get('page', 1, type=int)
    usuario = Usuario.query.filter_by(usuario=usuario).first_or_404()
    notas = Notas.query.filter_by(autor=usuario)\
        .order_by(Notas.fecha.desc())\
        .paginate(page=pagina, per_page=3)
    return render_template('notas_usuario.html', notas=notas, usuario=usuario)

@usuarios.route("/resetear_contraseña", methods=['GET', 'POST'])
def resetear_solicitud():
    if current_user.is_authenticated:
        return redirect(url_for('main.inicio'))
    forma = FormaSolicitarResetear()
    if forma.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=forma.correo.data).first()
        enviar_reseteo_correo(usuario)
        flash('Un correo ha sido enviado con instruccione para resetear tu contraseña.', 'info')
        return redirect(url_for('usuarios.ingresar'))
    return render_template('resetear_solicitud.html', titulo='Resetear contraseña', forma=forma)


@usuarios.route("/resetear_contraseña/<token>", methods=['GET', 'POST'])
def resetear_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.inicio'))
    usuario = Usuario.verificar_resetear_token(token)
    if usuario is None:
        flash('Ese es un token invalido o expiro', 'warning')
        return redirect(url_for('usuarios.resetear_solicitud'))
    forma = FormaResetear()
    if forma.validate_on_submit():
        hashed_contraseña = bcrypt.generate_password_hash(forma.contraseña.data).decode('utf-8')
        usuario.contraseña = hashed_contraseña
        db.session.commit()
        flash('Tu contraseña ha sido actualizada! Puede ingresar.', 'success')
        return redirect(url_for('usuarios.ingresar'))
    return render_template('resetear_token.html', titulo='Resetear Contraseña', forma=forma)

