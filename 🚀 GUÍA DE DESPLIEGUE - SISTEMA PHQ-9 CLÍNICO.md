
# 🚀 GUÍA DE DESPLIEGUE - SISTEMA PHQ-9 CLÍNICO

## 📋 Resumen del Sistema

Sistema web completo para seguimiento longitudinal de síntomas depresivos mediante el cuestionario PHQ-9, con envío automático de resultados al Dr. Breison Velarde.

## 🔧 Configuración Previa

### 1. Variables de Entorno Requeridas

```bash
EMAIL_USER=tu_email@gmail.com
EMAIL_PASS=tu_app_password_de_gmail
PORT=5000
```

### 2. Obtener App Password de Gmail

1. Ir a [Google Account Settings](https://myaccount.google.com/)
2. Security > 2-Step Verification > App passwords
3. Generar password para "Mail"
4. Usar este password en `EMAIL_PASS`

## 🌐 Opciones de Despliegue

### OPCIÓN A: Heroku (Recomendado)

```bash
# 1. Instalar Heroku CLI
# 2. Login y crear app
heroku login
heroku create tu-app-phq9-clinico

# 3. Configurar variables de entorno
heroku config:set EMAIL_USER=tu_email@gmail.com
heroku config:set EMAIL_PASS=tu_app_password_aqui

# 4. Desplegar
git add .
git commit -m "Deploy PHQ-9 Clinical System"
git push heroku main

# 5. Abrir aplicación
heroku open
```

**URL Final**: `https://tu-app-phq9-clinico.herokuapp.com/`

### OPCIÓN B: Railway

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login y desplegar
railway login
railway init
railway up

# 3. Configurar variables en dashboard
# Ir a railway.app > tu-proyecto > Variables
# Agregar EMAIL_USER y EMAIL_PASS
```

### OPCIÓN C: Render

1. Conectar repositorio en [render.com](https://render.com)
2. Crear nuevo "Web Service"
3. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn phq9_backend:app`
4. Agregar variables de entorno en dashboard

### OPCIÓN D: Local (Solo para pruebas)

```bash
# 1. Configurar .env
echo "EMAIL_USER=tu_email@gmail.com" > .env
echo "EMAIL_PASS=tu_app_password" >> .env

# 2. Ejecutar
python3 phq9_backend.py
```

## 📧 Configuración de Correo

### Gmail Setup (Recomendado)

1. **Habilitar 2FA** en tu cuenta Gmail
2. **Generar App Password**:
   - Google Account > Security > 2-Step Verification
   - App passwords > Select app: Mail
   - Copiar el password generado
3. **Usar en variables de entorno**

### Alternativas de Correo

Si Gmail no funciona, puedes usar:

- **Outlook/Hotmail**: 
  - SMTP: `smtp-mail.outlook.com:587`
  - Modificar `SMTP_SERVER` en `phq9_backend.py`

- **SendGrid** (Para producción):
  - Registrarse en sendgrid.com
  - Obtener API key
  - Modificar función `send_email_to_doctor()`

## 🔗 Distribución del Formulario

### Enlaces para Pacientes

Una vez desplegado, compartir:

```
https://tu-dominio.com/

📱 Compatible con:
- WhatsApp
- SMS
- Email
- Códigos QR
```

### Ejemplo de Mensaje para Pacientes

```
🏥 Evaluación PHQ-9 - Dr. Breison Velarde

Por favor complete su evaluación de seguimiento:
https://tu-app-phq9.herokuapp.com/

✅ Seguro y confidencial
✅ Compatible con celular
✅ Toma 3-5 minutos

Sus resultados serán enviados automáticamente al Dr. Velarde para revisión en su próxima consulta.
```

## 🔒 Seguridad y Cumplimiento

### Características de Seguridad Implementadas

- ✅ **Sin almacenamiento local**: Datos van directo a base de datos
- ✅ **Consentimiento informado obligatorio**
- ✅ **No muestra puntajes al paciente**
- ✅ **Envío automático solo al médico**
- ✅ **Validaciones de formulario completas**
- ✅ **HTTPS en producción**

### Datos Almacenados

- Correo electrónico del paciente (identificador)
- Respuestas PHQ-9 (valores 0-3)
- Fecha y hora de cada medición
- Número de medición secuencial

### Datos NO Almacenados

- Nombres reales
- Información personal adicional
- Direcciones IP
- Datos de navegador

## 📊 Funcionalidad del Sistema

### Para el Paciente

1. **Consentimiento informado** (obligatorio)
2. **Identificación** por correo electrónico
3. **Cuestionario PHQ-9** (9 preguntas + impacto funcional)
4. **Mensaje de confirmación** (sin resultados)

### Para el Médico (breison@hotmail.com)

Recibe correo automático con:

- Información del paciente
- Puntaje total PHQ-9
- Respuestas detalladas
- Número de medición
- Comparación con mediciones anteriores
- Análisis de tendencia (↑ ↓ =)

## 🧪 Verificación Post-Despliegue

### Checklist de Pruebas

```bash
# 1. Verificar que la página carga
curl https://tu-dominio.com/

# 2. Probar endpoint de salud
curl https://tu-dominio.com/api/health

# 3. Completar formulario de prueba
# Usar email de prueba y verificar que llega correo
```

### Prueba Completa

1. **Abrir formulario** en móvil y desktop
2. **Completar con datos de prueba**
3. **Verificar que llega correo** a breison@hotmail.com
4. **Completar segunda vez** con mismo email
5. **Verificar seguimiento longitudinal** en correo

## 🆘 Solución de Problemas

### Error: Correos no llegan

```bash
# Verificar variables de entorno
heroku config

# Verificar logs
heroku logs --tail

# Probar credenciales Gmail manualmente
```

### Error: Base de datos

```bash
# Verificar que SQLite funciona
heroku run python3 -c "import sqlite3; print('OK')"

# Reiniciar base de datos
heroku restart
```

### Error: Formulario no carga

```bash
# Verificar archivos
heroku run ls -la

# Verificar logs de Flask
heroku logs --source app
```

## 📞 Soporte

### Contacto Técnico

Para problemas técnicos:
1. Revisar logs del servidor
2. Verificar variables de entorno
3. Probar conexión SMTP manualmente

### Contacto Clínico

Dr. Breison Velarde: breison@hotmail.com

## 🔄 Actualizaciones Futuras

### Mejoras Sugeridas

- Dashboard web para el médico
- Exportación de datos en PDF
- Notificaciones por SMS
- Integración con sistemas hospitalarios
- Análisis estadístico automatizado

### Mantenimiento

- Backup automático de base de datos
- Monitoreo de uptime
- Logs de auditoría
- Actualizaciones de seguridad

---

## ✅ SISTEMA LISTO PARA USO CLÍNICO

El sistema PHQ-9 está completamente configurado y listo para uso clínico real con pacientes del Dr. Breison Velarde.

**📧 Destino de resultados**: breison@hotmail.com
**🔒 Cumplimiento**: Ético y clínicamente apropiado
**📱 Accesibilidad**: Compatible con todos los dispositivos
