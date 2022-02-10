from datetime import datetime
from listadeactividades import db

class MiListaDeActividades(db.Model):
	id = db.Column( db.Integer, primary_key=True )
	titulo = db.Column( db.String( 100 ))
	completado = db.Column(db.Boolean)