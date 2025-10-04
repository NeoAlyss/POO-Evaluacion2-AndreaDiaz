from Clases.Publicacion import Publicacion, PublicacionException
from Clases.Libro import Libro
import sys

def separador(titulo):
    """Función de ayuda para mejorar la legibilidad de la salida en consola."""
    print("\n" + "=" * 50)
    print(f"--- {titulo} ---")
    print("=" * 50)

def main():
    """
    Función principal que implementa los criterios de aceptación del ejercicio.
    """
    
    # 1. Crear publicación "Don Quijote" con año 1605.
    separador("1. Creación de Publicación Válida (Don Quijote)")
    try:
        don_quijote = Publicacion(
            id_publicacion="DQ1605", 
            titulo="El ingenioso hidalgo Don Quijote de la Mancha", 
            anio=1605
        )
        print(f"Publicación creada: {don_quijote.titulo} ({don_quijote.anio})")
        
        # Muestra el historial inicial
        print(f"Total de eventos en historial: {len(don_quijote.historial_eventos)}")

    except PublicacionException as e:
        print(f"[ERROR FATAL] Fallo inesperado al crear Quijote: {e}")
        return


    # 2. Intentar crear publicación con año 1400 -> rechazo.
    separador("2. Intento de Creación de Publicación con Año Inválido (1400)")
    try:
        Publicacion(id_publicacion="M1400", titulo="Manuscrito Antiguo", anio=1400)
        print("[ERROR] No se lanzó la excepción de año inválido.")
    except PublicacionException as e:
        print(f"[VALIDACIÓN EXITOSA] Rechazo por regla de negocio: {e}")


    # 3. Crear libro "Cien años de soledad" con 500 páginas.
    separador("3. Creación de Libro Válido (Cien Años de Soledad)")
    try:
        cien_anios = Libro(
            id_publicacion="CAS1967", 
            titulo="Cien años de soledad", 
            anio=1967, 
            paginas_totales=500
        )
        print(f"Libro creado: {cien_anios.titulo} | Páginas Totales: {cien_anios.paginas_totales}")
        print(f"Páginas Leídas: {cien_anios.paginas_leidas} | Progreso: {cien_anios.consultar_progreso()}%")
    except PublicacionException as e:
        print(f"[ERROR FATAL] Fallo inesperado al crear Libro: {e}")
        return
        

    # 4. leer(120) -> paginas_leidas = 120, progreso = 24%.
    separador("4. Operación: leer(120)")
    try:
        cien_anios.leer(120)
        print(f"Páginas Leídas (Esperado 120): {cien_anios.paginas_leidas}")
        print(f"Progreso (Esperado 24.0%): {cien_anios.consultar_progreso()}%")
        # Mostrar último evento de lectura
        print(f"Último evento de lectura: {cien_anios.eventos_lectura[-1]['descripcion']}")
    except PublicacionException as e:
        print(f"[ERROR] Fallo al leer 120 páginas: {e}")


    # 5. leer(400) -> rechazo, no puede superar total.
    separador("5. Operación: Intentar leer(400) - Excede el total restante")
    try:
        # Páginas restantes: 500 - 120 = 380. 400 excede.
        cien_anios.leer(400)
        print("[ERROR] No se lanzó la excepción de lectura excesiva.")
    except PublicacionException as e:
        print(f"[VALIDACIÓN EXITOSA] Rechazo por regla de negocio: {e}")
        print(f"Páginas Leídas siguen en: {cien_anios.paginas_leidas}")

    # Continuamos la lectura hasta el final
    separador("6. Continuar la lectura hasta el 100%")
    try:
        cien_anios.leer(380) # Leemos las 380 páginas restantes
        print(f"Páginas Leídas (Esperado 500): {cien_anios.paginas_leidas}")
        print(f"Progreso (Esperado 100.0%): {cien_anios.consultar_progreso()}%")
    except PublicacionException as e:
        print(f"[ERROR] Fallo al completar la lectura: {e}")


    # 7. actualizar_anio(1967) en el libro -> cambio válido, queda en historial_eventos.
    separador("7. Operación: actualizar_anio(1967) y verificar historial")
    try:
        # El año ya es 1967, probemos con otro año válido para ver el cambio en el historial
        print(f"Año anterior: {cien_anios.anio}")
        cien_anios.actualizar_anio(1970)
        print(f"Año nuevo: {cien_anios.anio}")
        
        # El historial de eventos de la clase Publicacion DEBE tener ahora 2 eventos (creación + cambio de año)
        print(f"Total de eventos en historial: {len(cien_anios.historial_eventos)}")
        print("Último evento de historial:")
        print(cien_anios.historial_eventos[-1])
        
    except PublicacionException as e:
        print(f"[ERROR] Fallo al actualizar el año: {e}")


    # 8. Intento de alteración directa (Rechazo/Imposible).
    separador("8. Intento de alteración directa de campos (Ej. paginas_leidas)")
    try:
        # Intentar acceder al atributo privado (protegido por convención)
        cien_anios._paginas_leidas = 999 
        print(f"[PELIGRO] Se alteró directamente el valor a {cien_anios._paginas_leidas} (Esto es mala práctica y se debe evitar).")
    except AttributeError:
        # Esto no siempre falla en Python, pero si usamos la propiedad pública, no se puede
        print("No se puede acceder a la propiedad con el decorador @property")

    try:
        # Intentar modificar una propiedad que solo tiene 'getter'
        cien_anios.paginas_leidas = 999 
        print("[ERROR] No se lanzó el AttributeError (setter no definido).")
    except AttributeError as e:
        print(f"[VALIDACIÓN EXITOSA] No se puede alterar 'paginas_leidas' directamente: {e}")
    
    try:
        # Intentar modificar paginas_totales (no tiene setter)
        cien_anios.paginas_totales = 1000 
        print("[ERROR] No se lanzó el AttributeError (setter no definido) para paginas_totales.")
    except AttributeError as e:
        print(f"[VALIDACIÓN EXITOSA] No se puede alterar 'paginas_totales' directamente: {e}")
        
    print("\n--- Demostración Finalizada ---")


if __name__ == "__main__":
    main()
