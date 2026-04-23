"""
Aplicación de ejemplo: Gestor de tareas con MongoDB y Python usando las funcionalidades que nos enseño el profe
"""

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import os

class GestorTareas:
    def __init__(self, uri: str = 'mongodb://localhost:27017/'):
        """Inicializar conexión a MongoDB"""
        try:
            self.cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.cliente.admin.command('ping')
            self.db = self.cliente['gestor_tareas']
            self.tareas = self.db['tareas']
            self.usuarios = self.db['usuarios']
            # Crear índices necesarios
            self._crear_indices()
            print("✅ Conectado a MongoDB")
        except ConnectionFailure:
            print("❌ Error: No se pudo conectar a MongoDB")
            raise
    
    def _crear_indices(self):
        """Crear índices para mejorar rendimiento"""
        self.usuarios.create_index("email", unique=True)
        self.tareas.create_index([("user", 1), ("fecha_creacion", -1)])
        self.tareas.create_index("estado")
    
    def crear_usuario(self, nombre: str, email: str) -> Optional[str]:
        """Crear un nuevo usuario"""
        try:
            resultado = self.usuarios.insert_one({
                "nombre": nombre,
                "email": email,
                "username": user,
                "fecha_registro": datetime.now(),
                "activo": True,
                
            })
            return str(resultado.inserted_id)
        except DuplicateKeyError:
            print(f"❌ Error: El email {email} ya está registrado")
            return None
    # ESTO AUN NO FUNCIONA PROX 
    def obtener_usuario(self, usuario_id: str) -> Optional[Dict]:
        """Obtener usuario por ID"""
        try:
            usuario = self.usuarios.find_one({"_id": ObjectId(usuario_id)})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        
        # Ejemplo de uso
def ejemplo_uso():
    # Inicializar gestor
    gestor = GestorTareas()
    
    # Crear usuario
    usuario_id = gestor.crear_usuario("Ana García", "ana@email.com")
    print(f"Usuario creado con ID: {usuario_id}")
    
    if usuario_id:
        # Crear tareas
        tarea1 = gestor.crear_tarea(
            usuario_id, 
            "Aprender MongoDB", 
            "Completar tutorial de PyMongo",
            datetime.now() + timedelta(days=3)
        )
        print(f"Tarea creada: {tarea1}")
        
        tarea2 = gestor.crear_tarea(
            usuario_id,
            "Hacer ejercicio",
            "Ir al gimnasio 3 veces esta semana"
        )
        
        # Agregar etiqueta
        gestor.agregar_etiqueta(tarea1, "programación")
        gestor.agregar_etiqueta(tarea1, "estudio")
        
        # Listar tareas
        tareas = gestor.obtener_tareas_usuario(usuario_id)
        print(f"\nTareas de {usuario_id}:")
        for t in tareas:
            print(f"  - {t['titulo']} [{t['estado']}]")
        
        # Actualizar estado
        gestor.actualizar_estado_tarea(tarea1, "en_progreso")
        
        # Estadísticas
        stats = gestor.estadisticas_usuario(usuario_id)
        print(f"\nEstadísticas: {stats}")
        
        # Tareas urgentes
        urgentes = gestor.tareas_urgentes(72)
        print(f"\nTareas urgentes próximos 3 días: {len(urgentes)}")
    gestor.cerrar_conexion()

if __name__ == "__main__":
    ejemplo_uso()