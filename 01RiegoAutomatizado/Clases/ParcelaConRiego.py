# Extiende el comportamiento funcional del modelo 1 incorporando gestión de riego para una parcela concreta.
# Datos adicionales
    # • litros_disponibles (≥ 0; no editable directamente). CHECK
    # • tasa_riego_l_ha (> 0; por defecto del sistema). CHECK
    # • umbral_min_litros (≥ 0). CHECK
    # • estado_riego ∈ {habilitado, inhabilitado} (por defecto habilitado si la parcela está activa). CHECK
    # • eventos_riego (solo lectura: fecha, litros_solicitados, litros_aplicados, saldo_antes/después, modo). CHECK SOLO LECTURA
# Operaciones
    # • configurar_tasa(l_ha) → > 0.
    # • configurar_umbral(litros) → ≥ 0.
    # • habilitar_riego() / inhabilitar_riego().
    # • cargar_agua(litros) → suma si litros > 0; registra evento de carga.
    # • regar_automatico(modo)
        # o Demanda = superficie_ha × tasa_riego_l_ha.
        # o modo ∈ {estricto, parcial}.
        # o En estricto: aplica solo si litros_disponibles - demanda ≥ umbral_min_litros; si no, rechaza.
        # o En parcial: aplica la mayor cantidad posible manteniendo saldo_final ≥ umbral_min_litros.
        # o Descuenta de litros_disponibles y registra en eventos_riego.
# Reglas de negocio
    # • Prohibido regar si: parcela inactiva, estado_riego = inhabilitado, tasa_riego_l_ha ≤ 0.
    # • litros_disponibles solo cambia por cargar_agua o regar_automatico.
    # • Saldo nunca puede quedar negativo.
    # • Si la parcela pasa a inactiva, el riego queda automáticamente inhabilitado.
"""--------------------------------------------------------------------------------------------------------------- """
from Clases.Parcela import Parcela
from datetime import datetime

