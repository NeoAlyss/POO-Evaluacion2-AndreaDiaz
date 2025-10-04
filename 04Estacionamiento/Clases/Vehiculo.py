# Datos mínimos
    # id_vehiculo (único).
    # patente (cadena no vacía, formato válido definido por el sistema; p. ej., regex configurable).
    # peso_kg (número > 0).
    # estado ∈ {habilitado, inhabilitado} (por defecto habilitado).
    # historial_eventos (solo lectura: fecha/hora, usuario, tipo_evento, detalle anterior/nuevo).
# Operaciones
    # actualizar_peso(nuevo_peso_kg) → valida > 0; registra en historial.
    # habilitar(motivo) / inhabilitar(motivo) → cambia estado; registra en historial.
    # consultar_ficha() → devuelve datos actuales y últimas marcas de auditoría.
# Reglas de negocio
    # patente no se puede modificar una vez creado el registro.
    # peso_kg no puede ajustarse por acceso directo; solo por actualizar_peso.
    # No se permiten operaciones sobre vehículos inhabilitados salvo habilitar.
    # Todo cambio relevante queda en historial_eventos con timestamp y usuario.
# Datos derivados/reportables
    # Fecha de último pesaje/actualización.
    # Conteo de cambios de estado (habilitado/inhabilitado).
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from datetime import datetime
import uuid

class Vehiculo:

    _ids_existentes = set()
    
    def __init__(self, patente: str, peso_kg: float, usuario: str = "Sistema"):

        if not patente or not patente.strip():
            raise ValueError("La patente no puede estar vacía.")
        # Validación de unicidad
        if patente in Vehiculo._ids_existentes:
            raise ValueError(f"La patente '{patente}' ya está registrada.")
            
        if peso_kg <= 0:
            raise ValueError("El peso debe ser un número positivo (mayor a 0 kg).")

        self.__id_vehiculo = str(uuid.uuid4())
        self.__patente = patente.strip().upper()
        self.__peso_kg = peso_kg
        self.__estado = "habilitado"
        self.__historial_eventos = []
        self.__fecha_ultimo_ajuste = datetime.now()
        self.__conteo_cambios_estado = 0

        Vehiculo._ids_existentes.add(self.__patente)
        
        self.__registrar_evento(usuario, "Creación", None, f"Patente: {self.__patente}, Peso: {self.__peso_kg} kg, Estado: {self.__estado}")
        print(f"Vehículo con patente '{self.__patente}' creado y habilitado.")

    
    """ Método para registrar evento----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def __registrar_evento(self, usuario: str, tipo_evento: str, valor_anterior, valor_nuevo):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usuario": usuario,
            "tipo_evento": tipo_evento,
            "anterior": valor_anterior,
            "nuevo": valor_nuevo
        }
        self.__historial_eventos.append(evento)

    
    """ Getters----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    @property
    def id_vehiculo(self):
        return self.__id_vehiculo

    @property
    def patente(self):
        return self.__patente

    @property
    def peso_kg(self):
        return self.__peso_kg

    @property
    def estado(self):
        return self.__estado

    @property
    def historial_eventos(self):
        return list(self.__historial_eventos)

    @property
    def fecha_ultimo_ajuste(self):
        return self.__fecha_ultimo_ajuste
        
    @property
    def conteo_cambios_estado(self):
        return self.__conteo_cambios_estado
        
    
    """ Setters----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    @peso_kg.setter
    def peso_kg(self, nuevo_peso):
        raise AttributeError("El peso no se puede modificar directamente. Use actualizar_peso().")

    @patente.setter
    def patente(self, nueva_patente):
        raise AttributeError("La patente no se puede modificar una vez creado el registro.")

    
    """ Métodos del Negocio----------------------------------------------------------------------------------------------------------------------------------------------------------"""

    def actualizar_peso(self, nuevo_peso_kg: float, usuario: str):
        if self.__estado == "inhabilitado":
            raise PermissionError(f"Operación rechazada. El vehículo está en estado '{self.__estado}'.")

        if nuevo_peso_kg <= 0:
            raise ValueError("El nuevo peso debe ser un número positivo (mayor a 0 kg).")

        valor_anterior = self.__peso_kg
        self.__peso_kg = nuevo_peso_kg
        self.__fecha_ultimo_ajuste = datetime.now()
        
        self.__registrar_evento(usuario, "Actualización Peso", valor_anterior, self.__peso_kg)
        print(f"Peso del vehículo {self.__patente} actualizado de {valor_anterior} kg a {self.__peso_kg} kg.")

    def inhabilitar(self, motivo: str, usuario: str):
        if self.__estado == "inhabilitado":
            print(f"El vehículo {self.__patente} ya está inhabilitado.")
            return

        anterior = self.__estado
        self.__estado = "inhabilitado"
        self.__conteo_cambios_estado += 1
        
        self.__registrar_evento(usuario, "Inhabilitación", anterior, self.__estado)
        print(f"Vehículo {self.__patente} inhabilitado. Motivo: {motivo}.")

    def habilitar(self, motivo: str, usuario: str):
        if self.__estado == "habilitado":
            print(f"El vehículo {self.__patente} ya está habilitado.")
            return

        anterior = self.__estado
        self.__estado = "habilitado"
        self.__conteo_cambios_estado += 1
        
        self.__registrar_evento(usuario, "Habilitación", anterior, self.__estado)
        print(f"Vehículo {self.__patente} habilitado. Motivo: {motivo}.")

    def consultar_ficha(self):
        ficha = {
            "ID": self.__id_vehiculo,
            "Patente": self.__patente,
            "Peso Actual (kg)": self.__peso_kg,
            "Estado": self.__estado,
            "Fecha Último Ajuste": self.__fecha_ultimo_ajuste.strftime("%Y-%m-%d %H:%M:%S"),
            "Conteo Cambios Estado": self.__conteo_cambios_estado,
            "Último Evento": self.__historial_eventos[-1] if self.__historial_eventos else "N/A"
        }
        return ficha

    def __str__(self):
        return (f"Vehiculo(Patente: {self.__patente}, Peso: {self.__peso_kg} kg, "
                f"Estado: {self.__estado}, Último Ajuste: {self.fecha_ultimo_ajuste.strftime('%Y-%m-%d %H:%M')})")