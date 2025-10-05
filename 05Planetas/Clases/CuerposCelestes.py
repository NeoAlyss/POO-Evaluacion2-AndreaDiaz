# Datos mínimos.
    # id_celeste (único).
    # nombre (cadena no vacía).
    # masa_kg (número > 0).
    # historial_eventos (solo lectura: fecha/hora, campo modificado, valor anterior/nuevo).
# Operaciones.
    # actualizar_nombre(nuevo_nombre) → valida no vacío.
    # actualizar_masa(nueva_masa) → valida > 0; registra en historial.
    # consultar_ficha() → devuelve datos actuales más últimos eventos.
    # Reglas de negocio.
    # La masa nunca puede ser ≤ 0.
    # El nombre no puede quedar vacío.
    # No se permiten cambios directos; todo ajuste debe pasar por operaciones con validación.
    # Cada actualización queda registrada en el historial.
# Datos derivados/reportable
    # Fecha de última actualización de masa.
    # Número de modificaciones realizadas.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from datetime import datetime
import uuid

class ObjetoCeleste:

    def __init__(self, nombre: str, masa_kg: float):
        
        #Validaciones
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        
        if masa_kg <= 0:
            raise ValueError("La masa debe ser un número positivo (mayor a 0 kg).")

        #atributos
        self.__id_celeste = str(uuid.uuid4())
        self.__nombre = nombre.strip()
        self.__masa_kg = masa_kg
        self.__historial_eventos = []
        self.__fecha_ultima_actualizacion = datetime.now()
        self.__numero_modificaciones = 0

        #registro de evento de creación
        self.__registrar_evento("creacion", None, self.__masa_kg)
        print(f"Objeto Celeste '{self.__nombre}' (ID: {self.__id_celeste[:4]}...) creado con masa de {self.__masa_kg} kg.")

    
    """ Registro de vento--------------------------------------------------------------------------------------------------------------------------------------------------"""

    def __registrar_evento(self, campo: str, valor_anterior, valor_nuevo):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo_modificado": campo,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo
        }
        self.__historial_eventos.append(evento)
        self.__numero_modificaciones += 1
    
    
    """ Getters--------------------------------------------------------------------------------------------------------------------------------------------------"""

    @property
    def id_celeste(self) -> str:
        return self.__id_celeste

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def masa_kg(self) -> float:
        return self.__masa_kg

    @property
    def historial_eventos(self) -> list:
        # Devuelve una copia para mantener el encapsulamiento
        return list(self.__historial_eventos)

    @property
    def fecha_ultima_actualizacion(self) -> datetime:
        return self.__fecha_ultima_actualizacion
        
    @property
    def numero_modificaciones(self) -> int:
        return self.__numero_modificaciones

    """ Métodos--------------------------------------------------------------------------------------------------------------------------------------------------"""

    def actualizar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("El nuevo nombre no puede estar vacío.")
        
        valor_anterior = self.__nombre
        self.__nombre = nuevo_nombre.strip()
        
        self.__registrar_evento("nombre", valor_anterior, self.__nombre)
        print(f"Nombre actualizado de '{valor_anterior}' a '{self.__nombre}'.")

    def actualizar_masa(self, nueva_masa: float):
        if nueva_masa <= 0:
            raise ValueError("La nueva masa debe ser un número positivo (mayor a 0 kg).")
            
        valor_anterior = self.__masa_kg
        self.__masa_kg = nueva_masa
        self.__fecha_ultima_actualizacion = datetime.now()
        
        self.__registrar_evento("masa_kg", valor_anterior, self.__masa_kg)
        print(f"Masa actualizada de {valor_anterior} kg a {self.__masa_kg} kg.")

    def consultar_ficha(self):
        """Devuelve los datos actuales del objeto y el resumen de auditoría."""
        return {
            "ID Celeste": self.__id_celeste,
            "Nombre": self.__nombre,
            "Masa Actual (kg)": self.__masa_kg,
            "Última Modificación": self.fecha_ultima_actualizacion.strftime("%Y-%m-%d %H:%M:%S"),
            "Total Modificaciones": self.numero_modificaciones,
            "Último Evento": self.__historial_eventos[-1] if self.__historial_eventos else "N/A"
        }

    def __str__(self):
        return (f"ObjetoCeleste(Nombre: {self.__nombre}, Masa: {self.__masa_kg} kg, "
                f"Modificaciones: {self.numero_modificaciones}, Última Act.: {self.fecha_ultima_actualizacion.strftime('%Y-%m-%d')})")