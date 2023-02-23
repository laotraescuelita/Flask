from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from miapp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'usuarios.ingresar'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from miapp.usuarios.rutas import usuarios
    from miapp.notas.rutas import notas
    from miapp.main.rutas import main
    from miapp.errores.errores import errores
    app.register_blueprint(usuarios)
    app.register_blueprint(notas)
    app.register_blueprint(main)
    app.register_blueprint(errores)

    return app
