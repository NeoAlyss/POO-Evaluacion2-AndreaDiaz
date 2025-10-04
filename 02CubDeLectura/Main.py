# Criterios de aceptación mínimos.
    # Crear publicación "Don Quijote" con año 1605. OK
    # Intentar crear publicación con año 1400 → rechazo OK
    # Crear libro "Cien años de soledad" con 500 páginas. OK
    # leer(120) → paginas_leidas = 120, progreso = 24%.
    # leer(400) → rechazo, no puede superar total.
    # consultar_progreso() muestra porcentaje redondeado. OK
    # actualizar_anio(1967) en el libro → cambio válido, queda en historial_eventos. OK
    # Todo intento de alterar paginas_leidas o paginas_totales directamente debe ser imposible (error o rechazo). OK

"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

from Clases.Publicacion import Publicacion
from Clases.Libro import Libro

publicacion1 = Publicacion(1, "Don Quijote", 1605)
print(f"Publicación creada: {publicacion1.titulo}, Año: {publicacion1.anio}")

try:
    publicacionInvalida = Publicacion(1, "Publicación Inválida", 1400)
except Exception as e:
    print(f"Error al crear publicación: {e}")

libro1 = Libro(2, "Cien años de soledad", 1967, 500)

try:
    libro1.leer(120)
    progreso = libro1.consultar_progreso()
    print(f"Páginas leídas: {libro1.paginasLeidas}, Progreso: {progreso:.2f}%")
    
    libro1.leer(400)  # Esto debería ser rechazado
except Exception as e:
    print(f"Error al leer páginas: {e}")

libro1.actualizar_anio(2025)
print(f"Año actualizado: {libro1.anio}")

libro1.consultar_progreso()
print(f"Progreso actual: {libro1.consultar_progreso():.2f}%")

try:
    libro1.paginasLeidas = 300  # Intento de alterar directamente (debe fallar)
except AttributeError as e:
    print(f"Error al modificar páginas leídas directamente: {e}")



