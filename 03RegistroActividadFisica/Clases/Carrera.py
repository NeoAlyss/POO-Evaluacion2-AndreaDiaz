# Incluye todo lo del Modelo 1 y añade control de distancia y cálculo de ritmo.
# Datos adicionales
    # distancia_km (decimal > 0). OK
    # eventos_registro (solo lectura: fecha, distancia registrada, duración acumulada). OK
# Operaciones
    # registrar_distancia(nueva_distancia) → valida > 0.
    # calcular_ritmo() → devuelve minutos por km (duracion_min / distancia_km).
# Reglas de negocio
    # La distancia debe ser positiva.
    # Ritmo solo puede calcularse si existe una distancia registrada válida.
    # Ni la distancia ni la duración pueden editarse directamente; solo mediante operaciones.
    # Cada registro de distancia queda en eventos_registro con fecha/hora.

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

from Clases.Actividad import Actividad
from datetime import datetime

class Carrera(Actividad):

    def __init__(self, nombre: str, duracion_min: int, distancia_km: float):
        super().__init__(nombre, duracion_min)
        
        if distancia_km <= 0:
            raise Exception("La distancia debe ser positiva (mayor que 0).")
        
        self._distancia_km = distancia_km #esto hace que la distancia no pueda ser modificada directamente desde fuera de la clase
        
        self._eventos_registro = []

        self._registrar_distancia_interna(distancia_km, duracion_min)
        print(f"Carrera '{self.nombre}' creada con distancia de {self._distancia_km} km y duración mínima de {self.duracion_min} minutos.")

    """ Getters----------------------------------------------------------------------------------------------------------------------------------------------------------"""
    @property
    def distancia_km(self) -> float:
        return self._distancia_km
    
    @property
    def eventos_registro(self) -> list:
        # Devolvemos una copia
        return list(self._eventos_registro)
    
    """ Métodos----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def actualizar_duracion(self, nueva_duracion: int):
        """
        Sobreescribe el método para actualizar la duración.
        Además de registrar en historial_eventos, registra en eventos_registro.
        """
        super().actualizar_duracion(nueva_duracion)
        # Registramos el evento en eventos_registro también
        self._registrar_distancia_interna(self._distancia_km, nueva_duracion)



    
    def _registrar_distancia_interna(self, distancia: float, duracion: int):
        """Método interno para registrar un evento de distancia/duración."""
        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "distancia_registrada": distancia,
            "duracion_acumulada": duracion
        }
        self._eventos_registro.append(registro)

    def registrar_distancia(self, nueva_distancia: float):
        """
        Permite 'registrar' o 'cambiar' la distancia.
        (Aunque el enunciado lo pide como 'registrar', en este contexto
        se asume que es el valor final de la carrera).
        """
        if nueva_distancia <= 0:
            raise ValueError("La nueva distancia debe ser positiva.")
            
        valor_anterior = self._distancia_km
        self._distancia_km = nueva_distancia
        
        # Se registra como un evento en el historial de la Actividad (para la distancia)
        self._registrar_evento("distancia_km", valor_anterior, self._distancia_km)
        
        # Se registra el nuevo punto de control en eventos_registro
        self._registrar_distancia_interna(self._distancia_km, self.duracion_min)
        

    def calcular_ritmo(self) -> float:
        """Calcula el ritmo en minutos por kilómetro (duracion_min / distancia_km)."""
        if self._distancia_km <= 0:
            raise ValueError("No se puede calcular el ritmo sin una distancia registrada válida (> 0).")
        
        # El ritmo se calcula con la duración actual y la distancia registrada.
        return round(self.duracion_min / self._distancia_km, 2) # Redondeo a 2 decimales para claridad

    def __str__(self):
        return (f"Carrera(ID: {self.id_actividad[:4]}..., Nombre: {self.nombre}, "
                f"Duración: {self.duracion_min} min, Distancia: {self.distancia_km} km)")

# Ejemplo de implementación simple (aunque las pruebas van en main.py)
if __name__ == "__main__":
    try:
        carr = Carrera("Maratón", 240, 42.195)
        print(carr)
        print(f"Ritmo: {carr.calcular_ritmo()} min/km")
    except ValueError as e:
        print(f"Error: {e}")