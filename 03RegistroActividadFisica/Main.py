# Crear actividad "Yoga" con duración 60 min. OK
# Intentar crear actividad con duración 0 min → rechazo. ok
# Crear carrera de 10 km en 50 min. OK
# calcular_ritmo() devuelve 5 min/km. ok
# Intentar registrar distancia -3 km → rechazo. OK
# Actualizar duración de carrera a 55 min → cambio válido, queda en historial_eventos. OK
# Todo intento de alterar distancia_km directamente debe ser imposible (error o rechazo).
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from Clases.Actividad import Actividad
from Clases.Carrera import Carrera

actividad1= Actividad("Yoga", 60)
print(actividad1.historial_eventos)

try:
    actividad_invalida = Actividad("Meditacion", 0)
except ValueError as e: #e es el mensaje de error que definimos en la clase con motivo
    print(f"Error al crear actividad: {e}")

carrera1 = Carrera("Carrera de los 10K", 50, 10.0)
print(carrera1)

ritmo = carrera1.calcular_ritmo()
print(f"Ritmo de la carrera: {ritmo} min/km")

try:
    carrera1.registrar_distancia(-3.0)
except ValueError as e:
    print(f"Error al registrar distancia: {e}")

carrera1.actualizar_duracion(55)
print(carrera1.historial_eventos)   

try:
    carrera1.distancia_km = 15.0  # Intento de modificar directamente (debe fallar)
except AttributeError as e:
    print(f"Error al modificar distancia directamente: {e}")
print(f"Distancia actual de la carrera: {carrera1.distancia_km} km")  # Verifica que no cambió

carrera1.actualizar_duracion(55)
print(carrera1.historial_eventos)   

carrera1.distancia_km = 15.0  # Intento de modificar directamente (debe fallar)
print(f"Distancia actual de la carrera: {carrera1.distancia_km}")


