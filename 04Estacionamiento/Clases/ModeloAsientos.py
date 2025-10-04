# Incluye todo lo del Modelo A y añade administración de asientos y ocupantes.Regla: el precio final no puede ser negativo.
# Datos adicionales
    # asientos_totales (entero ≥ 1).
    # ocupantes_actuales (entero ≥ 0; no editable directamente).
    # sistema_retencion_infantil ∈ {si, no} (opcional, por políticas de seguridad).
    # eventos_ocupacion (solo lectura: fecha/hora, acción, cantidad, ocupantes_antes/después).
# Operaciones
    # subir_personas(n) → incrementa ocupación; valida límites.
    # bajar_personas(n) → decrementa ocupación; valida que no quede negativa.
    # reconfigurar_asientos(nuevo_total, motivo) → solo con ocupantes_actuales ≤ nuevo_total y nuevo_total ≥ 1; registra en historial.
    # vaciar_auto(motivo) → fuerza ocupantes_actuales = 0; registra en eventos.
    # consultar_ocupacion() → ocupantes actuales, asientos libres y tasa de ocupación.Regla: volumen y concentración solo cambian mediante la operación de dilución.
# Reglas de negocio
    # 0 ≤ ocupantes_actuales ≤ asientos_totales siempre.
    # subir_personas(n) requiere n ≥ 1 y que ocupantes_actuales + n ≤ asientos_totales.
    # bajar_personas(n) requiere n ≥ 1 y que ocupantes_actuales - n ≥ 0.
    # No se puede subir_personas ni bajar_personas si el vehículo está inhabilitado.
    # ocupantes_actuales no puede ser modificado directamente; solo mediante operaciones.
    # Todo cambio de ocupación genera entrada en eventos_ocupacion.
    # Si reconfigurar_asientos reduce asientos por debajo de la ocupación actual, debe rechazarse.
        # Políticas opcionales (si el sistema las define):
             # Si sistema_retencion_infantil = no, prohibir subir_personas(n) cuando se identifique pasajero menor de edad (si se modela), o registrar advertencia en eventos.
# Datos derivados/reportables
    # Asientos libres = asientos_totales - ocupantes_actuales.
    # Tasa de ocupación (%) = ocupantes_actuales / asientos_totales × 100.
    # Número de eventos de subida/bajada en un rango de fechas.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from datetime import datetime
from Clases.Vehiculo import Vehiculo # Asumiendo que la clase Vehiculo está en Clases/Vehiculo.py

