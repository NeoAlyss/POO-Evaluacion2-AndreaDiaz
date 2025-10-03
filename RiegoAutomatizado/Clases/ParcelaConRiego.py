# Extiende el comportamiento funcional del modelo 1 incorporando gestión de riego para una parcela concreta.
# Datos adicionales
    # • litros_disponibles (≥ 0; no editable directamente).
    # • tasa_riego_l_ha (> 0; por defecto del sistema).
    # • umbral_min_litros (≥ 0).
    # • estado_riego ∈ {habilitado, inhabilitado} (por defecto habilitado si la parcela está activa).
    # • eventos_riego (solo lectura: fecha, litros_solicitados, litros_aplicados, saldo_antes/después, modo).
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
# Criterios de aceptación mínimos
    # • Crear parcela 10.50 ha, cultivo = "Trigo", estado = activa.
    # • actualizar_cultivo("Maíz") registra en historial con fecha.
    # • Asociar riego: tasa = 1500 L/ha, umbral = 2000 L; cargar_agua(20000).
    # • regar_automatico(estricto) con 10.50 ha → demanda 15 750 L; aplica y deja saldo 2 250L (evento registrado).
    # • Desactivar parcela y luego intentar regar_automatico → rechazo con mensaje claro.
    # • regar_automatico(parcial) con saldo 3000 L, demanda 15 750 L, umbral 2000 L → aplica 1000 L y deja saldo 2000 L (evento “parcial”).
    # • Intentar fijar litros_disponibles por fuera de operaciones → imposible / error.
    # • Toda operación queda en historial_eventos / eventos_riego con timestamp y detalle
"""--------------------------------------------------------------------------------------------------------------- """
from Clases.Parcela import Parcela
from datetime import datetime

