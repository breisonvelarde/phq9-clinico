#!/usr/bin/env python3
"""
Script de configuración para despliegue del sistema PHQ-9 clínico
"""

import os
import subprocess
import sys

def install_dependencies():
    """Instalar dependencias de Python"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crear archivo .env con configuración"""
    env_content = """# Configuración del sistema PHQ-9 clínico
# IMPORTANTE: Configurar estas variables antes del despliegue

# Configuración de correo electrónico (Gmail)
EMAIL_USER=tu_email@gmail.com
EMAIL_PASS=tu_app_password_de_gmail

# Puerto del servidor (opcional)
PORT=5000

# Configuración de base de datos
DB_PATH=phq9_clinical.db
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        print("⚠️  IMPORTANTE: Editar .env con las credenciales reales")
    else:
        print("ℹ️  Archivo .env ya existe")

def test_system():
    """Probar el sistema básico"""
    print("🧪 Probando sistema...")
    
    # Verificar archivos principales
    required_files = [
        'phq9_backend.py',
        'phq9_clinico_real.html',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los archivos principales están presentes")
    
    # Probar importación de módulos
    try:
        import flask
        import flask_cors
        print("✅ Módulos de Flask importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    
    return True

def create_startup_script():
    """Crear script de inicio"""
    startup_content = """#!/bin/bash
# Script de inicio para PHQ-9 clínico

echo "🏥 Iniciando sistema PHQ-9 clínico..."

# Verificar variables de entorno
if [ -z "$EMAIL_USER" ] || [ -z "$EMAIL_PASS" ]; then
    echo "⚠️  Variables EMAIL_USER y EMAIL_PASS no configuradas"
    echo "   Editando archivo .env..."
fi

# Iniciar servidor
python3 phq9_backend.py
"""
    
    with open('start_server.sh', 'w') as f:
        f.write(startup_content)
    
    # Hacer ejecutable
    os.chmod('start_server.sh', 0o755)
    print("✅ Script de inicio creado: start_server.sh")

def print_deployment_instructions():
    """Mostrar instrucciones de despliegue"""
    instructions = """
🚀 INSTRUCCIONES DE DESPLIEGUE
===============================

1. CONFIGURACIÓN DE CORREO:
   - Editar archivo .env
   - Configurar EMAIL_USER con una cuenta Gmail
   - Configurar EMAIL_PASS con App Password de Gmail
   
   Para obtener App Password:
   - Ir a Google Account Settings
   - Security > 2-Step Verification > App passwords
   - Generar password para "Mail"

2. EJECUTAR LOCALMENTE:
   python3 phq9_backend.py
   
   O usar el script:
   ./start_server.sh

3. DESPLIEGUE EN PRODUCCIÓN:
   
   OPCIÓN A - Heroku:
   - heroku create tu-app-phq9
   - git add .
   - git commit -m "Deploy PHQ-9"
   - heroku config:set EMAIL_USER=tu_email@gmail.com
   - heroku config:set EMAIL_PASS=tu_app_password
   - git push heroku main
   
   OPCIÓN B - Railway:
   - railway login
   - railway init
   - railway add
   - railway deploy
   
   OPCIÓN C - Render:
   - Conectar repositorio en render.com
   - Configurar variables de entorno
   - Deploy automático

4. CONFIGURACIÓN DE VARIABLES:
   EMAIL_USER=tu_email@gmail.com
   EMAIL_PASS=tu_app_password_de_gmail
   PORT=5000

5. URL FINAL:
   https://tu-dominio.com/
   
   El formulario estará disponible en la raíz del dominio.

⚠️  IMPORTANTE:
- Nunca subir credenciales al repositorio
- Usar variables de entorno en producción
- Probar envío de correos antes del uso clínico
- Verificar que breisonvelarde@gmail.com reciba los reportes

📧 CORREO DE DESTINO: breisonvelarde@gmail.com
"""
    
    print(instructions)

def main():
    """Función principal de configuración"""
    print("🏥 CONFIGURACIÓN DEL SISTEMA PHQ-9 CLÍNICO")
    print("=" * 50)
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Crear archivo de configuración
    create_env_file()
    
    # Probar sistema
    if not test_system():
        return False
    
    # Crear script de inicio
    create_startup_script()
    
    # Mostrar instrucciones
    print_deployment_instructions()
    
    print("✅ Configuración completada exitosamente")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)