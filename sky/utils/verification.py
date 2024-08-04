import re
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def emailVerification(email):    
    if re.fullmatch(regex_email, email):
        return ""
    else:
        return "Correo no es válido"
def userVerification(user):
    if len(user)<6:
        return "Usuario muy corto"
    else:
        return ""
def passVerification(password):
    if len(password)<8:
        return "Contraseña muy corta"
    else:
        return ""