class ParcelaConRiego(Parcela):
    
    def __init__(self, id_parcela: int, superficie_ha: float, cultivo_actual:str):
        super().__init__(id_parcela, superficie_ha, cultivo_actual)
        
        self.__litros_disponibles = 0  # Cumple con lo de >= 0
        self.__tasa_riego_l_ha = 0     # default del sistema
        self.__umbral_min_litros = 0   # Cumple
        self.__estado_riego = "inhabilitado" # Actualmente inhabilitado, se habilita si la parcela se activa
        self.__eventos_riego = []      # solo lectura

            # Si la parcela se crea como activa, habilitamos el riego automáticamente
        if self.estado == "activo":
            self.habilitar_riego() # Llama al método para habilitar el riego y registrar el evento

    """ Getters--------------------------------------------------------------------------------------------------------------- """
    @property
    def litrosDisponibles(self):
        return self.__litros_disponibles
        
    @property
    def tasaRiegoLHa(self):
        return self.__tasa_riego_l_ha
        
    @property
    def umbralMinLitros(self):
        return self.__umbral_min_litros
        
    @property
    def estadoRiego(self):
        return self.__estado_riego
        
    @property
    def eventosRiego(self):
        # Se devuelve una copia para asegurar la inmutabilidad desde fuera
        return list(self.__eventos_riego)
    
    """ Setters--------------------------------------------------------------------------------------------------------------- """

    @litrosDisponibles.setter
    def litrosDisponibles(self, value):
        raise Exception("No puedes modificar la cantidad de agua directamente. Pare eso, deber usar el método cargar_agua() o regar_automatico()")

    """ Métodos--------------------------------------------------------------------------------------------------------------- """

    def desactivar(self, motivo: str):
        super().desactivar(motivo) # Llama al método de la clase base para cambiar el estado y registrar el evento
        if self.__estado_riego == "habilitado":
            self.__estado_riego = "inhabilitado"
            # Usamos el método de la clase base para registrar el evento en el historial principal
            self._Parcela__registrar_evento("Riego Inhabilitado", "La parcela fue desactivada, por lo que el riego se inhabilitó automáticamente.")

    def configurar_tasa(self, l_ha: float): #cantidad de litros por hectárea
        if l_ha <= 0:
            print(" La tasa de riego debe ser un número mayor a 0")
            return #Valido que sea mayor a 0
        
        anterior = self.__tasa_riego_l_ha #Guardo el valor previo para el registro del evento
        self.__tasa_riego_l_ha = l_ha #Actualizo la tasa
        self._Parcela__registrar_evento("COnfiguración tasa de riego",f"Tasa de riego configurada de {anterior} L/ha a {l_ha} L/ha.")
        print(f"La tasa de riego ha sido configurada a: {self.__tasa_riego_l_ha} L/ha.")

    def configurar_umbral(self, litros: float): #mínimo de litros que debe quedar después de regar
        if litros < 0: #Valido que sea mayor o igual a 0 los litros
            print("Umbral mínimo de litros debe ser un número mayor o igual a 0.")
            return
        
        self.__umbral_min_litros = litros #Actualizo el umbral
        self._Parcela__registrar_evento("Configuración umbral de la tasa de riego", f"Umbral mínimo de litros configurado a: {litros} L.")
        print(f"Umbral mínimo configurado a: {self.__umbral_min_litros} L.")

    #-----Acá empiezan los cambios de habilitar/deshabiliar el riego de una parcela----------------------------------------------------------------------------------------    
    
    def habilitar_riego(self):
        if self.estado != "activo": #Valido que la parcela esté activa para habilitar el riego
            print("No se puede habilitar el riego porque la parcela se encuentra inactiva.")
            return
            
        if self.__estado_riego == "habilitado": #Valido que no esté ya habilitado,,,si es así, no hago nada
            print("El riego ya se ha habilitado.")
            return

        self.__estado_riego = "habilitado" #Cambio el estado a habilitado
        self._Parcela__registrar_evento("Riego Habilitado", "Sistema de riego puesto en 'habilitado'.")
        print("Se ha habilitado el riego de la parcela")

    def inhabilitar_riego(self):
        if self.__estado_riego == "inhabilitado":
            print("El riego ya ha inhabilitado.")
            return

        self.__estado_riego = "inhabilitado"
        self._Parcela__registrar_evento("Riego Inhabilitado", "Sistema de riego puesto en 'inhabilitado'.")
        print("Se ha inhabilitado el riego de la parcela")

    #-----Acá termina los cambios de habilitar/deshabiliar riego y empieza lo de cargar agua y regar automático----------------------------------------------------------------
    
    def cargar_agua(self, litros: float):
        if litros <= 0:
            print("La cantidad a cargar debe ser mayor a 0 litros.")
            return
            
        saldo_antes = self.__litros_disponibles #Guardo el saldo antes de la carga
        self.__litros_disponibles += litros #Actualizo el saldo
        saldo_despues = self.__litros_disponibles #Guardo el saldo después de la carga
        
        detalle_evento = f"Se ha cargado agua: Litros: {litros} L, Saldo Antes: {saldo_antes:.2f} L, Saldo Después: {saldo_despues:.2f} L."
        self._Parcela__registrar_evento("Carga de Agua", detalle_evento)
        print(f"Se ha cargado {litros:.2f} L de agua, su nuevo saldo es de: {self.__litros_disponibles:.2f} L.")

    def __registrar_evento_riego(self, litros_solicitados: float, litros_aplicados: float, saldo_antes: float, modo: str):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "litros_solicitados": litros_solicitados,
            "litros_aplicados": litros_aplicados,
            "saldo_antes": saldo_antes,
            "saldo_despues": self.__litros_disponibles,
            "modo": modo
        }
        self.__eventos_riego.append(evento)
        
        # Registrar también en el historial general de la parcela
        self._Parcela__registrar_evento(f"Riego ({modo})", f"Aplicados {litros_aplicados:.2f} L. Saldo final: {self.__litros_disponibles:.2f} L.")

    def __es_riego_permitido(self):
        if self.estado != "activo":
            print("Riego rechazado: La parcela está inactiva.")
            return False
        if self.__estado_riego == "inhabilitado":
            print("Riego rechazado: El riego está inhabilitado.")
            return False
        if self.__tasa_riego_l_ha <= 0:
            print("Riego rechazado: La tasa de riego es 0 o menor. Configúrala primero.")
            return False
        return True
        
    def regar_automatico(self, modo: str):
        if not self.__es_riego_permitido():
            return 0
            
        if modo not in ["estricto", "parcial"]:
            print("Modo de riego inválido. Use 'estricto' o 'parcial'.")
            return 0
    
        demanda = self.superficieHa * self.tasaRiegoLHa
        litros_aplicados = 0
        saldo_antes = self.__litros_disponibles
        
        print(f"Iniciando riego '{modo}' (Demanda: {demanda:.2f} L, Saldo: {saldo_antes:.2f} L, Umbral: {self.umbralMinLitros} L)")
        
        if modo == "estricto":
            # Condición: aplica solo si litros_disponibles - demanda >= umbral_min_litros
            saldo_final_esperado = saldo_antes - demanda
            
            if saldo_final_esperado >= self.umbralMinLitros:
                litros_aplicados = demanda
                self.__litros_disponibles -= litros_aplicados
                print(f"Riego Estricto APLICADO. Aplicados {litros_aplicados:.2f} L.")
            else:
                print(f"Riego Estricto RECHAZADO. Saldo final ({saldo_final_esperado:.2f} L) sería inferior al umbral ({self.umbralMinLitros} L).")
                
        elif modo == "parcial":
            # Aplica la mayor cantidad posible manteniendo saldo_final >= umbral_min_litros.
            
            maximo_aplicable = saldo_antes - self.umbralMinLitros
            
            if maximo_aplicable <= 0:
                print(f"Riego Parcial RECHAZADO. Saldo disponible ({saldo_antes:.2f} L) es insuficiente para dejar el umbral ({self.umbralMinLitros} L).")
                
            elif maximo_aplicable < demanda:
                # Aplica un riego parcial, dejando el saldo justo en el umbral
                litros_aplicados = maximo_aplicable
                self.__litros_disponibles -= litros_aplicados
                print(f"Riego Parcial APLICADO parcialmente. Aplicados {litros_aplicados:.2f} L.")
                
            else: # maximo_aplicable >= demanda
                # Aplica la demanda completa
                litros_aplicados = demanda
                self.__litros_disponibles -= litros_aplicados
                print(f"Riego Parcial APLICADO en su totalidad. Aplicados {litros_aplicados:.2f} L.")

        # Registrar el evento si se aplicó agua
        if litros_aplicados > 0:
            self.__registrar_evento_riego(demanda, litros_aplicados, saldo_antes, modo)
        
        return litros_aplicados