import time
try:
    import pywhatkit
except ImportError:
    pywhatkit = None

def send_payment_reminder(phone_number, student_name, month, amount):
    """
    Envía un recordatorio de pago a través de WhatsApp Web.
    Requiere que la sesión de WhatsApp Web esté abierta en el navegador predeterminado.
    """
    if not pywhatkit:
        print("La librería pywhatkit no está instalada. Ejecuta: pip install pywhatkit")
        return False
        
    message = (
        f"🥋 *Dojang Taekwondo Segma* 🥋\n\n"
        f"Estimado padre/apoderado,\n"
        f"Le recordamos amablemente que la pensión del alumno *{student_name}* "
        f"correspondiente al mes de *{month}* por el monto de *S/ {amount}* se encuentra pendiente.\n\n"
        f"Por favor regularizar a la brevedad. ¡Gracias por su compromiso!"
    )
    
    # Formato de número: debe incluir código de país, ej. +51999999999
    if not phone_number.startswith('+'):
        # Asumiendo Perú (+51) por defecto, ajustar según necesidad
        phone_number = f"+51{phone_number}"
        
    try:
        # Enviar mensaje instantáneamente y cerrar la pestaña en 15 segundos
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=10, tab_close=True, close_time=5)
        print(f"Mensaje enviado a {phone_number} exitosamente.")
        return True
    except Exception as e:
        print(f"Error al enviar mensaje a {phone_number}: {e}")
        return False
