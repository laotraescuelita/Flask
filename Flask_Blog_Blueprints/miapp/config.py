import os

class Config:
	# estos dos primeros campos es mejor tenerlos en variables globales del sistema operativo
	SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
	SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('CORREO')
	MAIL_PASSWORD = os.environ.get('CONTRASEÑA')
	#MAIL_PASSWORD = os.environ.get('wkqfkmuwpjivwdux')
