from flask import render_template, request, Blueprint
from miapp.modelos import Notas

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/inicio")
def inicio():
    
    pagina = request.args.get('page',1, type=int)
    notas = Notas.query.order_by(Notas.fecha.desc()).paginate(page=pagina, per_page=3)
    return render_template("inicio.html", notas=notas)

@main.route("/acercade")
def acercade():
    return render_template("acercade.html", titulo = "acerca de")
