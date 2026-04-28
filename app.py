#practica de flask para el its
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


# --- SOLUCIÓN AL ERROR DE UNICODE ---
# Forzamos a que el cliente de Postgres use UTF-8 antes de inicializar algo
os.environ['PGCLIENTENCODING'] = 'utf-8'

app = Flask(__name__)

#jsonify es para retornar un json como respuesta

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost:5432/tareadb?client_encoding=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#definicion del modelo (la tabla en postgres)
class Tarea(db.Model):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False) #que no puede haber datos faltantes o nulos
    completada = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "completada": self.completada}
    

#creamos las tablas en la base de datos(se ejecuta una sola vez,ya que identifica si esta creada, lo ejecuta una vez, pero si ya esta, no hace nada)
with app.app_context():
    try:
        db.create_all()
        print("¡Conexión exitosa y tablas creadas!")
    except Exception as e:
        print(f"Error al conectar: {e}")


#ENDPOINT PARA LA RUTA INICIAL. METODO GET QUE ENVIA UN SALUDO
@app.get("/")
def inicio():
    return jsonify({
        "mensaje": "hola mundo desde flask",
        "descripcion": "conexion a la db exitosa"
    })



#ENDPOINT CON METODO -GET- QUE SE LE PASA POR PARAMETRO EL NOMBRE Y SALUDA CON ESE NOMBRE
@app.get("/saludo/<nombre>")
def saludo(nombre):
    return jsonify({
        "mensaje": f"Hola, {nombre}"
    })


#ENDPOINT PARA LA PETICION -GET- QUE RETORNA TODAS LAS TAREAS
@app.get("/tareas")
def get_tarea():
    tareas = Tarea.query.all()
    if not tareas:
      return jsonify({"mensaje": "no hay tareas"})
    return jsonify([t.to_dict() for t in tareas]), 200



#ENDPOINT PARA LA CREACION DE TAREAS
@app.post("/crear-tarea")
def crear_tarea():
  
    try:
        #capturamos los datos del usuario por el body
        datos = request.get_json() 
        if not datos or "titulo" not in datos:
            return jsonify({"error": "falta el campo 'titulo'"}), 400
        
        #creamos nueva instancia del modelo para la creacion de un nuevo registro
        nueva_tarea = Tarea(
            titulo = datos["titulo"],
            completada = datos.get("completada", False)
        )

        #guardamos en base de datos
        db.session.add(nueva_tarea)
        db.session.commit()

        return jsonify(nueva_tarea.to_dict()), 201

    except Exception as e:
       return jsonify({"error": f"error en la peticion: {e} "})


#endpoint para buscar una tarea por id, que se le pasa por parametros identificando al id
@app.get("/tareas/<int:id>")
def buscar_tarea(id):
    #buscamos por id
    tarea = Tarea.query.get(id) #ese es el metodo para la busqueda de un elemento por su id
    if tarea:
        return jsonify(tarea.to_dict()), 200
    return jsonify({"error": f"no se encuentra esa tarea con id {id}"}), 404

#endpoint -DELETE- para eliminar una tarea por su id
@app.delete("/eliminar-tarea/<int:id>")
def eliminar_tarea(id):
    try:
        #buscamos por el id del parametro
        tarea_id = Tarea.query.get(id)
        #consultamos si no existe ese id, tire error
        if not tarea_id:    
            return jsonify({"error": f"no se encuentra ese id {id} para eliminar"})
        
        #si lo encuentra, que lo elimine
        db.session.delete(tarea_id)
        #hacemos el commit contra la db
        db.session.commit()

        return jsonify({"ok": "se elimino con exito"}), 200

    except Exception as e:
        return jsonify({"error": f"no se pudo eliminar o algo: {e} "})



#endpoint -PUT- para actualizar una tarea buscando por su id
@app.put("/tarea/<int:id>")
def actualizar_tarea(id):
    try:
        tarea = Tarea.query.get(id)
        if not tarea:
            return jsonify({"error": "no existe tarea con ese id"})

        datos = request.get_json()

        #actualizamos los campos si vienen del json, y si algun campo no sufre cambios, mantenemos los mismos que estaban
        tarea.titulo = datos.get("titulo", tarea.titulo)
        tarea.completa = datos.get("completada", tarea.completada)

        #guardamos los cambios
        db.session.commit()

        return jsonify(tarea.to_dict()),200
    

    except Exception as e:
        return jsonify({"error": f"error a la hora de eliminar: {e}"})

if __name__ == "__main__":
    app.run(debug=True)