# Modelo 2 — Planeta
# Extiende el modelo de Cuerpo Celeste agregando radio y distancia al sol..
# Datos adicionales
    # radio_km (número > 0).
    # distancia_sol_km (número > 0).
# Operaciones.
    # actualizar_radio(nuevo_radio) → valida > 0.
    # actualizar_distancia_sol(nueva_distancia) → valida > 0.
    # calcular_densidad() → densidad = masa / volumen (volumen ≈ 4/3 × π × radio³).
    # comparar_distancia(otro_planeta) → indica cuál está más cerca del sol.
# Reglas de negocio.
    # El radio y la distancia al sol deben ser mayores que cero.
    # Ningún campo puede alterarse directamente; solo mediante operaciones.
    # Comparaciones solo son válidas entre objetos del tipo Planeta.
# Datos derivados/reportables
    # Densidad (kg/km³).
    # Demanda de energía teórica: podría calcularse más adelante a partir de la masa y la distancia (opcional como extensión).
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
import math
from Clases.CuerposCelestes import ObjetoCeleste 
from datetime import datetime

class Planeta(ObjetoCeleste):

    def __init__(self, nombre: str, masa_kg: float, radio_km: float, distancia_sol_km: float):
        
        # 1. Validación de atributos específicos
        if radio_km <= 0:
            raise ValueError("El radio debe ser un número positivo (mayor a 0 km).")
        
        if distancia_sol_km <= 0:
            raise ValueError("La distancia al sol debe ser un número positivo (mayor a 0 km).")

        # 2. Inicialización de la clase base (ObjetoCeleste)
        super().__init__(nombre, masa_kg)
        
        # 3. Inicialización de atributos de Planeta (Encapsulados)
        self.__radio_km = radio_km
        self.__distancia_sol_km = distancia_sol_km
        
        # Registro inicial en el historial general (del padre)
        self._ObjetoCeleste__registrar_evento("radio_km", None, radio_km)
        self._ObjetoCeleste__registrar_evento("distancia_sol_km", None, distancia_sol_km)
        print(f"Planeta '{self.nombre}' inicializado con radio {radio_km} km y a {distancia_sol_km} km del sol.")

    
    """ Getters-----------------------------------------------------------------------------------------------------------------------------------------------------------"""
    @property
    def radio_km(self) -> float:
        return self.__radio_km

    @property
    def distancia_sol_km(self) -> float:
        return self.__distancia_sol_km
        
    @property
    def volumen_km3(self) -> float:
        # Volumen (4/3 * pi * r^3)
        return (4/3) * math.pi * (self.__radio_km ** 3)
        
    @property
    def densidad_kg_km3(self) -> float:
        # Dato Derivado: Densidad (masa / volumen)
        volumen = self.volumen_km3
        if volumen == 0:
            return 0.0
        return self.masa_kg / volumen

    """ Métodos-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def actualizar_radio(self, nuevo_radio: float):
        if nuevo_radio <= 0:
            raise ValueError("El nuevo radio debe ser un número positivo (mayor a 0 km).")
            
        valor_anterior = self.__radio_km
        self.__radio_km = nuevo_radio
        
        # Uso del name mangling del padre para registrar el evento
        self._ObjetoCeleste__registrar_evento("radio_km", valor_anterior, self.__radio_km)
        print(f"Radio de {self.nombre} actualizado de {valor_anterior} km a {self.__radio_km} km.")

    def actualizar_distancia_sol(self, nueva_distancia: float):
        if nueva_distancia <= 0:
            raise ValueError("La nueva distancia al sol debe ser un número positivo (mayor a 0 km).")
            
        valor_anterior = self.__distancia_sol_km
        self.__distancia_sol_km = nueva_distancia
        
        # Uso del name mangling del padre para registrar el evento
        self._ObjetoCeleste__registrar_evento("distancia_sol_km", valor_anterior, self.__distancia_sol_km)
        print(f"Distancia al sol de {self.nombre} actualizada de {valor_anterior} km a {self.__distancia_sol_km} km.")

    def calcular_densidad(self) -> float:
        """Calcula y devuelve la densidad (masa / volumen)."""
        return self.densidad_kg_km3
        
    def comparar_distancia(self, otro_planeta):
        """Indica cuál de los dos planetas está más cerca del sol."""
        
        # Regla de Negocio: Comparaciones solo son válidas entre objetos del tipo Planeta
        if not isinstance(otro_planeta, Planeta):
            raise TypeError("La comparación de distancia solo es válida entre objetos de tipo Planeta.")
            
        mi_distancia = self.distancia_sol_km
        otra_distancia = otro_planeta.distancia_