from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from miapp import db
from miapp.modelos import Notas
from miapp.notas.formas import FormaNotas

notas = Blueprint('notas', __name__)

@notas.route("/nota/nueva", methods=["GET","POST"])
@login_required
def nueva_nota():
    forma = FormaNotas()
    if forma.validate_on_submit():
        nota = Notas(titulo=forma.titulo.data, contenido=forma.contenido.data, autor=current_user)
        db.session.add(nota)
        db.session.commit()
        flash("Tu nota ha sido creada!","success")
        return redirect(url_for("main.inicio"))
    return render_template("crear_nota.html", titulo="Nueva nota", forma=forma, leyenda="Nueva nota")


@notas.route("/nota/<int:nota_id>")
def nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    return render_template('nota.html', title=nota.titulo, nota=nota)

@notas.route("/nota/<int:nota_id>/actualizar", methods=['GET', 'POST'])
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
        return redirect(url_for('notas.nota', nota_id=nota.id))
    elif request.method == 'GET':
        forma.titulo.data = nota.titulo
        forma.contenido.data = nota.contenido
    return render_template('crear_nota.html', titulo='Actualizar Nota',
                           forma=forma, leyenda='Actualizar nota')

@notas.route("/nota/<int:nota_id>/eliminar", methods=['POST'])
@login_required
def eliminar_nota(nota_id):
    nota = Notas.query.get_or_404(nota_id)
    if nota.autor != current_user:
        abort(403)
    db.session.delete(nota)
    db.session.commit()
    flash('Tu nota ha sido eliminada!', 'success')
    return redirect(url_for('main.inicio'))




