from actividad import Actividad
from carrera import Carrera

def ejecutar_pruebas():
    print("=== Ejercicio 3: Registro de Actividades Físicas ===")
    
    # 1. Crear actividad "Yoga" con duración 60 min.
    print("\n--- PRUEBA 1: Creación de Actividad Válida ---")
    try:
        yoga = Actividad("Yoga", 60)
        print(f"✅ Creada: {yoga}")
        print(f"   Historial inicial: {yoga.historial_eventos[-1]}")
    except ValueError as e:
        print(f"❌ Error al crear Actividad válida: {e}")
        return # Terminamos si la prueba base falla

    # 2. Intentar crear actividad con duración 0 min → rechazo.
    print("\n--- PRUEBA 2: Creación de Actividad con Duración Inválida (0 min) ---")
    try:
        Actividad("Estiramiento", 0)
        print("❌ Fallo: Se permitió crear una actividad con duración 0.")
    except ValueError as e:
        print(f"✅ Rechazo correcto: {e}")

    # 3. Crear carrera de 10 km en 50 min.
    print("\n--- PRUEBA 3: Creación de Carrera Válida ---")
    try:
        carrera_50m = Carrera("5K Local", 50, 10.0)
        print(f"✅ Creada: {carrera_50m}")
    except ValueError as e:
        print(f"❌ Error al crear Carrera válida: {e}")
        return # Terminamos si la prueba base falla

    # 4. calcular_ritmo() devuelve 5 min/km.
    print("\n--- PRUEBA 4: Cálculo de Ritmo ---")
    ritmo_calculado = carrera_50m.calcular_ritmo()
    ritmo_esperado = 5.0
    if ritmo_calculado == ritmo_esperado:
        print(f"✅ Ritmo correcto: {ritmo_calculado} min/km (Esperado: {ritmo_esperado})")
    else:
        print(f"❌ Ritmo incorrecto: {ritmo_calculado} min/km (Esperado: {ritmo_esperado})")

    # 5. Intentar registrar distancia -3 km → rechazo.
    print("\n--- PRUEBA 5: Registro de Distancia Negativa ---")
    try:
        carrera_50m.registrar_distancia(-3.0)
        print("❌ Fallo: Se permitió registrar una distancia negativa.")
    except ValueError as e:
        print(f"✅ Rechazo correcto al registrar distancia: {e}")

    # 6. Actualizar duración de carrera a 55 min → cambio válido, queda en historial_eventos.
    print("\n--- PRUEBA 6: Actualizar Duración ---")
    duracion_anterior = carrera_50m.duracion_min
    try:
        carrera_50m.actualizar_duracion(55)
        print(f"✅ Duración actualizada a {carrera_50m.duracion_min} min.")
        
        # Verificar historial
        ultimo_evento = carrera_50m.historial_eventos[-1]
        if ultimo_evento["campo_modificado"] == "duracion_min" and ultimo_evento["valor_nuevo"] == 55:
            print(f"✅ Cambio registrado en historial_eventos: {ultimo_evento}")
            
            # Verificar eventos_registro (debe haber un nuevo punto)
            ultimo_registro = carrera_50m.eventos_registro[-1]
            if ultimo_registro["distancia_registrada"] == 10.0 and ultimo_registro["duracion_acumulada"] == 55:
                 print(f"✅ Registro de punto actualizado en eventos_registro: {ultimo_registro}")
            else:
                 print("❌ Fallo en registro de punto")
        else:
            print("❌ Fallo: Cambio no registrado correctamente en historial_eventos.")
            
        print(f"   Nuevo ritmo calculado: {carrera_50m.calcular_ritmo()} min/km")

    except ValueError as e:
        print(f"❌ Error al actualizar la duración: {e}")

    # 7. Todo intento de alterar distancia_km directamente debe ser imposible (error o rechazo).
    print("\n--- PRUEBA 7: Intento de Alteración Directa de Distancia ---")
    try:
        # Esto generará un AttributeError porque _distancia_km es una propiedad "privada" (por convención)
        carrera_50m._distancia_km = 50.0 
        print("❌ Fallo: Se permitió alterar la distancia_km directamente (aunque sea por convención).")
    except AttributeError:
        print("✅ Intento de modificación directa fallido (Propiedad 'privada').")
    except Exception as e:
         print(f"✅ Otro error (no es AttributeError, pero evita modificación directa): {type(e).__name__} - {e}")

if __name__ == "__main__":
    ejecutar_pruebas()