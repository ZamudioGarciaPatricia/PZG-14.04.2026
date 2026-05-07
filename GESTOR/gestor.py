"""
Aplicación de ejemplo: Gestor de tareas con MongoDB y Python usando las funcionalidades que nos enseño el profe y el archivode moodle
adaptandolo poco a poco
"""

from pymongo import MongoClient
from datetime import datetime

class GestorTareas:
    def __init__(self, uri="mongodb://localhost:27017/"): 
        self.cliente = MongoClient(uri, serverSelectionTimeoutMS=2000)
        self.db = self.cliente['lula']
        self.usuarios = self.db['usuarios']
        self.usuarios.create_index("email", unique=True)

    def crear_usuario(self, user, email, secreto):
        try:
            self.usuarios.insert_one({
                "user": user,
                "email": email,
                "secreto": secreto,
                "fecha_registro": datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error al crear: {e}")
            return False
        
            tarea = {
            "usuario_id": ObjectId(usuario_id),
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": "pendiente",
            "fecha_creacion": datetime.now(),
            "fecha_limite": fecha_limite or datetime.now() + timedelta(days=7),
            "completada": False,
            "etiquetas": []
        }
        
        resultado = self.tareas.insert_one(tarea)
        return str(resultado.inserted_id)
    def obtener_tareas_usuario(self, usuario_id: str, estado: Optional[str] = None) -> List[Dict]:
        """Obtener tareas de un usuario, opcionalmente filtradas por estado"""
        filtro = {"usuario_id": ObjectId(usuario_id)}
        if estado:
        filtro["estado"] = estado
        
        tareas = self.tareas.find(filtro).sort("fecha_creacion", -1)
        resultado = []
        for t in tareas:
            t['_id'] = str(t['_id'])
            t['usuario_id'] = str(t['usuario_id'])
            resultado.append(t)
        return resultado
    filtro["estado"] = estado
    tareas = self.tareas.find(filtro).sort("fecha_creacion", -1)
    resultado = []
    for t in tareas:
        t['_id'] = str(t['_id'])
    º           t['usuario_id'] = str(t['usuario_id'])
        resultado.append(t)
        return resultado


    def obtener_usuario_por_email(self, email):
        return self.usuarios.find_one({"email": email})