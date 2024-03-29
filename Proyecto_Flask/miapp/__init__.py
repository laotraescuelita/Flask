import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'ingresar'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#Configuracion de otro canal de youtube.
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True

app.config['MAIL_USERNAME'] = os.environ.get('CORREO')
app.config['MAIL_PASSWORD'] = os.environ.get('CONTRASEÑA')
#app.config['MAIL_PASSWORD'] = os.environ.get('wkqfkmuwpjivwdux')
mail = Mail(app)

from miapp import rutas