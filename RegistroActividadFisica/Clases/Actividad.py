# actividad.py

from datetime import datetime
import uuid

class Actividad:
    """
    Modelo base para registrar una actividad física.
    Mantiene un historial de cambios para la duración.
    """
    def __init__(self, nombre: str, duracion_min: int):
        # Generar un ID único al crear la actividad
        self._id_actividad = str(uuid.uuid4())
        
        # Validar el nombre (no vacío)
        if not nombre.strip():
            raise ValueError("El nombre de la actividad no puede estar vacío.")
        self._nombre = nombre
        
        # Validar la duración inicial (>= 1)
        if duracion_min < 1:
            raise ValueError("La duración mínima aceptada es 1 minuto.")
        self._duracion_min = duracion_min
        
        # Historial de eventos (solo lectura)
        self._historial_eventos = []
        self._registrar_evento("creacion", None, self._duracion_min)

    # --- Propiedades de Solo Lectura (Getters) ---
    @property
    def id_actividad(self) -> str:
        return self._id_actividad

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def duracion_min(self) -> int:
        return self._duracion_min

    @property
    def historial_eventos(self) -> list:
        # Devolvemos una copia para evitar modificación directa de la lista
        return list(self._historial_eventos)

    # --- Operaciones y Métodos Internos ---
    def _registrar_evento(self, campo: str, valor_anterior, valor_nuevo):
        """Método interno para registrar un cambio en el historial."""
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo_modificado": campo,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo
        }
        self._historial_eventos.append(evento)

    def actualizar_nombre(self, nuevo_nombre: str):
        """Actualiza el nombre, validando que no esté vacío."""
        if not nuevo_nombre.strip():
            raise ValueError("El nuevo nombre no puede estar vacío.")
        
        valor_anterior = self._nombre
        self._nombre = nuevo_nombre
        self._registrar_evento("nombre", valor_anterior, self._nombre)

    def actualizar_duracion(self, nueva_duracion: int):
        """Actualiza la duración, validando que sea >= 1."""
        if nueva_duracion < 1:
            raise ValueError("La duración mínima aceptada es 1 minuto.")
        
        valor_anterior = self._duracion_min
        self._duracion_min = nueva_duracion
        self._registrar_evento("duracion_min", valor_anterior, self._duracion_min)

    def __str__(self):
        return f"Actividad(ID: {self._id_actividad[:4]}..., Nombre: {self._nombre}, Duración: {self._duracion_min} min)"

# Ejemplo de implementación simple (aunque las pruebas van en main.py)
if __name__ == "__main__":
    try:
        act1 = Actividad("Caminata", 30)
        print(act1)
        act1.actualizar_duracion(45)
        print(f"Nueva duración: {act1.duracion_min}")
        print("Historial de eventos:", act1.historial_eventos)
    except ValueError as e:
        print(f"Error: {e}")