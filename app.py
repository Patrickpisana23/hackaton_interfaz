import json
from flask import Flask, render_template, request, redirect, url_for
import smtplib

app = Flask(__name__)

# Cargar datos del archivo JSON
with open('response_prompt_2.json', 'r') as file:
    data = json.load(file)

@app.route('/')
def index():
    return redirect(url_for('info'))

@app.route('/info')
def info():
    return render_template('info.html', users=data)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', users=data)

@app.route('/add_user', methods=['POST'])
def add_user():
    selected_user = request.form.get('userSelect')
    
    # Buscar el correo electrónico y el discurso del usuario seleccionado en los datos cargados
    selected_user_email = None
    selected_user_speech = None
    for user in data:
        if user['CLIENTE_APENOM'] == selected_user:
            selected_user_email = user.get('CORREO', None)
            selected_user_speech = user.get('speech', None)
            break
    
    # Enviar correo electrónico al usuario seleccionado si se encontró su dirección de correo electrónico
    if selected_user_email:
        send_email(selected_user_email, selected_user_speech)
    
    return redirect(url_for('info'))

def send_email(email, speech):
    # Configurar el servidor SMTP y enviar el correo electrónico
    smtp_server = 'tu_servidor_smtp'
    smtp_port = 587
    sender_email = 'tu_correo@gmail.com'  # Debe ser una dirección de correo electrónico válida
    password = 'tu_contraseña'  # Debes configurar la autenticación de correo electrónico correctamente

    subject = f'Speech para {email}'  # Asunto del correo personalizado con el correo electrónico del usuario
    body = speech  # Contenido del correo

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)

if __name__ == '__main__':
    app.run(debug=True)
