import os 
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from miapp import app, db, bcrypt, mail
from miapp.formularios import FormaRegistro, FormaIngreso, FormaCuenta, FormaNotas, FormaResetear, FormaSolicitarResetear
from miapp.modelos import Usuario, Notas
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/inicio")
def inicio():
    
    pagina = request.args.get('page',1, type=int)
    notas = Notas.query.order_by(Notas.fecha.desc()).paginate(page=pagina, per_page=3)
    return render_template("inicio.html", notas=notas)

@app.route("/acercade")
def acercade():
    return render_template("acercade.html", titulo = "acerca de")

@app.route("/registrarse", methods=["POST","GET"])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    forma = FormaRegistro()
    if forma.validate_on_submit():
        hashed_contraseña = bcrypt.generate_password_hash(forma.contraseña.data).decode("utf-8")
        usuario = Usuario(usuario=forma.usuario.data, correo=forma.correo.data, contraseña=hashed_contraseña)
        db.session.add(usuario)
        db.session.commit()
        flash(f"Tu cuenta ha sido creada. Puedes ingresar", "success")
        return redirect(url_for("ingresar"))
    return render_template("registrarse.html", titulo="registrarse", forma=forma)

@app.route("/ingresar", methods=["GET","POST"])
def ingresar():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    forma = FormaIngreso()
    if forma.validate_on_submit():
        #if forma.correo.data == "marge@gmail.com" and forma.contraseña.data == "123":
        usuario = Usuario.query.filter_by(correo=forma.correo.data).first()
        if usuario and bcrypt.check_password_hash(usuario.contraseña, forma.contraseña.data):
           login_user(usuario, remember=forma.recordarme.data)
           siguiente_pagina = request.args.get("next")
           return redirect(siguiente_pagina) if siguiente_pagina else redirect(url_for("inicio"))
        else:
            flash(f"Ingreso sin exito. Revisa el correo o el usuario", "danger")
    return render_template("ingresar.html", titulo="ingresar", forma=forma)

@app.route("/salir")
def salir():
    logout_user()
    return redirect(url_for("inicio"))

def guardar_foto(foto):
    numeros_al_azar = secrets.token_hex(8)
    _, extension = os.path.splitext(foto.filename)
    foto_guardada = numeros_al_azar + extension
    ruta_foto = os.path.join(app.root_path, "static/fotos", foto_guardada)

    tamaño_final = (125,125)
    i = Image.open(foto)
    i.thumbnail(tamaño_final)
    i.save(ruta_foto)

    return foto_guardada

@app.route("/cuenta", methods=["GET","POST"])
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
        return redirect(url_for("cuenta"))
    elif request.method == "GET":
        forma.usuario.data = current_user.usuario
        forma.correo.data = current_user.correo
    imagen = url_for("static", filename='fotos/' + current_user.imagen)
    return render_template("cuenta.html", titulo="cuenta", imagen = imagen, forma=forma)

@app.route("/nota/nueva", methods=["GET","POST"])
@login_required
def nueva_nota():
    forma = FormaNotas()
    if forma.validate_on_submit():
        nota = Notas(titulo=forma.titulo.data, contenido=forma.contenido.data, autor=current_user)
        db.session.add(nota)
        db.session.commit()
        flash("Tu nota ha sido creada!","success")
        return redirect(url_for("inicio"))
    return render_template("crear_nota.html", titulo="Nueva nota", forma=forma, leyenda="Nueva nota")


@app.route("/nota/<int:nota_id>")
def nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    return render_template('nota.html', title=nota.titulo, nota=nota)

@app.route("/nota/<int:nota_id>/actualizar", methods=['GET', 'POST'])
@login_required
def actualizar_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    if nota.autor != current_user:
        abort(403)
    forma = FormaNotas()
    if forma.validate_on_submit():
        nota.titulo = forma.titulo.data
        nota.contenido = forma.contenido.data
        db.session.commit()
        flash('Tu Nota se ha actualizado!', 'success')
        return redirect(url_for('nota', nota_id=nota.id))
    elif request.method == 'GET':
        forma.titulo.data = nota.titulo
        forma.contenido.data = nota.contenido
    return render_template('crear_nota.html', titulo='Actualizar Nota',
                           forma=forma, leyenda='Actualizar nota')

@app.route("/nota/<int:nota_id>/eliminar", methods=['POST'])
@login_required
def eliminar_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    if nota.autor != current_user:
        abort(403)
    db.session.delete(nota)
    db.session.commit()
    flash('Tu nota ha sido eliminada!', 'success')
    return redirect(url_for('inicio'))

@app.route("/usuario/<string:usuario>")
def notas_usuario(usuario):
    pagina = request.args.get('page', 1, type=int)
    usuario = Usuario.query.filter_by(usuario=usuario).first_or_404()
    notas = Notas.query.filter_by(autor=usuario)\
        .order_by(Notas.fecha.desc())\
        .paginate(page=pagina, per_page=3)
    return render_template('notas_usuario.html', notas=notas, usuario=usuario)

def enviar_reseteo_correo(usuario):
    token = usuario.resetear_token()
    msg = Message('Solicitud de reseteo de contraseña',
                  sender='noreply@demo.com',
                  recipients=[usuario.correo])
    msg.body = f'''Para resetear tu contraseña, visita la siguiente liga:
{url_for('resetear_token', token=token, _external=True)}

Si no solicitaste el reseteo simplemente ignora el correo y no se hara ningun cambio.
'''
    mail.send(msg)


@app.route("/resetear_contraseña", methods=['GET', 'POST'])
def resetear_solicitud():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    forma = FormaSolicitarResetear()
    if forma.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=forma.correo.data).first()
        enviar_reseteo_correo(usuario)
        flash('Un correo ha sido enviado con instruccione para resetear tu contraseña.', 'info')
        return redirect(url_for('ingresar'))
    return render_template('resetear_solicitud.html', titulo='Resetear contraseña', forma=forma)


@app.route("/resetear_contraseña/<token>", methods=['GET', 'POST'])
def resetear_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    usuario = Usuario.verificar_resetear_token(token)
    if usuario is None:
        flash('Ese es un token invalido o expiro', 'warning')
        return redirect(url_for('resetear_solicitud'))
    forma = FormaResetear()
    if forma.validate_on_submit():
        hashed_contraseña = bcrypt.generate_password_hash(forma.contraseña.data).decode('utf-8')
        usuario.contraseña = hashed_contraseña
        db.session.commit()
        flash('Tu contraseña ha sido actualizada! Puede ingresar.', 'success')
        return redirect(url_for('ingresar'))
    return render_template('resetear_token.html', titulo='Resetear Contraseña', forma=forma)
