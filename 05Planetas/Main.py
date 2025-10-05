# Criterios de aceptación mínimos.
    # Crear cuerpo celeste "Estrella X" con masa 2 × 10^30 kg.
    # Crear planeta "Tierra" con masa 5.97 × 10^24 kg, radio 6371 km, distancia_sol 149 600 000 km.
    # Crear planeta "Marte" con masa 6.42 × 10^23 kg, radio 3389 km, distancia_sol 227 900 000 km.
    # calcular_densidad() en Tierra devuelve un valor aproximado (no nulo ni negativo).
    # comparar_distancia(Tierra, Marte) devuelve que Tierra está más cerca del sol.
    # Intentar crear planeta con radio 0 o distancia negativa → rechazo.
    # Actualizar masa del planeta a un valor válido → se registra en historial.
    # Intentar modificar atributos directamente sin operaciones → rechazo.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from Clases.CuerposCelestes import ObjetoCeleste
from Clases.Planeta import Planeta

cuerpo1 = ObjetoCeleste("Estrella X", 2e30)

planeta1 = Planeta("Tierra", 5.97e24, 6371, 149600000)

planeta2 = Planeta("Marte", 6.42e23, 3389, 227900000)

planeta1.calcular_densidad()
print(f"Densidad de {planeta1.nombre}: {planeta1.densidad_kg_km3:.2f} kg/km³")

cercano = planeta1 if planeta1.distancia_sol_km < planeta2.distancia_sol_km else planeta2
print(f"El planeta más cercano al sol es: {cercano.nombre}")

try:
    planeta_invalido = Planeta("Planeta Inválido", 1e22, 0, -100000)
except ValueError as e:
    print(f"Error al crear planeta inválido: {e}")

planeta1.actualizar_masa(6e24)

print(f"Historial de eventos de {planeta1.nombre}:")
for evento in planeta1.historial_eventos:
    print(evento)
try:
    planeta1.__masa_kg = 1e25  # Intento de modificación directa (debe fallar)
except AttributeError as e:
    print(f"Error al modificar masa directamente: {e}")

print(f"Masa actual de {planeta1.nombre}: {planeta1.masa_kg} kg")
print(f"Número de modificaciones en {planeta1.nombre}: {planeta1.numero_modificaciones}")