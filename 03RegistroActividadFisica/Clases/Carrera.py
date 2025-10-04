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
            raise Exception("La distancia debe ser positiva (mayor que 0)")
        
        self.__distancia_km = distancia_km #esto hace que la distancia no pueda ser modificada directamente desde fuera de la clase
        
        self.__eventos_registro = []

        self._registrar_distancia_interna(distancia_km, duracion_min)
        print(f"Carrera '{self.nombre}' creada con distancia de {self.distancia_km} km y duración mínima de {self.duracion_min} minutos")

    """ Getters----------------------------------------------------------------------------------------------------------------------------------------------------------"""
    @property
    def distancia_km(self) -> float:
        return self.__distancia_km
    
    @property
    def eventos_registro(self) -> list:
        # Devolvemos una copia
        return list(self.__eventos_registro)
    
    """ Métodos----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def actualizar_duracion(self, nueva_duracion: int):
        super().actualizar_duracion(nueva_duracion) # Llama al método padre para validar y registrar el cambio
        # Registra el nuevo punto de control en eventos_registro con la distancia actual
        self._registrar_distancia_interna(self.__distancia_km, nueva_duracion)
        print(f"Duración actualizada a {nueva_duracion} minutos para la carrera {self.nombre}")
    
    def _registrar_distancia_interna(self, distancia: float, duracion: int):
        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "distancia_registrada": distancia,
            "duracion_acumulada": duracion
        }
        self.__eventos_registro.append(registro)

    def registrar_distancia(self, nueva_distancia: float):
        if nueva_distancia <= 0:
            raise ValueError("La nueva distancia debe ser positiva")
            
        valor_anterior = self.__distancia_km
        self.__distancia_km = nueva_distancia
        print(f"Distancia actualizada de {valor_anterior} km a {self.__distancia_km} km para la carrera {self.nombre}")
        
        # Se registra en el historial de la actividad el cambio de distancia
        self._registrar_evento("distancia_km", valor_anterior, self.__distancia_km)
        
        # Se agrega un nuevo registro en eventos_registro con la nueva distancia y la duración actual
        self._registrar_distancia_interna(self.__distancia_km, self.duracion_min)
        

    def calcular_ritmo(self) -> float:
        if self.__distancia_km <= 0:
            raise Exception("No se puede calcular el ritmo sin una distancia registrada válida (> 0).")
        ritmo = self.duracion_min / self.__distancia_km
        return round(ritmo, 2)

    def __str__(self):
        return (f"Carrera(ID: {self.id_actividad[:4]}..., Nombre: {self.nombre}, "
                f"Duración: {self.duracion_min} min, Distancia: {self.distancia_km} km)")
