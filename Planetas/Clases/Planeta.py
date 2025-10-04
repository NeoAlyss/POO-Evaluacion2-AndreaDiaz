# planeta.py

import math
from Clases.CuerposCelestes import CuerpoCeleste, ValidacionError

class Planeta(CuerpoCeleste):
    """
    Extiende CuerpoCeleste para incluir propiedades específicas de un planeta.
    """
    
    def __init__(self, nombre: str, masa_kg: float, radio_km: float, distancia_sol_km: float):
        """
        Inicializa un Planeta, llamando al constructor de la clase base.
        """
        # Inicializa CuerpoCeleste: id, nombre, masa e historial
        super().__init__(nombre, masa_kg)
        
        # Atributos adicionales
        self._radio_km = None
        self._distancia_sol_km = None
        
        # Inicialización con las operaciones para asegurar validación
        self.actualizar_radio(radio_km)
        self.actualizar_distancia_sol(distancia_sol_km)
    
    # --- Propiedades de Solo Lectura (Getters) ---

    @property
    def radio_km(self) -> float:
        """Devuelve el radio actual en km."""
        return self._radio_km

    @property
    def distancia_sol_km(self) -> float:
        """Devuelve la distancia actual al Sol en km."""
        return self._distancia_sol_km
    
    # --- Operaciones de Modificación con Validación y Registro ---
    
    def actualizar_radio(self, nuevo_radio: float):
        """
        Actualiza el radio, validando que sea mayor que cero.
        """
        if nuevo_radio <= 0:
            raise ValidacionError("El radio debe ser un número positivo (mayor que 0) en km.")
        
        valor_anterior = self._radio_km
        if valor_anterior is not None and valor_anterior != nuevo_radio:
            self._registrar_evento("radio_km", valor_anterior, nuevo_radio)
            
        self._radio_km = nuevo_radio

    def actualizar_distancia_sol(self, nueva_distancia: float):
        """
        Actualiza la distancia al Sol, validando que sea mayor que cero.
        """
        if nueva_distancia <= 0:
            raise ValidacionError("La distancia al Sol debe ser un número positivo (mayor que 0) en km.")
        
        valor_anterior = self._distancia_sol_km
        if valor_anterior is not None and valor_anterior != nueva_distancia:
            self._registrar_evento("distancia_sol_km", valor_anterior, nueva_distancia)
            
        self._distancia_sol_km = nueva_distancia
        
    # --- Operaciones Específicas de Planeta ---

    def calcular_densidad(self) -> float:
        """
        Calcula la densidad aproximada (masa / volumen).
        Volumen = 4/3 * pi * radio^3.
        Resultado en kg/km³.
        """
        # Convertimos el radio a metros para un cálculo más estándar, 
        # pero la consigna pide kg/km³, así que usamos el radio en km
        radio_cubico = self._radio_km ** 3
        # Volumen de una esfera (aproximación)
        volumen_km3 = (4/3) * math.pi * radio_cubico
        
        if volumen_km3 == 0:
            # Esto no debería pasar si la validación de radio es correcta
            return 0.0
            
        densidad_kg_por_km3 = self.masa_kg / volumen_km3
        return densidad_kg_por_km3

    def comparar_distancia(self, otro_planeta: 'Planeta') -> str:
        """
        Compara la distancia al Sol con la de otro Planeta.
        Valida que el otro objeto sea de tipo Planeta.
        """
        if not isinstance(otro_planeta, Planeta):
            raise TypeError("La comparación de distancia solo es válida entre objetos de tipo Planeta.")
            
        dist_self = self.distancia_sol_km
        dist_otro = otro_planeta.distancia_sol_km
        
        if dist_self < dist_otro:
            return f"{self.nombre} está más cerca del Sol que {otro_planeta.nombre} ({dist_self:_.0f} km vs {dist_otro:_.0f} km)."
        elif dist_self > dist_otro:
            return f"{otro_planeta.nombre} está más cerca del Sol que {self.nombre} ({dist_otro:_.0f} km vs {dist_self:_.0f} km)."
        else:
            return f"{self.nombre} y {otro_planeta.nombre} están a la misma distancia del Sol ({dist_self:_.0f} km)."

    # --- Sobreescritura de Método de la Clase Base ---

    def consultar_ficha(self) -> str:
        """
        Sobreescribe la ficha base añadiendo los datos de Planeta.
        """
        ficha_base = super().consultar_ficha()
        
        # Añadir datos específicos de Planeta
        ficha_planeta = "\n  --- Datos de Planeta ---\n"
        ficha_planeta += f"  Radio (km): {self._radio_km:_.0f}\n"
        ficha_planeta += f"  Distancia al Sol (km): {self._distancia_sol_km:_.0f}\n"
        
        try:
            densidad = self.calcular_densidad()
            ficha_planeta += f"  Densidad Aprox (kg/km³): {densidad:_.2e}\n"
        except ValidacionError:
            ficha_planeta += "  Densidad Aprox (kg/km³): N/A (Datos incompletos/inválidos)\n"
            
        return ficha_base + ficha_planeta

    def __str__(self):
        """Representación legible del objeto."""
        return f"Planeta(ID={self.id_celeste}, Nombre='{self.nombre}', Masa={self.masa_kg:_.2e} kg, Radio={self.radio_km:_.0f} km)"