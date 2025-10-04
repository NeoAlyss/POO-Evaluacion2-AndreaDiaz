# Incluye todo lo del Modelo 1 y añade control de lectura por páginas.
# Datos adicionales
    # paginas_totales (> 0). CHECK
    # paginas_leidas (inicia en 0). CHECK
    # eventos_lectura (solo lectura: fecha, páginas leídas, acumulado). CHECK
# Operaciones
    # leer(paginas) → incrementa paginas_leidas.
    # consultar_progreso() → devuelve % leído (paginas_leidas / paginas_totales × 100).
# Reglas de negocio
    # paginas_leidas siempre debe estar entre 0 y paginas_totales.
    # No se pueden leer páginas negativas ni más que las restantes.
    # paginas_totales no puede cambiarse una vez creado el libro.
    # Toda lectura queda registrada en eventos_lectura con fecha.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

from datetime import datetime
from Clases.Publicacion import Publicacion

class Libro(Publicacion):
    def __init__(self, id_publicacion: int, titulo: str, anio: int, paginas_totales: int):
        super().__init__(id_publicacion, titulo, anio)
        
        # Validación de paginas_totales, tiene que ser > 0
        if paginas_totales <= 0: 
            raise Exception("El total de páginas debe ser mayor a 0.")
        
        self.__paginas_totales = paginas_totales
        self.__paginas_leidas = 0
        self.__eventos_lectura = []  # Lista de diccionarios con eventos de lectura

        self._Publicacion__registrar_evento("Creación", None, f"Libro creado con {paginas_totales} páginas.")
        self.__registrar_evento(0, "Creación del libro con páginas totales: " + str(paginas_totales))
        print(f"Libro '{titulo}' creado con {paginas_totales} páginas.")

    """ Getters--------------------------------------------------------------------------------------------------------------- """

    @property
    def paginasTotales(self):
        return self.__paginas_totales
    
    @property
    def paginasLeidas(self):
        return self.__paginas_leidas
    
    @property
    def eventosLectura(self):
        return self.__eventos_lectura
    
    """ Setters--------------------------------------------------------------------------------------------------------------- """
    #No se permiten setters para paginas_totales y paginas_leidas, ya que no deben cambiarse directamente.
    
    """ Métodos--------------------------------------------------------------------------------------------------------------- """
    def __registrar_evento(self, paginas_leidas: int, descripcion: str): 
        evento = {
            "fecha": datetime.now(),
            "paginas_leidas": paginas_leidas,
            "descripcion": descripcion
        }
        self.__eventos_lectura.append(evento)
        print(f"Evento registrado: {descripcion} - Páginas leídas en este evento: {paginas_leidas} - Fecha: {evento['fecha']}")
    
    def leer(self, paginas: int):
        if paginas <= 0:
            raise Exception("No se pueden leer páginas negativas o cero.")
        
        paginas_restantes = self.__paginas_totales - self.__paginas_leidas

        if paginas > paginas_restantes:
            raise Exception(f"No se pueden leer más páginas de las restantes. Páginas restantes: {paginas_restantes}.")

        if paginas_restantes == 0:
            raise Exception("El libro ya ha sido leído completamente.")
        
        paginasLectura = min(paginas, paginas_restantes)
        self.__paginas_leidas += paginasLectura
        self.__registrar_evento_lectura(paginasLectura, self.__paginas_leidas)
        print(f"Páginas leídas: {paginasLectura}. Total leído: {self.__paginas_leidas}/{self.__paginas_totales} páginas.")
        return paginasLectura

    def consultar_progreso(self) -> float: # aquí se calcula el progreso en % de la lectura
        if self.__paginas_totales == 0:
            return 0.0
        
        return (self.__paginas_leidas / self.__paginas_totales) * 100
    
    def ver_historial_lectura(self):
        return self.__eventos_lectura

    