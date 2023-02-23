from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class FormaNotas(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    contenido = TextAreaField('Contenido', validators=[DataRequired()])
    enviar = SubmitField('Nota')
