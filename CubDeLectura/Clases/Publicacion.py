from datetime import datetime

# Clase de excepción personalizada para manejar errores de Publicación
class PublicacionException(Exception):
    """Excepción base para errores relacionados con la Publicación."""
    pass

class Publicacion:
    """
    Representa una publicación genérica (artículo, libro, revista, etc.).
    Implementa validaciones de título y año, y registra un historial de eventos.
    """

    def __init__(self, id_publicacion: str, titulo: str, anio: int):
        """
        Constructor de la clase Publicacion.

        Args:
            id_publicacion (str): Identificador único de la publicación.
            titulo (str): Título de la publicación.
            anio (int): Año de publicación.
        
        Reglas de negocio validadas:
        - El título no puede ser vacío.
        - El año debe ser igual o superior a 1450 (inicio de la imprenta moderna).
        """
        # Atributos protegidos (por convención con _) para evitar alteración directa
        self._id_publicacion = id_publicacion
        self._historial_eventos = []

        # Validación inicial del título y año
        if not titulo:
            raise PublicacionException("El título no puede estar vacío al crear la publicación.")
        if anio < 1450:
            raise PublicacionException(f"El año debe ser >= 1450. Valor recibido: {anio}.")

        self._titulo = titulo
        self._anio = anio

        # Evento de creación inicial
        self._registrar_evento("CREACION", "N/A", "N/A", f"Publicación creada con título '{titulo}' y año {anio}")


    def _registrar_evento(self, campo_modificado: str, valor_anterior, nuevo_valor, descripcion: str = None):
        """
        Método interno para registrar cualquier cambio en el historial de eventos.
        """
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo_modificado": campo_modificado,
            "valor_anterior": valor_anterior,
            "nuevo_valor": nuevo_valor,
            "descripcion": descripcion if descripcion else f"Cambio en {campo_modificado}: {valor_anterior} -> {nuevo_valor}"
        }
        self._historial_eventos.append(evento)


    # --- Operaciones ---

    def actualizar_titulo(self, nuevo_titulo: str):
        """
        Actualiza el título de la publicación, validando que no sea una cadena vacía.
        Registra el cambio en el historial.
        """
        if not nuevo_titulo or nuevo_titulo.strip() == "":
            raise PublicacionException("El nuevo título no puede ser una cadena vacía.")

        valor_anterior = self._titulo
        self._titulo = nuevo_titulo
        self._registrar_evento("titulo", valor_anterior, self._titulo)
        print(f"[LOG] Título actualizado a: '{self._titulo}'.")

    def actualizar_anio(self, nuevo_anio: int):
        """
        Actualiza el año de la publicación, validando que sea >= 1450.
        Registra el cambio en el historial.
        """
        if nuevo_anio < 1450:
            raise PublicacionException(f"Regla de negocio: El año debe ser >= 1450. Intento: {nuevo_anio}.")

        valor_anterior = self._anio
        self._anio = nuevo_anio
        self._registrar_evento("anio", valor_anterior, self._anio)
        print(f"[LOG] Año actualizado a: {self._anio}.")

    # --- Propiedades de Solo Lectura (Getters) ---
    # Esto permite leer los atributos sin permitir la modificación directa (Regla de negocio)

    @property
    def id_publicacion(self):
        return self._id_publicacion

    @property
    def titulo(self):
        return self._titulo

    @property
    def anio(self):
        return self._anio

    @property
    def historial_eventos(self):
        # Devuelve una copia para asegurar que la lista original es "solo lectura"
        return list(self._historial_eventos)

# Nota: La regla de no alterar campos directamente se cumple usando propiedades
# de solo lectura y atributos internos con el prefijo '_'.