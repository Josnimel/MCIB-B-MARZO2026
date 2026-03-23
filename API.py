from flask import Flask, jsonify, render_template, request   

app = Flask(__name__)
@app.route('/')
def index():
    return jsonify({"message": "API FUNCIONANDO ADECUADAMENTE"})

#SALUDO
@app.route('/saludo', methods=['GET'])
def saludo():
    nombre = request.args.get('nombre', 'Invitado ')
    return jsonify({"saludo": f"Hola, {nombre}!"})

#SEGURIDAD
@app.route('/seguridad', methods=['GET'])
def seguridad():
    tips = [
        "Usa Contraseñas seguras",
        "No compartas tus credenciales",
        "Usa autenticación multifactor"
    ]
    return jsonify({"tips": tips})

#FORMULARIO
@app.route('/formulario', methods=['GET'])
def mostrar_formulario():
    return           render_template('formulario.html')

#EVALUAR PASSWORD
@app.route('/evaluar_password', methods=['POST'])
def evaluar_password():
    #DETECTAR SI LOS DATOS SON EN FORMATO JSON O FORMULARIO
    if request.is_json:
        data = request.get_json()
        password = data.get('password', '')
    else:     
        password = request.form.get('password', '')
    if not password:
        return jsonify({"error": "No se proporcionó una contraseña para evaluar"}), 400
    
    #EVALUAR LA CONTRASEÑA
    Puntaje = 0
    Recommendaciones = []
    
    #REGLAS DE EVALUACIÓN
    if len(password) <=5:
        Puntaje += 2
    elif len(password) <= 8:
        Puntaje += 1
    else:
        Recommendaciones.append("La contraseña es muy corta. Considera usar al menos 8 caracteres.")
        
    if any(c.islower() for c in password):
        Puntaje += 1
    else:
        Recommendaciones.append("La contraseña debe contener al menos una letra minúscula.")
    if any(c.isupper() for c in password):
        Puntaje += 1
    else:
        Recommendaciones.append("La contraseña debe contener al menos una letra mayúscula.")    
    if any(c.isdigit() for c in password):
        Puntaje += 1 
    else:
        Recommendaciones.append("La contraseña debe contener al menos un número.")      
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password):        
        Puntaje += 1
    else:
        Recommendaciones.append("La contraseña debe contener al menos un carácter especial.")
    if Puntaje <= 2:
        Fortaleza = "Débil"
        color = "red"
    elif Puntaje <= 4:
        Fortaleza = "Moderada"
        color = "orange"     
    else:        Fortaleza = "Fuerte"        
    color = "green"
    return jsonify({    
        "fortaleza": Fortaleza,
        "color": color,
        "recomendaciones": Recommendaciones
    })
  
