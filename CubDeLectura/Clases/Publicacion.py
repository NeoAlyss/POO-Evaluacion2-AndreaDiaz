# Datos mínimos
    # id_publicacion (único).
    # titulo (cadena no vacía). CHECK
    # anio (≥ 1450). CHECK
    # historial_eventos (solo lectura: lista de cambios con fecha, campo modificado, valor anterior/nuevo). CHECK
# Operaciones
    # actualizar_titulo(nuevo_titulo) → valida que no sea vacío.
    # actualizar_anio(nuevo_anio) → valida ≥ 1450; registra en historial.
# Reglas de negocio
    # El anio debe ser ≥ 1450 (inicio de la imprenta moderna). CHECK
    # titulo no puede quedar vacío. CHECK
    # Ningún campo puede alterarse directamente; todo cambio pasa por operaciones. CHECK
    # Cada cambio queda en historial_eventos con fecha/hora.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from datetime import datetime

class Publicacion:

    #VAmos hacer lo mismo que en parcela usando un atributo de clase para evitar ids repetidos
    _ids_existentes = set() #se utiliza set para evitar duplicados

    def __init__(self, id_publicacion: int, titulo: str, anio: int):

        if not isinstance(id_publicacion, int) or id_publicacion <= 0: #Acá el isinstance es para validar que sea un entero
            raise Exception("El ID de publicación debe ser un número entero positivo.")

        if id_publicacion in Publicacion._ids_existentes:
            raise Exception(f"El ID de publicación '{id_publicacion}' ya está registrado. Debe ser único.")
        
        if not titulo or titulo.strip() == "": #strip() elimina espacios en blanco al inicio y fin #esta validación cubre None y ""
            raise Exception("El título no puede estar vacío.")
        
        if anio < 1450:
            raise Exception("El año de publicación debe ser 1450 o posterior.")

        self.__id_publicacion = id_publicacion  # Regla: No se puede cambiar después de la creación
        self.__titulo = titulo
        self.__anio = anio
        self.__historial_eventos = []

        Publicacion._ids_existentes.add(id_publicacion) #Agregamos el id al set para evitar duplicados futuros

        #Registrando ando los eventos, como en parcela
        self.__registrar_evento("Creación", None, f"id_publicacion: {self.__id_publicacion}, titulo: {self.__titulo}, anio: {self.__anio}")
        print(f"Publicación '{titulo}' creada. ID: {id_publicacion}.")

    """ Getters--------------------------------------------------------------------------------------------------------------- """
    @property
    def id_publicacion(self):
        return self.__id_publicacion
    
    @property
    def titulo(self):
        return self.__titulo
        
    @property
    def anio(self):
        return self.__anio
        
    @property
    def historial_eventos(self):
        return list(self.__historial_eventos)

    """ Setters--------------------------------------------------------------------------------------------------------------- """
    #Demo de que no se pueden alterar directamente, sino mediante los métodos
    @titulo.setter
    def titulo(self, nuevo_titulo):
        raise AttributeError("El título no se puede modificar directamente. Use actualizar_titulo().")

    """ Métodos--------------------------------------------------------------------------------------------------------------- """

    def __registrar_evento(self, campo: str, valor_anterior, valor_nuevo, detalle: str = ""):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo": campo,
            "anterior": valor_anterior,
            "nuevo": valor_nuevo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)

    def actualizar_titulo(self, nuevo_titulo: str):
        if not nuevo_titulo or nuevo_titulo.strip() == "":
            raise Exception("El título no puede estar vacío.")
        
        titulo_anterior = self.__titulo
        self.__titulo = nuevo_titulo
        self.__registrar_evento("titulo", titulo_anterior, nuevo_titulo)
        print(f"Título actualizado de '{titulo_anterior}' a '{nuevo_titulo}'.")
    
    def actualizar_anio(self, nuevo_anio: int):
        if nuevo_anio < 1450:
            raise Exception("El año de publicación debe ser 1450 o posterior.")
        
        anio_anterior = self.__anio
        self.__anio = nuevo_anio
        self.__registrar_evento("anio", anio_anterior, nuevo_anio)
        print(f"Año actualizado de {anio_anterior} a {nuevo_anio}.")
    