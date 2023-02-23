import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from miapp import mail

def guardar_foto(foto):
    numeros_al_azar = secrets.token_hex(8)
    _, extension = os.path.splitext(foto.filename)
    foto_guardada = numeros_al_azar + extension
    ruta_foto = os.path.join(current_app.root_path, "static/fotos", foto_guardada)

    tamaño_final = (125,125)
    i = Image.open(foto)
    i.thumbnail(tamaño_final)
    i.save(ruta_foto)

    return foto_guardada

def enviar_reseteo_correo(usuario):
    token = usuario.resetear_token()
    msg = Message('Solicitud de reseteo de contraseña',
                  sender='noreply@demo.com',
                  recipients=[usuario.correo])
    msg.body = f'''Para resetear tu contraseña, visita la siguiente liga:
{url_for('usuarios.resetear_token', token=token, _external=True)}
Si no solicitaste el reseteo simplemente ignora el correo y no se hara ningun cambio.
'''
    mail.send(msg)