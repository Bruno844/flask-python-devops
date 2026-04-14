#practica de flask para el its
from flask import Flask, jsonify


app = Flask(__name__)

#jsonify es para retornar un json como respuesta



@app.get("/")
def inicio():
    return jsonify({
        "mensaje": "hola mundo desde flask",
        "descripcion": "esta es una api minima"
    })


@app.get("/saludo/<nombre>")
def saludo(nombre):
    return jsonify({
        "mensaje": f"Hola, {nombre}"
    })


@app.route("/empleados", methods=["GET"])
def get_empleados():

    empleados = [
        {"id": 1, "nombre": "bruno", "apellido": "ruiz"},
        {"id": 2, "nombre": "usuario1", "apellido": "apellido1"},
        {"id": 3, "nombre": "usuario2", "apellido": "apellido2"},
        {"id": 4, "nombre": "usuario3", "apellido": "apellido3"}
    ]
    return jsonify(empleados)
    


if __name__ == "__main__":
    app.run(debug=True)