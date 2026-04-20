
# 🚀 Flask Tareas  API

Esta es una API REST desarrollada con **Python** y **Flask** para la gestión de datos de tareas. El proyecto demuestra cómo realizar operaciones CRUD (Create, Read, Update, Delete) utilizando una lista en memoria como base de datos de prueba.

---

## 🛠️ Tecnologías utilizadas

* **Python 3.x**
* **Flask**: Micro-framework para el desarrollo web.
* **Postman/Insomnia**: Recomendados para testear los endpoints.

---

## 📦 Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Bruno844/flask-python-devops.git]
    cd flask-python-devops
    ```

2.  **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```
3. **Activamos nuestro entorno virtual**
    ```bash
    .\venv\Scripts\activate
    ```

4.  **Instalar dependencias:**
    una vez activado nuestro entorno virtual,debemos instalar las dependencias que estan en el archivo **requirements.txt**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ejecutar la aplicación:**
    ```bash
    python app.py
    o tambien
    flask --app nombre_del_archivo.py run --debug
    ```
    La API estará disponible en `http://127.0.0.1:5000`.

---

## 🛣️ Endpoints de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** | `/tareas` | Obtiene la lista completa de tareas. |
| **GET** | `/tarea/<id>` | Obtiene una tarea específica por id. |
| **POST** | `/nueva-tarea` | Crea un nueva tarea. |
| **PUT** | `/tarea/<id>` | Actualiza los datos de una tarea existente. |
| **DELETE** | `/tarea/<id>` | Elimina una tarea de la lista. |

### Ejemplos de uso

#### Obtener un tarea por id (GET)
**URL:** `/tarea/1`  
**Respuesta:**
```json
{
  "response": {
    "id": 1,
    "titulo": "tarea 1",
    "completada": false
  }
}
