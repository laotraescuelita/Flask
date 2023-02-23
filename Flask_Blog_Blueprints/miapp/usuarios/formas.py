from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from miapp.modelos import Usuario

class FormaRegistro(FlaskForm):
    usuario = StringField('Usuario',
                           validators=[DataRequired(), Length(min=2, max=20)])
    correo = StringField('Correo',
                        validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_contraseña = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('contraseña')])
    enviar = SubmitField('Registrar')

    def validate_usuario(self, usuario):
        usuario = Usuario.query.filter_by(usuario=usuario.data).first()
        if usuario:
            raise ValidationError("Ese usuario existe.Por favor, escribe uno diferente..")

    def validate_correo(self, correo):
        usuario = Usuario.query.filter_by(correo=correo.data).first()
        if usuario:
            raise ValidationError("Ese correo existe.Por favor, escribe uno diferente.")

class FormaIngreso(FlaskForm):
    correo = StringField('Correo',
                        validators=[DataRequired(), Email()])
    contraseña = PasswordField('Constraseña', validators=[DataRequired()])
    recordarme = BooleanField('Recordarme')
    enviar = SubmitField('Ingresar')

class FormaCuenta(FlaskForm):
    usuario = StringField('Usuario',
                           validators=[DataRequired(), Length(min=2, max=20)])
    correo = StringField('Correo',
                        validators=[DataRequired(), Email()])
    foto = FileField('Actualizar foto de perfil', validators=[FileAllowed(['jpg', 'png','jfif'])])
    enviar = SubmitField('Actualizar')

    def validate_usuario(self, usuario):
        if usuario.data != current_user.usuario:
            usuario = Usuario.query.filter_by(usuario=usuario.data).first()
            if usuario:
                raise ValidationError("Ese usuario existe.Por favor, escribe uno diferente..")

    def validate_correo(self, correo):
        if correo.data != current_user.correo:
            usuario = Usuario.query.filter_by(correo=correo.data).first()
            if usuario:
                raise ValidationError("Ese correo existe.Por favor, escribe uno diferente.")


class FormaSolicitarResetear(FlaskForm):
    correo = StringField('Correo',
                        validators=[DataRequired(), Email()])
    enviar = SubmitField('Solicitar reseteo de contraseña')

    def validate_correo(self, correo):
        usuario = Usuario.query.filter_by(correo=correo.data).first()
        if usuario is None:
            raise ValidationError('No hay cuenta con ese correo.Te debes registrar primero.')


class FormaResetear(FlaskForm):
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_contraseña = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('contraseña')])
    enviar = SubmitField('Resetear contraseña')



