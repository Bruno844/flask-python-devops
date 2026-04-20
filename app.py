#practica de flask para el its
from flask import Flask, jsonify, request


app = Flask(__name__)

#jsonify es para retornar un json como respuesta

tareas = [
 {"id": 1, "titulo": "Leer sobre APIs", "completada": False},
 {"id": 2, "titulo": "Probar Postman", "completada": True},
 {"id": 3, "titulo": "test tarea 3", "completada": False},
 {"id": 4, "titulo": "test tarea 4", "completada": True},
 {"id": 5, "titulo": "test tarea 5", "completada": False},
 {"id": 6, "titulo": "test tarea 6", "completada": True}
]


#ENDPOINT PARA LA RUTA INICIAL. METODO GET QUE ENVIA UN SALUDO
@app.get("/")
def inicio():
    return jsonify({
        "mensaje": "hola mundo desde flask",
        "descripcion": "esta es una api minima"
    })



#ENDPOINT CON METODO -GET- QUE SE LE PASA POR PARAMETRO EL NOMBRE Y SALUDA CON ESE NOMBRE
@app.get("/saludo/<nombre>")
def saludo(nombre):
    return jsonify({
        "mensaje": f"Hola, {nombre}"
    })


#ENDPOINT PARA LA PETICION -GET- QUE RETORNA TODAS LAS TAREAS
@app.route("/tareas", methods=["GET"])
def get_tarea():
   return jsonify(tareas),200



@app.post("/crear-tarea")
def crear_tarea():
    #con esta variable, capturamos lo que nos manda el usuario por el body en formato json
    datos = request.get_json()

    try:

        #si manda la peticion y no hay datos, que lance un error
        if not datos:
            return jsonify({"error": "debe enviar un json en el body"}), 404
        if "titulo" not in datos:
            return jsonify({"error": "no envio los datos necesarios"}), 404
        #creamos la nueva tarea asignandole un nuevo id
        nuevo_id = tareas[-1]["id"] + 1 if tareas else 1
        #aca concatenamos el nuevo id con los datos que nos pasen por el body
        nueva_tarea = {"id": nuevo_id, "titulo": datos["titulo"], "completada": datos.get("completada", False)}
        #por defecto obtenemos el campo completada en false, no es necesario colocarlo en la peticion

        #agregamos al array de tareas, la nueva tarea con el metodo .append    
        tareas.append(nueva_tarea)
        
        #y aca retornamos con jsonify la nueva tarea y con codigo 201 que salio con exito 
        return jsonify(nueva_tarea), 201 
        
    #aca con except capturamos cualquier fuga o error que haya salido de la peticion y la mostramos con un mensaje    
    except Exception as e:
        return jsonify(f"error en la peticion:", e)


#endpoint para buscar una tarea por id, que se le pasa por parametros identificando al id
@app.get("/tareas/<int:id>")
def buscar_tarea(id):
    #recorremos el arreglo de tareas
    for tarea in tareas:
        #consultamos si el id que esta en el array, es igual al que buscamos por parametro
        if tarea["id"] == id:
            return jsonify(tarea), 200
    return jsonify({"error": f"no se encontro esa tarea con id {id}", })

#endpoint -DELETE- para eliminar una tarea por su id
@app.delete("/eliminar-tarea/<int:id>")
def eliminar_tarea(id):
    #recorremos el array de tareas
    for tarea in tareas:
        #si coincide el id que ponemos por parametros con el que esta en el array, lo elimina de la lista
        if tarea["id"] == id:
            #metodo pop elimina por parametro que le pasemos
            tareas.remove(tarea)
            #retornamos un mensaje que fue una ejecucion con exito
            return jsonify(f"tarea con id {id} eliminado"), 200
    #retornamos un jsonify en caso que falle la peticion
    return jsonify({"error": "no se elimino ya que ese id no existe"}), 404



#endpoint -PUT- para actualizar una tarea buscando por su id
@app.put("/tarea/<int:id>")
def actualizar_tarea(id):
   #el metodo next sirve para poder convertir una lista en un iterador y solo recorrer ese elemento que coincida con la condicion que le pongamos, sin la necesidad de recorrerlos todos como lo hace el bucle fot, de esa manera se ahorra muchos procesos y tiempo de rendimiento
   tarea = next((t for t in tareas if t["id"] == id), {"error": "no existe tarea con ese id"})
   if not tarea:
    return jsonify({"error": "no hay tarea"}), 404
   
   #aca capturamos lo que el usuario nos escribo en el body
   data = request.json
   #actualizamos la lista de tareas con la data nueva
   tarea.update(data)
   #retornamos un json
   return jsonify(tarea), 200


if __name__ == "__main__":
    app.run(debug=True)