class ModeloAsientos(Vehiculo):

    def __init__(self, patente: str, peso_kg: float, asientos_totales: int, usuario: str = "Sistema", sistema_retencion_infantil: str = "no"):
        
        if asientos_totales < 1:
            raise ValueError("El total de asientos debe ser un entero positivo (mínimo 1).")
        
        if sistema_retencion_infantil.lower() not in ["si", "no"]:
            raise ValueError("El sistema de retención infantil debe ser 'si' o 'no'.")
        
        super().__init__(patente, peso_kg, usuario)
        
        self.__asientos_totales = asientos_totales
        self.__ocupantes_actuales = 0
        self.__sistema_retencion_infantil = sistema_retencion_infantil.lower()
        self.__eventos_ocupacion = []

        self.__registrar_evento_ocupacion("Inicialización", 0, self.__ocupantes_actuales, f"Asientos totales configurados: {asientos_totales}")
        print(f"Vehículo con patente '{self.patente}' configurado con {asientos_totales} asientos.")

    # --- Métodos Privados de Encapsulamiento ---
    
    def __registrar_evento_ocupacion(self, accion: str, cantidad: int, ocupantes_despues: int, detalle: str = ""):
        ocupantes_antes = self.__ocupantes_actuales
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": accion,
            "cantidad": cantidad,
            "ocupantes_antes": ocupantes_antes,
            "ocupantes_despues": ocupantes_despues,
            "detalle": detalle
        }
        self.__eventos_ocupacion.append(evento)
        
        # Registro en el historial general del padre para trazabilidad completa
        # Usamos el name mangling del padre: _Vehiculo__registrar_evento
        self._Vehiculo__registrar_evento("Ocupación", f"Acción: {accion}, Cantidad: {cantidad}", f"Ocupantes: {ocupantes_despues}", detalle)

    """ Getters----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    @property
    def asientos_totales(self):
        return self.__asientos_totales

    @property
    def ocupantes_actuales(self):
        return self.__ocupantes_actuales

    @property
    def sistema_retencion_infantil(self):
        return self.__sistema_retencion_infantil

    @property
    def eventos_ocupacion(self):
        return list(self.__eventos_ocupacion)
        
    @property
    def asientos_libres(self):
        return self.__asientos_totales - self.__ocupantes_actuales

    """ Métodos----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def subir_personas(self, n: int):
        if self.estado == "inhabilitado":
            raise PermissionError("Operación rechazada. El vehículo está inhabilitado.")
            
        if n < 1:
            raise ValueError("La cantidad de personas a subir debe ser 1 o más.")
            
        espacio_disponible = self.asientos_libres
        if n > espacio_disponible:
            raise ValueError(f"No hay suficientes asientos. Solo quedan {espacio_disponible} libres.")

        self.__ocupantes_actuales += n
        self.__registrar_evento_ocupacion("Subida", n, self.__ocupantes_actuales, f"Suben {n} persona(s).")
        print(f"Subieron {n} persona(s). Ocupación actual: {self.__ocupantes_actuales}/{self.__asientos_totales}.")

    def bajar_personas(self, n: int):
        if self.estado == "inhabilitado":
            raise PermissionError("Operación rechazada. El vehículo está inhabilitado.")
            
        if n < 1:
            raise ValueError("La cantidad de personas a bajar debe ser 1 o más.")
            
        if n > self.__ocupantes_actuales:
            raise ValueError(f"No hay suficientes ocupantes. Solo hay {self.__ocupantes_actuales} personas a bordo.")

        self.__ocupantes_actuales -= n
        self.__registrar_evento_ocupacion("Bajada", n, self.__ocupantes_actuales, f"Bajan {n} persona(s).")
        print(f"Bajaron {n} persona(s). Ocupación actual: {self.__ocupantes_actuales}/{self.__asientos_totales}.")

    def reconfigurar_asientos(self, nuevo_total: int, motivo: str):
        if self.estado == "inhabilitado":
            raise PermissionError("Operación rechazada. El vehículo está inhabilitado.")
            
        if nuevo_total < 1:
            raise ValueError("El nuevo total de asientos debe ser 1 o más.")
            
        # Regla de Negocio: Si reduce asientos por debajo de la ocupación actual, debe rechazarse.
        if nuevo_total < self.__ocupantes_actuales:
            raise ValueError(f"Reconfiguración rechazada. Nuevo total ({nuevo_total}) es menor a la ocupación actual ({self.__ocupantes_actuales}).")

        anterior = self.__asientos_totales
        self.__asientos_totales = nuevo_total
        
        self.__registrar_evento_ocupacion("Reconfiguración", nuevo_total, self.__ocupantes_actuales, f"Asientos cambiados de {anterior} a {nuevo_total}. Motivo: {motivo}")
        print(f"Asientos reconfigurados de {anterior} a {self.__asientos_totales}. Motivo: {motivo}.")

    def vaciar_auto(self, motivo: str):
        if self.__ocupantes_actuales == 0:
            print("El vehículo ya está vacío.")
            return

        cantidad_vaciada = self.__ocupantes_actuales
        self.__ocupantes_actuales = 0
        
        self.__registrar_evento_ocupacion("Vaciado", cantidad_vaciada, 0, f"Vaciado forzado de {cantidad_vaciada} personas. Motivo: {motivo}")
        print(f"Vehículo vaciado. {cantidad_vaciada} persona(s) bajaron. Motivo: {motivo}.")