class ParcelaConRiego(Parcela):
    
    demanda_riego = {"estricto", "parcial"}
    # TASA_RIEGO_DEFECTO_L_HA = 1000   

    def _registrar_evento(self, tipo: str, detalle: str, es_riego=False, datos_riego=None):
        self._Parcela__registrar_evento(tipo, detalle)  # Llama al método privado del padre
        if es_riego and datos_riego:
            evento_riego = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "litros_solicitados": datos_riego['solicitados'],
                "litros_aplicados": datos_riego['aplicados'],
                "saldo_antes": datos_riego['saldo_antes'],
                "saldo_despues": datos_riego['saldo_despues'],
                "modo": datos_riego['modo']
            }
            self.__eventos_riego.append(evento_riego)
            

    def __init__(self, id_parcela: int, superficie_ha: float, cultivo_actual: str):
        super().__init__(id_parcela, superficie_ha, cultivo_actual)
        self.__litros_disponibles = 0.0 # Iniciamos con 0 litros disponibles
        self.__tasa_riego_l_ha = 1000.0  # Valor por defecto del sistema
        self.__umbral_min_litros = 0.0
        self.__estado_riego = "habilitado" if self.estado == "activo" else "inhabilitado"
        self.__eventos_riego = []

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
        return list(self.__eventos_riego)  # Devuelve una copia para evitar modificaciones externas
    """ Setters--------------------------------------------------------------------------------------------------------------- """
    # No se permiten setters para los atributos que no deben ser modificados directamente
    """ Métodos--------------------------------------------------------------------------------------------------------------- """

    def configurar_tasa(self, l_ha: float):
        if l_ha > 0:
            self.__tasa_riego_l_ha = l_ha
            self._Parcela__registrar_evento("Configuración Riego", f"Tasa de riego configurada a {l_ha} L/ha.")
        else:
            raise ValueError("La tasa de riego debe ser un número mayor a 0.")
    
    def configurar_umbral(self, litros: float):
        if litros >= 0:
            self.__umbral_min_litros = litros
            self._Parcela__registrar_evento("Configuración Riego", f"Umbral mínimo de litros configurado a {litros} L.")
        else:
            raise ValueError("El umbral mínimo de litros debe ser un número mayor o igual a 0.")
    
    def habilitar_riego(self):
        if self.estado == "activo":
            self.__estado_riego = "habilitado"
            self._Parcela__registrar_evento("Riego", "Riego habilitado.")
        else:
            raise ValueError("No se puede habilitar el riego en una parcela inactiva.")
    
    def inhabilitar_riego(self):
        self.__estado_riego = "inhabilitado"
        self._Parcela__registrar_evento("Riego", "Riego inhabilitado.")
    
    def cargar_agua(self, litros: float):
        if litros > 0:
            saldo_antes = self.__litros_disponibles
            self.__litros_disponibles += litros
            self._Parcela__registrar_evento("Carga de Agua", f"Cargados {litros} L. Saldo antes: {saldo_antes} L, saldo después: {self.__litros_disponibles} L.")
        else:
            raise ValueError("La cantidad de litros a cargar debe ser un número mayor a 0.")
        
    def regar_automatico(self, modo: str):
        modo = modo.lower()
        if modo not in self.demanda_riego:
            raise ValueError(f"Modo de riego '{modo}' no es válido.")

        #No se puede regar si la parcela está inactiva, el estado del riego es inhabilitado o la tasa de riego es menor o igual a 0
        if self.estado == "inactiva" or self.__estado_riego == "inhabilitado" or self.__tasa_riego_l_ha <= 0:
            motivo = ("Parcela inactiva." if self.estado == "inactiva" else 
                      "Riego inhabilitado." if self.__estado_riego == "inhabilitado" else 
                      "Tasa de riego inválida.")
            self.__registrar_evento("Riego: Rechazo", f"Intento de riego rechazado. Motivo: {motivo}")
            print(f"Riego rechazado: {motivo}")
            return
            
        demanda = self.superficieHa * self.__tasa_riego_l_ha
        litros_aplicados = 0.0
        saldo_antes = self.__litros_disponibles
        saldo_despues_requerido = self.__umbral_min_litros

        if modo == "estricto":
            saldo_estimado = saldo_antes - demanda
            if saldo_estimado >= saldo_despues_requerido:
                litros_aplicados = demanda
                print(f"Riego estricto aprobado. Aplicados: {litros_aplicados:.2f} L.")
            else:
                self._registrar_evento("Riego: Rechazo Estricto", f"Demanda ({demanda:.2f} L) rechazada. Saldo estimado ({saldo_estimado:.2f} L) es menor que el Umbral ({saldo_despues_requerido:.2f} L).")
                print(f"Riego estricto rechazado. Saldo insuficiente para mantener el umbral.")
                return

        elif modo == "parcial":
            litros_max_a_usar = max(0, saldo_antes - saldo_despues_requerido)
            if litros_max_a_usar >= demanda:
                litros_aplicados = demanda
            elif litros_max_a_usar > 0:
                litros_aplicados = litros_max_a_usar
                print(f"Riego parcial aplicado. Demanda: {demanda:.2f} L. Aplicados: {litros_aplicados:.2f} L (Máximo permitido por Umbral).")
            else:
                self.__registrar_evento("Riego: Rechazo Parcial", f"Demanda ({demanda:.2f} L) rechazada. Saldo actual ({saldo_antes:.2f} L) no permite aplicar ninguna cantidad manteniendo el Umbral.")
                print(f"Riego parcial rechazado. Saldo insuficiente para aplicar manteniendo el umbral.")
                return

        # Aplicar el descuento y registrar (Solo si litros_aplicados > 0)
        if litros_aplicados > 0:
            self.__litros_disponibles -= litros_aplicados
            self.__registrar_evento(
                f"Riego: Aplicado ({modo.capitalize()})", 
                f"Aplicados {litros_aplicados:.2f} L. Saldo final: {self.__litros_disponibles:.2f} L.",
                es_riego=True,
                datos_riego={'solicitados': demanda, 'aplicados': litros_aplicados, 'saldo_antes': saldo_antes, 'saldo_despues': self.__litros_disponibles, 'modo': modo}
            )
        
    def __str__(self):
        # Combina la información del padre y los datos de riego.
        base_info = super().__str__()
        riego_info = (
            f"Riegos isponibles: {self.__litros_disponibles:.2f} L / Tasa: {self.__tasa_riego_l_ha} L/ha / Estado Riego: {self.__estado_riego.upper()}"
        )
        return base_info + riego_info
        