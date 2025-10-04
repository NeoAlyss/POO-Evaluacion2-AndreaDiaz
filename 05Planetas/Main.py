# main.py

from Clases.CuerposCelestes import CuerpoCeleste, ValidacionError
from Clases.Planeta import Planeta

def ejecutar_pruebas():
    """Ejecuta todos los criterios de aceptación y pruebas de validación."""
    print("===============================================")
    print("=== Ejercicio 5: Catálogo de Planetas - PRUEBAS ===")
    print("===============================================\n")

    # --- Criterio 1: Crear Cuerpo Celeste (Estrella) ---
    print("--- 1. Creación de Cuerpo Celeste (Estrella) ---")
    try:
        # 2 x 10^30 kg (Masa aproximada del Sol)
        estrella_x = CuerpoCeleste("Estrella X", 2e30) 
        print(f"✅ Creado: {estrella_x}")
    except ValidacionError as e:
        print(f"❌ Error al crear Estrella X: {e}")
    print("-" * 30)


    # --- Criterio 2 y 3: Creación de Planetas (Tierra y Marte) ---
    print("\n--- 2 & 3. Creación de Planetas (Tierra y Marte) ---")
    try:
        tierra = Planeta(
            nombre="Tierra",
            masa_kg=5.97e24,          # kg
            radio_km=6371,            # km
            distancia_sol_km=149600000  # km (1 AU)
        )
        print(f"✅ Creado: {tierra}")
        
        marte = Planeta(
            nombre="Marte",
            masa_kg=6.42e23,          # kg
            radio_km=3389,            # km
            distancia_sol_km=227900000  # km
        )
        print(f"✅ Creado: {marte}")
    except ValidacionError as e:
        print(f"❌ Error al crear un planeta: {e}")
    print("-" * 30)


    # --- Criterio 4: calcular_densidad() en Tierra ---
    print("\n--- 4. Cálculo de Densidad de la Tierra ---")
    try:
        densidad_tierra = tierra.calcular_densidad()
        # Densidad en kg/km³
        print(f"✅ Densidad de la Tierra (kg/km³): {densidad_tierra:_.4e}")
        # La densidad debe ser positiva (no nula ni negativa)
        if densidad_tierra > 0:
            print("✅ El valor es positivo.")
        else:
             print("❌ El valor no es positivo.")
    except Exception as e:
        print(f"❌ Error al calcular densidad: {e}")
    print("-" * 30)


    # --- Criterio 5: comparar_distancia(Tierra, Marte) ---
    print("\n--- 5. Comparación de Distancia al Sol (Tierra vs Marte) ---")
    try:
        resultado_comparacion = tierra.comparar_distancia(marte)
        print(f"Resultado: {resultado_comparacion}")
        # Criterio: Tierra debe estar más cerca del Sol
        if "Tierra está más cerca" in resultado_comparacion:
             print("✅ Tierra está más cerca, criterio cumplido.")
        else:
             print("❌ Comparación incorrecta.")
    except Exception as e:
        print(f"❌ Error en la comparación: {e}")
    print("-" * 30)


    # --- Criterio 6: Intentar crear planeta con radio 0 o distancia negativa ---
    print("\n--- 6. Pruebas de Validación de Creación (Radio y Distancia) ---")
    try:
        # Intentar crear con radio 0
        Planeta("Planeta Malo 1", 1e20, 0, 1000)
    except ValidacionError as e:
        print(f"✅ Rechazo por radio 0: {e}")
        
    try:
        # Intentar crear con distancia negativa
        Planeta("Planeta Malo 2", 1e20, 1000, -500)
    except ValidacionError as e:
        print(f"✅ Rechazo por distancia negativa: {e}")
    print("-" * 30)


    # --- Criterio 7: Actualizar masa del planeta a un valor válido → se registra en historial ---
    print("\n--- 7. Actualización de Masa con Registro Historial ---")
    masa_original = tierra.masa_kg
    nueva_masa = 6.00e24 # Un valor ligeramente diferente
    
    print(f"Masa inicial de la Tierra: {masa_original:_.2e} kg")
    print(f"Número de modificaciones antes: {tierra.numero_modificaciones}")
    
    try:
        tierra.actualizar_masa(nueva_masa)
        print(f"✅ Masa actualizada a: {tierra.masa_kg:_.2e} kg")
        print(f"Número de modificaciones después: {tierra.numero_modificaciones}")
        
        # Consultar la ficha para ver el historial
        print("\n--- Ficha de la Tierra (Ver historial) ---")
        print(tierra.consultar_ficha())
        
        if tierra.numero_modificaciones > 0 and nueva_masa in [e['valor_nuevo'] for e in tierra.historial_eventos]:
            print("✅ Cambio de masa registrado correctamente en el historial.")
        else:
            print("❌ El cambio de masa no se registró en el historial.")
            
    except ValidacionError as e:
        print(f"❌ Error al actualizar masa: {e}")
    print("-" * 30)

    # --- Criterio 8: Intentar modificar atributos directamente sin operaciones ---
    print("\n--- 8. Pruebas de Encapsulamiento (Modificación Directa) ---")
    try:
        tierra._masa_kg = 100 # Intento de modificar directamente el atributo "privado"
        print("❌ PELIGRO: Se permitió la modificación directa de _masa_kg. (Aunque Python lo permite, la regla de negocio busca evitarlo, confiando en las operaciones).")
        # Se explica al estudiante: En Python, los atributos con _ son una CONVENCIÓN, no una restricción estricta.
        # Por eso, la regla de negocio debe ser reforzada usando SOLAMENTE las operaciones (métodos) públicos.
        print("💡 Nota para el estudiante: En Python, los atributos precedidos por '_' son solo una convención para indicar que NO DEBEN modificarse directamente.")
    except AttributeError:
        # Este error solo ocurre si se usa __ (dunder) que hace name mangling, no solo _
        print("✅ No se pudo modificar directamente (esperado en otros lenguajes, no en Python con solo un _) ")
        
    print(f"Masa actual de la Tierra después del intento: {tierra.masa_kg:_.2e} kg")
    # Intentemos con el nombre, que no tiene setter
    try:
        tierra.nombre = "Planeta X"
    except AttributeError:
        print("✅ No se puede asignar a 'nombre' directamente (es un @property solo de lectura).")
    print("-" * 30)


if __name__ == "__main__":
    ejecutar_pruebas()