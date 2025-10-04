# auto.py
from Clases.Vehiculo import Vehiculo, USUARIO_SISTEMA, EventoHistorico
from datetime import datetime

# --- Clases de Apoyo para Eventos de Ocupación ---
class EventoOcupacion:
    """Clase para registrar un evento en eventos_ocupacion."""
    def __init__(self, accion: str, cantidad: int, ocupantes_antes: int, ocupantes_despues: int):
        self.fecha_hora = datetime.now()
        self.accion = accion # subir, bajar, vaciar, reconfigurar
        self.cantidad = cantidad
        self.ocupantes_antes = ocupantes_antes
        self.ocupantes_despues = ocupantes_despues

    def __str__(self):
        """Representación legible del evento de ocupación."""
        return (f"[{self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Acción: {self.accion} ({self.cantidad} p.) | "
                f"Ocupantes: {self.ocupantes_antes} -> {self.ocupantes_despues}")

# --- Clase Hija: Auto ---
class Auto(Vehiculo):
    """
    Extiende Vehiculo añadiendo gestión de asientos y ocupantes.
    """
    def __init__(self, patente: str, peso_kg: float, asientos_totales: int, 
                 sistema_retencion_infantil: str = "no", usuario: str = USUARIO_SISTEMA):
        
        # Llama al constructor de la clase base (Vehiculo)
        super().__init__(patente, peso_kg, usuario) 
        
        # Validaciones iniciales de Auto
        if asientos_totales < 1:
            raise ValueError("Los asientos totales deben ser 1 o más.")
            
        # Datos Adicionales de Auto
        self.__asientos_totales = asientos_totales
        self.__ocupantes_actuales = 0 # Inicia en 0 (Regla de negocio: no editable directamente)
        self.__sistema_retencion_infantil = sistema_retencion_infantil.lower()
        self.__eventos_ocupacion = []
        
        # Auditoría de creación extendida
        self._registrar_evento(usuario, "Creación Auto", "N/A", 
                               f"Asientos: {asientos_totales}, Retención Infantil: {sistema_retencion_infantil}")

    # --- Propiedades (Getters) de Auto ---
    @property
    def asientos_totales(self) -> int:
        return self.__asientos_totales

    @property
    def ocupantes_actuales(self) -> int:
        return self.__ocupantes_actuales
        
    @property
    def sistema_retencion_infantil(self) -> str:
        return self.__sistema_retencion_infantil

    @property
    def eventos_ocupacion(self) -> list:
        # Solo lectura
        return list(self.__eventos_ocupacion)

    # --- Métodos de Ocupación ---
    
    def _registrar_evento_ocupacion(self, accion: str, cantidad: int, antes: int, despues: int):
        """Método privado para añadir un evento de ocupación."""
        evento = EventoOcupacion(accion, cantidad, antes, despues)
        self.__eventos_ocupacion.append(evento)
        
    def subir_personas(self, n: int) -> bool:
        """Incrementa la ocupación. Valida límites y estado."""
        if self.estado == "inhabilitado":
            print(f"❌ Error: No se puede subir personas, el auto está inhabilitado ({self.patente}).")
            return False

        if n < 1:
            print("❌ Error: Debe subir al menos 1 persona.")
            return False
            
        nueva_ocupacion = self.__ocupantes_actuales + n
        if nueva_ocupacion > self.__asientos_totales:
            print(f"❌ Error: Capacidad excedida. Asientos libres: {self.asientos_libres}. Se intentó subir {n}.")
            return False

        # Aplica la Regla de Negocio
        ocupantes_antes = self.__ocupantes_actuales
        self.__ocupantes_actuales = nueva_ocupacion
        self._registrar_evento_ocupacion("subir", n, ocupantes_antes, self.__ocupantes_actuales)
        print(f"✅ Éxito: Subieron {n} personas. Ocupantes actuales: {self.__ocupantes_actuales}.")
        return True

    def bajar_personas(self, n: int) -> bool:
        """Decrementa la ocupación. Valida límites y estado."""
        if self.estado == "inhabilitado":
            print(f"❌ Error: No se puede bajar personas, el auto está inhabilitado ({self.patente}).")
            return False
            
        if n < 1:
            print("❌ Error: Debe bajar al menos 1 persona.")
            return False

        nueva_ocupacion = self.__ocupantes_actuales - n
        if nueva_ocupacion < 0:
            print(f"❌ Error: La ocupación no puede ser negativa. Ocupantes actuales: {self.__ocupantes_actuales}. Se intentó bajar {n}.")
            return False
            
        # Aplica la Regla de Negocio
        ocupantes_antes = self.__ocupantes_actuales
        self.__ocupantes_actuales = nueva_ocupacion
        self._registrar_evento_ocupacion("bajar", n, ocupantes_antes, self.__ocupantes_actuales)
        print(f"✅ Éxito: Bajaron {n} personas. Ocupantes actuales: {self.__ocupantes_actuales}.")
        return True

    def vaciar_auto(self, motivo: str, usuario: str = USUARIO_SISTEMA) -> bool:
        """Fuerza la ocupación a cero."""
        if self.__ocupantes_actuales == 0:
            print("ℹ️ Aviso: El auto ya está vacío.")
            return False
            
        ocupantes_antes = self.__ocupantes_actuales
        self.__ocupantes_actuales = 0
        self._registrar_evento_ocupacion("vaciar", ocupantes_antes, ocupantes_antes, 0)
        self._registrar_evento(usuario, "Vaciar Auto", 
                               f"{ocupantes_antes} ocupantes", 
                               f"0 ocupantes | Motivo: {motivo}")
        print(f"✅ Éxito: Auto vaciado. Motivo: {motivo}.")
        return True

    def reconfigurar_asientos(self, nuevo_total: int, motivo: str, usuario: str = USUARIO_SISTEMA) -> bool:
        """Cambia el total de asientos. Valida que sea >= 1 y >= ocupación actual."""
        if nuevo_total < 1:
            print("❌ Error: El nuevo total de asientos debe ser 1 o más.")
            return False
            
        if nuevo_total < self.__ocupantes_actuales:
            print(f"❌ Error: No se puede reducir a {nuevo_total} asientos, hay {self.__ocupantes_actuales} ocupantes.")
            return False
            
        if nuevo_total == self.__asientos_totales:
            print("ℹ️ Aviso: El total de asientos no cambió.")
            return False
            
        asientos_antes = self.__asientos_totales
        self.__asientos_totales = nuevo_total
        
        self._registrar_evento(usuario, "Reconfigurar Asientos", 
                               f"{asientos_antes} asientos", 
                               f"{nuevo_total} asientos | Motivo: {motivo}")
        self._registrar_evento_ocupacion("reconfigurar", nuevo_total, self.__ocupantes_actuales, self.__ocupantes_actuales)
        print(f"✅ Éxito: Asientos reconfigurados a {nuevo_total}. Motivo: {motivo}.")
        return True

    # --- Datos Derivados/Reportables ---

    @property
    def asientos_libres(self) -> int:
        """Calcula los asientos disponibles."""
        return self.__asientos_totales - self.__ocupantes_actuales

    def tasa_ocupacion(self) -> str:
        """Calcula la tasa de ocupación en porcentaje."""
        if self.__asientos_totales == 0:
            return "0.00%"
        tasa = (self.__ocupantes_actuales / self.__asientos_totales) * 100
        return f"{tasa:.2f}%"

    def consultar_ocupacion(self) -> dict:
        """Devuelve los datos de ocupación y derivados."""
        return {
            "Ocupantes Actuales": self.ocupantes_actuales,
            "Asientos Totales": self.asientos_totales,
            "Asientos Libres": self.asientos_libres,
            "Tasa de Ocupación": self.tasa_ocupacion(),
            "Sistema Retención Infantil": self.sistema_retencion_infantil.upper()
        }

    def __str__(self):
        return (f"Auto ({self.patente}) - Peso: {self.peso_kg} kg, Estado: {self.estado}, "
                f"Ocupantes: {self.ocupantes_actuales}/{self.asientos_totales}")