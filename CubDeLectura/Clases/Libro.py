
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from datetime import datetime
from publicacion import Publicacion, PublicacionException # Importamos la clase base y la excepción

class Libro(Publicacion):
    """
    Representa un Libro, extendiendo Publicacion con control de páginas y progreso de lectura.
    """

    def __init__(self, id_publicacion: str, titulo: str, anio: int, paginas_totales: int):
        """
        Constructor de la clase Libro. Llama al constructor de Publicacion.

        Args:
            id_publicacion (str): Identificador único.
            titulo (str): Título.
            anio (int): Año de publicación (>= 1450).
            paginas_totales (int): Total de páginas del libro (> 0).

        Reglas de negocio validadas:
        - paginas_totales debe ser > 0.
        - paginas_leidas se inicializa en 0.
        """
        super().__init__(id_publicacion, titulo, anio)

        if paginas_totales <= 0:
            raise PublicacionException("Las páginas totales deben ser un número positivo.")

        # Atributos adicionales, también protegidos (inmutables o controlados por métodos)
        self._paginas_totales = paginas_totales  # Regla: No se puede cambiar después de la creación
        self._paginas_leidas = 0
        self._eventos_lectura = []

        # Registro del estado inicial del libro
        self._registrar_evento_lectura(0, f"Libro inicializado con {paginas_totales} páginas totales.")


    # --- Métodos de Ayuda ---

    def _registrar_evento_lectura(self, paginas_leidas_en_evento: int, descripcion: str = None):
        """
        Método interno para registrar un evento de lectura.
        """
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "paginas_leidas_en_evento": paginas_leidas_en_evento,
            "acumulado": self._paginas_leidas,
            "descripcion": descripcion if descripcion else f"Leídas {paginas_leidas_en_evento} páginas."
        }
        self._eventos_lectura.append(evento)


    # --- Operaciones ---

    def leer(self, paginas: int):
        """
        Incrementa el número de páginas leídas, aplicando las reglas de negocio.

        Args:
            paginas (int): Número de páginas leídas en esta sesión.

        Reglas de negocio validadas:
        - No se pueden leer páginas negativas.
        - No se pueden leer más páginas que las restantes (no superar paginas_totales).
        """
        if paginas <= 0:
            raise PublicacionException("No se pueden leer un número negativo o cero de páginas.")

        paginas_restantes = self._paginas_totales - self._paginas_leidas

        if paginas > paginas_restantes:
            raise PublicacionException(
                f"No puedes leer {paginas} páginas. Solo quedan {paginas_restantes} páginas por leer."
            )

        # Si la validación es exitosa, actualiza el estado
        self._paginas_leidas += paginas
        self._registrar_evento_lectura(paginas)
        print(f"[LOG] ¡Genial! Leíste {paginas} páginas. Acumulado: {self._paginas_leidas}.")


    def consultar_progreso(self) -> float:
        """
        Devuelve el porcentaje de lectura completado.
        """
        if self._paginas_totales == 0:
            return 0.0 # Evitar división por cero

        progreso = (self._paginas_leidas / self._paginas_totales) * 100
        # Criterio de aceptación: porcentaje redondeado
        return round(progreso, 2)


    # --- Propiedades de Solo Lectura (Getters) ---
    
    @property
    def paginas_totales(self):
        # Esta propiedad garantiza que paginas_totales no puede ser alterada
        return self._paginas_totales

    @property
    def paginas_leidas(self):
        return self._paginas_leidas

    @property
    def eventos_lectura(self):
        # Devuelve una copia para asegurar que la lista original es "solo lectura"
        return list(self._eventos_lectura)

    # El resto de propiedades de Publicacion (titulo, anio, historial_eventos) son heredadas.
