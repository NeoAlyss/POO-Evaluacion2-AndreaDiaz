# Crear parcela 10.50 ha, cultivo = "Trigo", estado = activa. CHECK
# actualizar_cultivo("Maíz") registra en historial con fecha CHECK
# Asociar riego: tasa = 1500 L/ha, umbral = 2000 L; cargar_agua(20000). CHECK
# regar_automatico(estricto) con 10.50 ha → demanda 15 750 L; aplica y deja saldo 2 250 L (evento registrado). CHECK
# Desactivar parcela y luego intentar regar_automatico → rechazo con mensaje claro. CHECK
# regar_automatico(parcial) con saldo 3000 L, demanda 15 750 L, umbral 2000 L → aplica 1000 L y deja saldo 2000 L (evento “parcial”).CHECK
# Intentar fijar litros_disponibles por fuera de operaciones → imposible / error.
# Toda operación queda en historial_eventos / eventos_riego con timestamp y detalle. CEHCK
"""--------------------------------------------------------------------------------------------------------------- """

from Clases.ParcelaConRiego import ParcelaConRiego

"""CREAR PARCELA"""

parcela1 = ParcelaConRiego(id_parcela=1, superficie_ha=10.50, cultivo_actual="Trigo")
print(f"Parcela creada: ID: {parcela1.idParcela}, cultivo: {parcela1.cultivoActual} , superficie: {parcela1.superficieHa} ha , estado: {parcela1.estado}")

"""ACTUALIZAR PARCELA A CULTIVO DE MAIZ"""
parcela1.actualizar_cultivo("Maíz")
print(f"Parcela actualizada: ID: {parcela1.idParcela}, cultivo: {parcela1.cultivoActual} , superficie: {parcela1.superficieHa} ha , estado: {parcela1.estado}")

"""ASOCIAR RIEGO Y CARGAR AGUA"""
parcela1.configurar_tasa(1500)
parcela1.configurar_umbral(2000)
parcela1.cargar_agua(20000)

"""REGAR AUTOM ATICO ESTRICTO"""
parcela1.regar_automatico("estricto")
print(f"Saldo Actual de {parcela1.idParcela}: {parcela1.litrosDisponibles:.2f} L (Esperado: 2250.00 L)")

"""REGAR AUTOMATICO CON PARCELA RECHAZADA AL DESACTIVAR"""

parcela1.desactivar("Prueba de rechazo por inactividad.") # Inhabilita automáticamente el riego.
parcela1.regar_automatico("estricto") # Debe ser rechazado.
print(f"Estado de Riego {parcela1.idParcela} después de desactivar: {parcela1.estadoRiego}")

"""Intentar fijar litros_disponibles por fuera de operaciones → imposible / error."""
try:
    parcela1.__litros_disponibles = 50000
    print("Error: Se pudo modificar el atributo privado, ¡Fallo el encapsulamiento!")
except AttributeError:
        print(f"Intento de modificar litros_disponibles por acceso directo falló. Encapsulamiento OK.")
except Exception as e:
    print(f"Intento de modificar litros_disponibles falló con error: {e}")

except ValueError as e:
    print(f"No se pudo ejecutar el test de la primera parcela: {e}")

"""SEGUNDA PARCELA PARA PROBAR"""
try:
    parcela2 = ParcelaConRiego(id_parcela=2, superficie_ha=5.75, cultivo_actual="Soja")
    print(f"\nParcela creada: ID: {parcela2.idParcela}, cultivo: {parcela2.cultivoActual} , superficie: {parcela2.superficieHa} ha , estado: {parcela2.estado}")
    
    parcela2.configurar_tasa(1200)
    parcela2.configurar_umbral(1500)
    parcela2.cargar_agua(3000)
    
    parcela2.regar_automatico("parcial") # Con 3000 L, demanda 6900 L, umbral 1500 L → aplica 1500 L y deja saldo 1500 L.
    print(f"Saldo Actual de {parcela2.idParcela}: {parcela2.litrosDisponibles:.2f} L (Esperado: 1500.00 L)")
except ValueError as e:
    print(f"No se pudo ejecutar el test de la segunda parcela: {e}")

""" Mostrar Historiales de Eventos """
print("EVENTOS REGISTRADOS:")
for evento in parcela1.historialEventos:
    print(evento)
for evento in parcela2.historialEventos:
    print(evento)
