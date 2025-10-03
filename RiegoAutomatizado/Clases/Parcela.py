# Datos mínimos:
    # • id_parcela (único). CHECK
    # • superficie_ha (número > 0, hasta 2 decimales). CHECK
    # • cultivo_actual (cadena no vacía). CHECK
    # • estado ∈ {activa, inactiva} (por defecto activa). CHECK
    # • historial_eventos (solo lectura: lista de cambios con fecha, tipo, detalle). CHECK SOLO LECTURA
# Operaciones:
    # • actualizar_cultivo(nuevo_cultivo) → valida no vacía; registra en historial.
    # • activar(motivo) / desactivar(motivo) → cambia estado; registra en historial.
    # • rectificar_superficie(nueva_superficie, motivo) → solo > 0; registra valor previo/nuevo.
# Reglas de negocio:
    # • No se permite actualizar_cultivo si estado = inactiva.
    # • superficie_ha no se modifica por acceso directo; solo vía rectificar_superficie.
    # • Todo cambio genera entrada en historial_eventos con marca de tiempo.
"""--------------------------------------------------------------------------------------------------------------- """

from datetime import datetime

class Parcela:
    _parcelas_existentes = {} # Según entiendo, esto se llama atributo de clase. En este caso, está permitiendo almacenar los id's para evitar duplicados. 
#Se ubica antes del constructor, porque si estuviese dentro, sería un atributo del objeto, lo que al crear un nuevo objeto haría que el dicc se reinicie
    estados_permitidos = {"activo", "inactivo"}

    def __init__(self, id_parcela: int, superficie_ha: float, cultivo_actual:str):
        
        if id_parcela in Parcela._parcelas_existentes:
            raise ValueError(f"El ID de parcela '{id_parcela}' ya está registrado. Debe ser único.")
        #Acá estamos validado que el id no se repita, si no se repite se inicializa el objeto y se agrega al diccionario

        if superficie_ha <= 0:
            raise ValueError("La superficie debe ser un número mayor a 0.") #Se chequea que la superficie sea mayor o igual a 0
        
        if not cultivo_actual:
            raise ValueError("El cultivo actual no puede estar vacío.")#VAlidación que no esté vacío
        
        self.__id_parcela = id_parcela
        self.__superficie_ha = round(superficie_ha, 2) # Acá se cummple con lo de los 2 decimales
        self.__cultivo_actual = cultivo_actual
        self.__estado = "activo" #Por defecto según lo pide el ejericcio
        self.__historial_eventos = []

        Parcela._parcelas_existentes[id_parcela] = self
        self.__registrar_evento("Creación", f"Parcela creada con cultivo '{cultivo_actual}' y superficie {superficie_ha} ha.")

    """ Getters--------------------------------------------------------------------------------------------------------------- """
    @property
    def idParcela(self):
        return self.__id_parcela
    
    @property
    def superficieHa(self):
        return self.__superficie_ha
    
    @property
    def cultivoActual(self):
        return self.__cultivo_actual
    
    @property
    def estado(self):
        return self.__estado
    
    @property
    def historialEventos(self):
        return list(self.__historial_eventos) 
    #Si lo escribo así, me devuelve una copia de la lista, no la lista original, por lo que no permitiría que se pueda modificar desde afuera
    
    """ Setters--------------------------------------------------------------------------------------------------------------- """
    #No deben haber setters ya que según las reglas de negocio, no se puede modificar directamente ninguno de los atributos
    #Lo siguiente tuve que buscarlo en internet, no lo tenía tan claro para hacer el registro del evento con los datos que pide el ejercicio
    
   
    #Acá se realiza un método privado para registrar el historial de los eventos. Se importa datetime para registrar la fecha y hora del evento

    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "detalle": detalle
        } #Acá creo el diccionario con los datos
        self.__historial_eventos.append(evento) #Acá le agrego al diccionario 

    """ Métodos--------------------------------------------------------------------------------------------------------------- """
    def actualizar_cultivo(self, nuevo_cultivo: str):
        if self.__estado == "inactivo":
            print("No se puede actualizar el cultivo de una parcela inactiva")
            return #Acá no permito si la parcela está inactiva
        
        if not nuevo_cultivo:
            print(f"El cultivo {nuevo_cultivo}no puede estar vacío.")
            return #Valido que no esté vacío
        
        if self.__cultivo_actual.lower() == nuevo_cultivo.lower():
            print(f" El cultivo ya es '{nuevo_cultivo}'. No se realizó ningún cambio.")
            return
        
        cultivo_previo = self.__cultivo_actual #Guardo el cultivo previo para el registro del evento
        self.__cultivo_actual = nuevo_cultivo #Actualizo el cultivo
        self.__registrar_evento("Actualización de Cultivo", f"Cultivo cambiado de '{cultivo_previo}' a '{nuevo_cultivo}'.")
        
    def activar(self, motivo: str):
        if self.__estado == "activo":
            print("La parcela ya está activa.")
            return
        
        self.__estado = "activo"
        self.__registrar_evento("Activación", motivo)
    
    def desactivar(self, motivo: str):
        if self.__estado == "inactivo":
            print("La parcela ya está inactiva.")
            return
        
        self.__estado = "inactivo"
        self.__registrar_evento("Desactivación", motivo)

    def rectificar_superficie(self, nueva_superficie: float, motivo: str):
        if nueva_superficie <= 0:
            print("La superficie debe ser un número mayor a 0.")
            return
        
        superficie_previa = self.__superficie_ha
        self.__superficie_ha = round(nueva_superficie, 2)
        self.__registrar_evento("Rectificación de Superficie", f"Superficie cambiada de {superficie_previa} ha a {nueva_superficie} ha. Motivo: {motivo}.")
    
# Pruebas
if __name__ == "__main__":
    parcela1 = Parcela(1, 10.567, "Trigo")
    parcela2 = Parcela(2, 5.25, "Maíz")
    
    print(f"ID Parcela: {parcela1.idParcela}, Superficie: {parcela1.superficieHa} ha, Cultivo: {parcela1.cultivoActual}, Estado: {parcela1.estado}")
    print(f"ID Parcela: {parcela2.idParcela}, Superficie: {parcela2.superficieHa} ha, Cultivo: {parcela2.cultivoActual}, Estado: {parcela2.estado}")
    
    parcela1.actualizar_cultivo("Cebada")
    parcela1.desactivar("Mantenimiento programado")
    parcela1.activar("Mantenimiento completado")
    parcela1.rectificar_superficie(12.34, "Medición precisa")
    
    for evento in parcela1.historialEventos:
        print(evento)