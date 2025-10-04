# cuerpo_celeste.py

from datetime import datetime

# --- Clase de Excepción Personalizada ---
class ValidacionError(Exception):
    """Excepción personalizada para errores de validación en los datos."""
    pass

# --- Clase Base CuerpoCeleste ---
class CuerpoCeleste:
    """
    Modelo base para cualquier cuerpo celeste.
    Implementa encapsulamiento, validación y registro de historial.
    """
    
    # Contador para generar IDs únicos de forma sencilla
    _next_id = 1

    def __init__(self, nombre: str, masa_kg: float):
        """
        Inicializa un nuevo CuerpoCeleste.
        Valida que nombre no sea vacío y masa sea positiva.
        """
        self._id_celeste = CuerpoCeleste._next_id
        CuerpoCeleste._next_id += 1
        
        # Atributos internos (privados)
        self._nombre = None
        self._masa_kg = None
        self._historial_eventos = []
        self._fecha_ultima_masa = None
        self._num_modificaciones = 0

        # Inicialización a través de las operaciones para asegurar validación
        self.actualizar_nombre(nombre)
        self.actualizar_masa(masa_kg)

    # --- Propiedades de Solo Lectura (Getters) ---
    
    @property
    def id_celeste(self) -> int:
        """Devuelve el ID único del cuerpo celeste."""
        return self._id_celeste

    @property
    def nombre(self) -> str:
        """Devuelve el nombre actual."""
        return self._nombre

    @property
    def masa_kg(self) -> float:
        """Devuelve la masa actual en kg."""
        return self._masa_kg

    @property
    def historial_eventos(self) -> list:
        """Devuelve el historial de eventos (solo lectura)."""
        # Devolvemos una copia para proteger la lista original
        return list(self._historial_eventos)

    @property
    def fecha_ultima_actualizacion_masa(self) -> str:
        """Devuelve la fecha de la última actualización de masa."""
        return self._fecha_ultima_masa

    @property
    def numero_modificaciones(self) -> int:
        """Devuelve el número total de modificaciones realizadas."""
        return self._num_modificaciones
    
    # --- Métodos de Ayuda Interna ---
    
    def _registrar_evento(self, campo: str, valor_anterior, valor_nuevo):
        """
        Registra un evento de modificación en el historial.
        """
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = {
            "fecha_hora": ahora,
            "campo_modificado": campo,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo
        }
        self._historial_eventos.append(evento)
        self._num_modificaciones += 1

    # --- Operaciones de Modificación con Validación y Registro ---

    def actualizar_nombre(self, nuevo_nombre: str):
        """
        Actualiza el nombre, validando que no esté vacío.
        """
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValidacionError("El nombre no puede ser una cadena vacía.")
        
        valor_anterior = self._nombre
        if valor_anterior is not None and valor_anterior != nuevo_nombre:
            self._registrar_evento("nombre", valor_anterior, nuevo_nombre)
            
        self._nombre = nuevo_nombre.strip()

    def actualizar_masa(self, nueva_masa: float):
        """
        Actualiza la masa, validando que sea mayor que cero.
        Registra el cambio en el historial.
        """
        if nueva_masa <= 0:
            raise ValidacionError("La masa debe ser un número positivo (mayor que 0).")
        
        valor_anterior = self._masa_kg
        if valor_anterior is not None and valor_anterior != nueva_masa:
            self._registrar_evento("masa_kg", valor_anterior, nueva_masa)
            self._fecha_ultima_masa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._masa_kg = nueva_masa

    # --- Operaciones de Reporte ---
    
    def consultar_ficha(self) -> str:
        """
        Devuelve una ficha de datos actuales más los últimos 3 eventos.
        """
        ficha = f"\n--- Ficha de {self.nombre} (ID: {self.id_celeste}) ---\n"
        ficha += f"  Masa (kg): {self.masa_kg:_.2e}\n"
        ficha += f"  Última Modificación Masa: {self.fecha_ultima_actualizacion_masa or 'N/A'}\n"
        ficha += f"  Total de Modificaciones: {self.numero_modificaciones}\n"
        
        eventos = self.historial_eventos
        if eventos:
            ficha += "\n  --- Últimos Eventos ---\n"
            # Mostrar los últimos 3 eventos
            for i, evento in enumerate(eventos[-3:], start=1):
                ficha += f"  {i}. {evento['fecha_hora']} - Campo: {evento['campo_modificado']} | Antes: {evento['valor_anterior']} | Ahora: {evento['valor_nuevo']}\n"
        else:
            ficha += "\n  --- No hay eventos de modificación registrados ---\n"
            
        return ficha

    # --- Representación de Objeto ---
    
    def __str__(self):
        """Representación legible del objeto."""
        return f"CuerpoCeleste(ID={self.id_celeste}, Nombre='{self.nombre}', Masa={self.masa_kg:_.2e} kg)"