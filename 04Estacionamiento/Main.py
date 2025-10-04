# Alta de vehículo: crear Vehículo con patente = "ABCD12" y peso_kg = 1450; queda habilitado.
# Actualización de peso: actualizar_peso(1500) → OK, historial registra cambio; actualizar_peso(0) → rechazo.
# Inhabilitar/Habilitar: inhabilitar("mantención") → OK; intentar actualizar_peso(1600) estando inhabilitado → rechazo; habilitar("mantención finalizada") → OK.
# Alta de auto: crear Auto con asientos_totales = 5, ocupantes_actuales inicia en 0.
# Subir personas: subir_personas(3) → ocupantes = 3; subir_personas(3) → rechazo (excede asientos); evento registrado.
# Bajar personas: bajar_personas(2) → ocupantes = 1; bajar_personas(5) → rechazo (no puede quedar negativo).
# Reconfigurar asientos: con ocupantes = 1, reconfigurar_asientos(2, "reparación") → OK; intentar reconfigurar_asientos(0) → rechazo.
# Vaciar auto: vaciar_auto("fin de turno") → ocupantes = 0, evento registrado.
# Estados: inhabilitar() y luego subir_personas(1) → rechazo por estado.
# Auditoría: historial_eventos y eventos_ocupacion muestran todos los movimientos con fecha/hora, usuario y detalle.
"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from datetime import datetime
from Clases.Vehiculo import Vehiculo
from Clases.ModeloAsientos import ModeloAsientos

auto1 = ModeloAsientos("ABCD12", 1450, 5, "admin", "si")
print(auto1)

auto1.actualizar_peso(1500, "admin")

try:
    auto1.actualizar_peso(0, "admin")
except ValueError as ve:
    print(f"Error: {ve}")
auto1.inhabilitar("mantención", "admin")
try:
    auto1.actualizar_peso(1600, "admin")
except PermissionError as pe:
    print(f"Error: {pe}")

auto1.habilitar("mantención finalizada", "admin")
auto1.subir_personas(3)
print(f"Ocupantes actuales: {auto1.ocupantes_actuales}")

try:
    auto1.subir_personas(3)
except ValueError as ve:
    print(f"Error: {ve}")

auto1.bajar_personas(2)
print(f"Ocupantes actuales: {auto1.ocupantes_actuales}")

try:
    auto1.bajar_personas(5)
except ValueError as ve:
    print(f"Error: {ve}")

try:
    auto1.reconfigurar_asientos(0, "Asientos inválidos") 
except ValueError as ve:
    print(f"Error: {ve}")
    
auto1.reconfigurar_asientos(2, "reparación") 
print(f"Asientos totales: {auto1.asientos_totales}, Asientos libres:{auto1.asientos_libres}")

auto1.vaciar_auto("fin de turno")
print(f"Ocupantes actuales: {auto1.ocupantes_actuales}")

auto1.inhabilitar("mantenimiento", "admin")

try:
    auto1.subir_personas(1)
except PermissionError as pe:
    print(f"Error: {pe}")
print("\nHistorial de Eventos del Vehículo:")

for evento in auto1.historial_eventos:
    print(evento)
        

