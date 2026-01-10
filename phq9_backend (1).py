#!/usr/bin/env python3
"""
Backend para Formulario PHQ-9 Clínico
Sistema de almacenamiento y envío de correos para seguimiento longitudinal
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import json
import os
from datetime import datetime
import sqlite3
import hashlib
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuración de correo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.environ.get('EMAIL_USER', '')  # Gmail del sistema
EMAIL_PASS = os.environ.get('EMAIL_PASS', '')  # App password de Gmail
DOCTOR_EMAIL = "breisonvelarde@gmail.com"

# Base de datos SQLite
DB_PATH = "phq9_clinical.db"

def init_database():
    """Inicializar base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phq9_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_email TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            measurement_number INTEGER NOT NULL,
            q1 INTEGER NOT NULL,
            q2 INTEGER NOT NULL,
            q3 INTEGER NOT NULL,
            q4 INTEGER NOT NULL,
            q5 INTEGER NOT NULL,
            q6 INTEGER NOT NULL,
            q7 INTEGER NOT NULL,
            q8 INTEGER NOT NULL,
            q9 INTEGER NOT NULL,
            difficulty INTEGER NOT NULL,
            total_score INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Base de datos inicializada correctamente")

def get_measurement_number(patient_email):
    """Obtener el número de medición para un paciente"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT COUNT(*) FROM phq9_responses WHERE patient_email = ?",
        (patient_email,)
    )
    count = cursor.fetchone()[0]
    conn.close()
    
    return count + 1

def get_previous_score(patient_email):
    """Obtener el puntaje de la medición anterior"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT total_score FROM phq9_responses WHERE patient_email = ? ORDER BY id DESC LIMIT 1",
        (patient_email,)
    )
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

def save_phq9_response(data):
    """Guardar respuesta PHQ-9 en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO phq9_responses 
        (patient_email, timestamp, measurement_number, q1, q2, q3, q4, q5, q6, q7, q8, q9, difficulty, total_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['email'],
        data['timestamp'],
        data['measurement_number'],
        data['responses']['q1'],
        data['responses']['q2'],
        data['responses']['q3'],
        data['responses']['q4'],
        data['responses']['q5'],
        data['responses']['q6'],
        data['responses']['q7'],
        data['responses']['q8'],
        data['responses']['q9'],
        data['responses']['difficulty'],
        data['total_score']
    ))
    
    conn.commit()
    conn.close()
    logger.info(f"Respuesta guardada para paciente: {data['email']}")

def get_response_text(value):
    """Convertir valor numérico a texto descriptivo"""
    texts = ['Para nada', 'Varios días', 'Más de la mitad de los días', 'Casi todos los días']
    return f"{texts[value]} ({value})"

def get_difficulty_text(value):
    """Convertir valor de dificultad a texto"""
    texts = ['Nada en absoluto', 'Algo difícil', 'Muy difícil', 'Extremadamente difícil']
    return f"{texts[value]} ({value})"

def send_email_to_doctor(data):
    """Enviar correo electrónico al médico con los resultados"""
    try:
        # Crear mensaje
        msg = MimeMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = DOCTOR_EMAIL
        msg['Subject'] = f"PHQ-9 #{data['measurement_number']} - {data['email']}"
        
        # Generar contenido del correo
        previous_score = get_previous_score(data['email'])
        if previous_score is not None and data['measurement_number'] > 1:
            difference = data['total_score'] - previous_score
            trend = '↑' if difference > 0 else '↓' if difference < 0 else '='
            trend_text = f"\nTENDENCIA: {trend} (Diferencia: {'+' if difference > 0 else ''}{difference} puntos respecto a medición anterior)"
        else:
            trend_text = "\nTENDENCIA: Primera medición"
        
        email_content = f"""
REPORTE PHQ-9 - SEGUIMIENTO CLÍNICO
=====================================

INFORMACIÓN DEL PACIENTE:
- Correo electrónico: {data['email']}
- Fecha y hora: {data['date']} {data['time']}
- Número de medición: PHQ-9 #{data['measurement_number']}

PUNTAJE ACTUAL:
- Puntaje total PHQ-9: {data['total_score']}/27

RESPUESTAS ACTUALES:
1. Poco interés o placer: {get_response_text(data['responses']['q1'])}
2. Sentirse decaído/deprimido: {get_response_text(data['responses']['q2'])}
3. Problemas de sueño: {get_response_text(data['responses']['q3'])}
4. Fatiga/poca energía: {get_response_text(data['responses']['q4'])}
5. Problemas de apetito: {get_response_text(data['responses']['q5'])}
6. Sentimientos negativos sobre sí mismo: {get_response_text(data['responses']['q6'])}
7. Problemas de concentración: {get_response_text(data['responses']['q7'])}
8. Cambios psicomotores: {get_response_text(data['responses']['q8'])}
9. Pensamientos de muerte/autolesión: {get_response_text(data['responses']['q9'])}

IMPACTO FUNCIONAL:
- Dificultad para actividades diarias: {get_difficulty_text(data['responses']['difficulty'])}
{trend_text}

--- Fin del reporte ---
Este reporte es confidencial y destinado exclusivamente para revisión clínica.
Sistema PHQ-9 Clínico - Dr. Breison Velarde
"""
        
        msg.attach(MimeText(email_content, 'plain', 'utf-8'))
        
        # Enviar correo
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, DOCTOR_EMAIL, text)
        server.quit()
        
        logger.info(f"Correo enviado exitosamente al Dr. Breison Velarde para paciente: {data['email']}")
        return True
        
    except Exception as e:
        logger.error(f"Error enviando correo: {str(e)}")
        return False

@app.route('/')
def index():
    """Página principal con el formulario PHQ-9"""
    return render_template_string(open('phq9_clinico_real.html', 'r', encoding='utf-8').read())

@app.route('/api/submit-phq9', methods=['POST'])
def submit_phq9():
    """Endpoint para recibir y procesar respuestas PHQ-9"""
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['email', 'responses']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'}), 400
        
        # Calcular puntaje total
        total_score = sum(data['responses'][f'q{i}'] for i in range(1, 10))
        
        # Preparar datos para almacenamiento
        current_datetime = datetime.now()
        measurement_number = get_measurement_number(data['email'])
        
        submission_data = {
            'email': data['email'],
            'timestamp': current_datetime.isoformat(),
            'date': current_datetime.strftime('%d/%m/%Y'),
            'time': current_datetime.strftime('%H:%M:%S'),
            'responses': data['responses'],
            'total_score': total_score,
            'measurement_number': measurement_number
        }
        
        # Guardar en base de datos
        save_phq9_response(submission_data)
        
        # Enviar correo al médico
        email_sent = send_email_to_doctor(submission_data)
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Cuestionario enviado exitosamente',
                'measurement_number': measurement_number
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error enviando notificación al médico'
            }), 500
            
    except Exception as e:
        logger.error(f"Error procesando PHQ-9: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud del sistema"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if os.path.exists(DB_PATH) else 'not_found'
    })

if __name__ == '__main__':
    # Inicializar base de datos
    init_database()
    
    # Verificar configuración de correo
    if not EMAIL_USER or not EMAIL_PASS:
        logger.warning("Variables de entorno EMAIL_USER y EMAIL_PASS no configuradas")
        logger.warning("El envío de correos no funcionará correctamente")
    
    # Ejecutar aplicación
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)