from datetime import datetime
#from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from miapp import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    imagen = db.Column(db.String(20), nullable=False, default='default.jpg')
    contraseña = db.Column(db.String(60), nullable=False)
    notas = db.relationship('Notas', backref='autor', lazy=True)

    def resetear_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'usuario_id': self.id}).decode('utf-8')

    @staticmethod
    def verificar_resetear_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            usuario = s.loads(token)['usuario_id']
        #except (BadSignature, SignatureExpired) :
        except :
            return None
        return Usuario.query.get(usuario)

    def __rep__(self):
        return f"Usuario('{self.usuario}', '{self.correo}', '{self.imagen}')"


class Notas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"Notas('{self.titulo}', '{self.fecha}')"

