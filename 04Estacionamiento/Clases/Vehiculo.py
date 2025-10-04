# vehiculo.py
import uuid
from datetime import datetime
import re

# Constantes para la Auditoría
USUARIO_SISTEMA = "Sistema-Parqueo"
ESTADOS_VEHICULO = {"habilitado", "inhabilitado"}

# --- Clases de Apoyo ---
class EventoHistorico:
    """Clase para registrar un evento de auditoría en el historial_eventos."""
    def __init__(self, usuario: str, tipo_evento: str, detalle_anterior: str, detalle_nuevo: str):
        self.fecha_hora = datetime.now()
        self.usuario = usuario
        self.tipo_evento = tipo_evento
        self.detalle_anterior = detalle_anterior
        self.detalle_nuevo = detalle_nuevo

    def __str__(self):
        """Representación legible del evento."""
        return (f"[{self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Usuario: {self.usuario} | Evento: {self.tipo_evento}\n"
                f"  -> Antes: {self.detalle_anterior} | Después: {self.detalle_nuevo}")

# --- Clase Principal: Vehiculo ---
class Vehiculo:
    """
    Representa un vehículo en el parque de estacionamiento.
    Implementa validaciones de peso y control de estado.
    """
    # Regex de ejemplo para patente: 4 letras y 2 números (ej: ABCD12)
    PATENTE_REGEX = r"^[A-Z]{4}\d{2}$" 

    def __init__(self, patente: str, peso_kg: float, usuario: str = USUARIO_SISTEMA):
        # Generación de ID único
        self.__id_vehiculo = str(uuid.uuid4())
        
        # Validaciones iniciales
        if not self._validar_patente(patente):
            raise ValueError(f"Patente '{patente}' no válida. Formato esperado: LLLLNN (ej: ABCD12).")
        if peso_kg <= 0:
            raise ValueError("El peso inicial debe ser mayor a 0 kg.")
        
        # Datos mínimos
        self.__patente = patente # Patente: No se puede modificar (Regla de negocio)
        self.__peso_kg = peso_kg
        self.__estado = "habilitado"
        self.__historial_eventos = []
        
        # Auditoría de creación
        self._registrar_evento(usuario, "Creación", "N/A", f"Vehículo creado: {patente}, {peso_kg} kg")

    # --- Propiedades (Getters) ---
    @property
    def id_vehiculo(self) -> str:
        return self.__id_vehiculo

    @property
    def patente(self) -> str:
        return self.__patente

    @property
    def peso_kg(self) -> float:
        return self.__peso_kg

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def historial_eventos(self) -> list:
        # Solo lectura: devolvemos una copia superficial para evitar modificación externa
        return list(self.__historial_eventos) 

    # --- Métodos de Validación Interna ---
    def _validar_patente(self, patente: str) -> bool:
        """Valida que la patente cumpla con el formato definido."""
        return bool(re.fullmatch(Vehiculo.PATENTE_REGEX, patente.upper()))

    def _registrar_evento(self, usuario: str, tipo: str, antes: str, despues: str):
        """Método privado para añadir un evento al historial."""
        evento = EventoHistorico(usuario, tipo, antes, despues)
        self.__historial_eventos.append(evento)

    # --- Operaciones Públicas ---

    def actualizar_peso(self, nuevo_peso_kg: float, usuario: str = USUARIO_SISTEMA) -> bool:
        """
        Actualiza el peso del vehículo. Valida si es > 0 y si el vehículo está habilitado.
        """
        if self.estado == "inhabilitado":
            print(f"❌ Error: No se puede actualizar el peso de un vehículo inhabilitado ({self.patente}).")
            return False

        if nuevo_peso_kg <= 0:
            print(f"❌ Error: El nuevo peso debe ser mayor a 0 kg. Se recibió {nuevo_peso_kg} kg.")
            return False

        if nuevo_peso_kg != self.__peso_kg:
            peso_anterior = f"{self.__peso_kg} kg"
            self.__peso_kg = nuevo_peso_kg
            self._registrar_evento(usuario, "Actualización Peso", peso_anterior, f"{nuevo_peso_kg} kg")
            print(f"✅ Éxito: Peso de {self.patente} actualizado a {self.__peso_kg} kg.")
            return True
        else:
            print(f"ℹ️ Aviso: Peso de {self.patente} no cambiado, el valor es el mismo.")
            return False


    def inhabilitar(self, motivo: str, usuario: str = USUARIO_SISTEMA) -> bool:
        """Cambia el estado del vehículo a 'inhabilitado'."""
        if self.__estado == "inhabilitado":
            print(f"ℹ️ Aviso: {self.patente} ya está inhabilitado.")
            return False
        
        estado_anterior = self.__estado
        self.__estado = "inhabilitado"
        self._registrar_evento(usuario, "Cambio Estado", 
                               f"Estado: {estado_anterior} | Motivo Anterior: N/A", 
                               f"Estado: {self.__estado} | Motivo: {motivo}")
        print(f"⚠️ Éxito: {self.patente} inhabilitado por '{motivo}'.")
        return True

    def habilitar(self, motivo: str, usuario: str = USUARIO_SISTEMA) -> bool:
        """Cambia el estado del vehículo a 'habilitado'. Única operación permitida en estado inhabilitado."""
        if self.__estado == "habilitado":
            print(f"ℹ️ Aviso: {self.patente} ya está habilitado.")
            return False
            
        estado_anterior = self.__estado
        self.__estado = "habilitado"
        self._registrar_evento(usuario, "Cambio Estado", 
                               f"Estado: {estado_anterior}", 
                               f"Estado: {self.__estado} | Motivo: {motivo}")
        print(f"✅ Éxito: {self.patente} habilitado por '{motivo}'.")
        return True

    def consultar_ficha(self) -> dict:
        """Devuelve un resumen de los datos y auditoría."""
        ultimo_pesaje = "N/A"
        conteo_cambios = 0
        
        # Datos derivados/reportables
        for evento in reversed(self.__historial_eventos):
            if evento.tipo_evento == "Actualización Peso":
                ultimo_pesaje = evento.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
            if evento.tipo_evento == "Cambio Estado":
                conteo_cambios += 1
                
        ultima_auditoria = str(self.__historial_eventos[-1]) if self.__historial_eventos else "No hay eventos registrados."

        return {
            "ID": self.id_vehiculo,
            "Patente": self.patente,
            "Peso (kg)": self.peso_kg,
            "Estado": self.estado.upper(),
            "Último Pesaje": ultimo_pesaje,
            "Conteo Cambios Estado": conteo_cambios,
            "Última Marca Auditoría": ultima_auditoria
        }

    def __str__(self):
        return f"Vehículo ({self.patente}) - Peso: {self.peso_kg} kg, Estado: {self.estado}"