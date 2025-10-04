# main.py
from Clases.Vehiculo import Vehiculo
from Clases.Auto import Auto

def separador(titulo):
    """Función de utilidad para mejor presentación."""
    print("\n" + "="*50)
    print(f"--- {titulo} ---")
    print("="*50)

if __name__ == "__main__":
    
    # ----------------------------------------------------
    separador("TEST 1: VEHÍCULO BASE (MODELO A)")
    # ----------------------------------------------------
    
    # Criterio: Alta de vehículo
    print("\n--- 1.1 ALTA DE VEHÍCULO ---")
    try:
        v1 = Vehiculo(patente="ABCD12", peso_kg=1450.0, usuario="AdminTest")
        print(v1)
        print(f"Estado inicial: {v1.estado}")
    except ValueError as e:
        print(f"Error al crear vehículo: {e}")
        
    # Criterio: Actualización de peso
    print("\n--- 1.2 ACTUALIZACIÓN DE PESO ---")
    v1.actualizar_peso(1500.0) # OK, historial registra cambio
    v1.actualizar_peso(1500.0) # Aviso, mismo peso
    v1.actualizar_peso(0)      # Rechazo por ser 0
    
    # Criterio: Inhabilitar/Habilitar
    print("\n--- 1.3 INHABILITAR / INTENTAR OPERACIÓN / HABILITAR ---")
    v1.inhabilitar("mantención") # OK
    
    # Intentar operación estando inhabilitado -> rechazo
    v1.actualizar_peso(1600.0, usuario="Taller") 
    
    v1.habilitar("mantención finalizada") # OK

    # Intento de operación después de habilitar
    v1.actualizar_peso(1600.0, usuario="Taller") # OK ahora
    
    # Criterio: Auditoría y Ficha
    separador("FICHA Y AUDITORÍA DE VEHÍCULO BASE")
    ficha_v1 = v1.consultar_ficha()
    for k, v in ficha_v1.items():
        print(f"| {k}: {v}")
    
    print("\n--- HISTORIAL DE EVENTOS COMPLETO ---")
    for evento in v1.historial_eventos:
        print(str(evento))

    # ----------------------------------------------------
    separador("TEST 2: AUTO (MODELO A EXTENDIDO)")
    # ----------------------------------------------------

    # Criterio: Alta de auto
    print("\n--- 2.1 ALTA DE AUTO ---")
    a1 = Auto(patente="EFGH34", peso_kg=1200.0, asientos_totales=5, usuario="AdminTest")
    print(a1)
    print(a1.consultar_ocupacion())
    
    # Criterio: Subir personas
    print("\n--- 2.2 SUBIR PERSONAS ---")
    a1.subir_personas(3) # OK: 0 -> 3
    a1.subir_personas(3) # Rechazo: Excede asientos (3+3 > 5)

    # Criterio: Bajar personas
    print("\n--- 2.3 BAJAR PERSONAS ---")
    a1.bajar_personas(2) # OK: 3 -> 1
    a1.bajar_personas(5) # Rechazo: No puede quedar negativo (1-5 < 0)

    # Criterio: Reconfigurar asientos
    print("\n--- 2.4 RECONFIGURAR ASIENTOS ---")
    # Ocupantes actuales: 1
    a1.reconfigurar_asientos(2, "reparación de asiento trasero") # OK: 5 -> 2 (1 <= 2)
    print(a1.consultar_ocupacion())
    a1.reconfigurar_asientos(0, "error") # Rechazo: Nuevo total < 1
    a1.reconfigurar_asientos(1, "prueba") # OK: 2 -> 1 (1 <= 1)
    a1.reconfigurar_asientos(0, "error de nuevo") # Rechazo: Ocupación (1) > Nuevo total (0)

    # Criterio: Vaciar auto
    print("\n--- 2.5 VACIAR AUTO ---")
    a1.vaciar_auto("fin de turno") # OK: 1 -> 0

    # Criterio: Estados (Inhabilitar y operaciones)
    print("\n--- 2.6 ESTADOS Y OPERACIONES DE OCUPACIÓN ---")
    a1.inhabilitar("inspección técnica") # OK
    a1.subir_personas(1) # Rechazo por estado inhabilitado
    a1.habilitar("inspección aprobada") # OK
    a1.subir_personas(1) # OK: 0 -> 1

    # Criterio: Auditoría de Ocupación
    separador("AUDITORÍA DE AUTO (OCUPACIÓN)")
    print(a1)
    print(a1.consultar_ocupacion())
    
    print("\n--- EVENTOS DE OCUPACIÓN COMPLETO ---")
    for evento in a1.eventos_ocupacion:
        print(str(evento))