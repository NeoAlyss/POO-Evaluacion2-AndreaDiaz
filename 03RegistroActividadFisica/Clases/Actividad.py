# Datos mínimos
    # id_actividad (único). OK
    # nombre (cadena no vacía). OK
    # duracion_min (entero ≥ 1). OK
    # historial_eventos (solo lectura: lista de cambios con fecha, campo modificado, valor anterior/nuevo).
# Operaciones
    # actualizar_nombre(nuevo_nombre) → valida no vacío.
    # actualizar_duracion(nueva_duracion) → valida ≥ 1, registra cambio en historial.
# Reglas de negocio
    # La duración mínima aceptada es 1 minuto.
    # Ningún dato puede alterarse directamente; todo cambio
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

from datetime import datetime
import uuid

class Actividad:

    def __init__(self, nombre: str, duracion_min: int):
        self.__id_actividad = str(uuid.uuid4()) # Con uuid4 generamos un ID único de forma automática
        
        if not nombre.strip(): #actividad no puede estar vacía según regla de negocio
            raise ValueError("El nombre de la actividad no puede estar vacío.")
        self.__nombre = nombre
        
        if duracion_min < 1: #validación de duracion mínima según regla de negocio
            raise ValueError("La duración mínima aceptada es 1 minuto.")
        self.__duracion_min = duracion_min
        
        self.__historial_eventos = []
        self.__registrar_evento("creacion", None, self.__duracion_min)
        print(f"Actividad '{self.__nombre}' creada con duración mínima de {self.__duracion_min} minutos.")

    """ Getters----------------------------------------------------------------------------------------------------------------------------------------------------------"""
    @property
    def id_actividad(self) -> str:
        return self.__id_actividad

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def duracion_min(self) -> int:
        return self.__duracion_min

    @property
    def historial_eventos(self) -> list:
        # Devolvemos una copia 
        return list(self.__historial_eventos)
    
    """ Métodos----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def __registrar_evento(self, campo: str, valor_anterior, valor_nuevo):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo_modificado": campo,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo
        }
        self.__historial_eventos.append(evento)

    def actualizar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre.strip(): #recordar que strip() elimina espacios en blanco, esto evita que se ingrese solo espacios y asi cumple con la regla de negocio de no vacío
            raise ValueError("El nuevo nombre no puede estar vacío.")
        
        valor_anterior = self.__nombre
        self.__nombre = nuevo_nombre
        self.__registrar_evento("nombre", valor_anterior, self.__nombre)
        print(f"Nombre actualizado de '{valor_anterior}' a '{self.__nombre}'.")

    def actualizar_duracion(self, nueva_duracion: int):
        if nueva_duracion < 1:
            raise ValueError("La duración mínima aceptada es 1 minuto.")
        
        valor_anterior = self.__duracion_min
        self.__duracion_min = nueva_duracion
        self.__registrar_evento("duracion_min", valor_anterior, self.__duracion_min)
        print(f"Duración mínima actualizada de {valor_anterior} a {self.__duracion_min} minutos.")
    
    def __str__(self):
        return f"Actividad {self.__nombre} (ID: {self.__id_actividad}, Nombre: {self.__nombre}, Duraciónmínima: {self.__duracion_min} minutos)"