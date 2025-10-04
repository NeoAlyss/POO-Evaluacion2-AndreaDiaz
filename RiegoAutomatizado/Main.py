from Clases.ParcelaConRiego import ParcelaConRiego

p1 = ParcelaConRiego(id_parcela=101, superficie_ha=10.50, cultivo_actual="Trigo")
print(f"\n--- 1. Parcela 101 Creada ---")
print(p1)

# 2. actualizar_cultivo("Maíz") registra en historial con fecha.
print(f"\n--- 2. Actualizar Cultivo ---")
p1.actualizar_cultivo("Maíz")

# 3. Asociar riego: tasa = 1500 L/ha, umbral = 2000 L; cargar_agua(20000).
print(f"\n--- 3. Configuración y Carga ---")
p1.configurar_tasa(1500)
p1.configurar_umbral(2000)
p1.cargar_agua(20000) # Saldo: 20000 L

# 4. regar_automatico(estricto) → demanda 15 750 L; aplica y deja saldo 4250 L (Verificación: 20000 - 15750 = 4250. 4250 >= 2000).
print(f"\n--- 4. Riego Estricto ---")
p1.regar_automatico("estricto")
print(f"✅ Saldo Actual P101: {p1.litrosDisponibles:.2f} L (Esperado: 4250.00 L)")

# 5. Desactivar parcela y luego intentar regar_automatico → rechazo con mensaje claro.
print(f"\n--- 5. Desactivar y Fallar Riego (Regla de Negocio) ---")
p1.desactivar("Prueba de rechazo por inactividad.") # Inhabilita automáticamente el riego.
p1.regar_automatico("estricto") # Debe ser rechazado.
print(f"Estado de Riego P101 después de desactivar: {p1.estadoRiego}")

# 7. Intentar fijar litros_disponibles por fuera de operaciones → imposible / error.
print(f"\n--- 7. Prueba de Encapsulamiento ---")
try:
    p1.__litros_disponibles = 50000
    print("❌ Error: Se pudo modificar el atributo privado, ¡Fallo el encapsulamiento!")
except AttributeError:
        print(f"✅ Intento de modificar litros_disponibles por acceso directo falló. Encapsulamiento OK.")
except Exception as e:
    print(f"✅ Intento de modificar litros_disponibles falló con error: {e}")

except ValueError as e:
    print(f"\n❌ ERROR CRÍTICO EN LA EJECUCIÓN (P101): {e}")

# --- PRUEBA 2: Parcela P102 (Modo Parcial) ---
print("\n" + "="*70)
try:
    # Creamos una nueva parcela para simular las condiciones exactas del test parcial.
    p2 = ParcelaConRiego(id_parcela=102, superficie_ha=10.50, cultivo_actual="Cebada")
    p2.configurar_tasa(1500)
    p2.configurar_umbral(2000)
    p2.cargar_agua(3000) # Saldo: 3000 L
    
    # 6. regar_automatico(parcial)
    # Demanda: 15750 L. Saldo antes: 3000 L. Umbral: 2000 L.
    # Máximo a usar (Parcial) = Saldo - Umbral = 3000 - 2000 = 1000 L.
    # Aplica 1000 L. Saldo final: 2000 L.
    print(f"\n--- 6. Riego Parcial ---")
    print(f"Saldo P102 antes: {p2.litrosDisponibles:.2f} L")
    p2.regar_automatico("parcial") 
    print(f"✅ Saldo Actual P102: {p2.litrosDisponibles:.2f} L (Esperado: 2000.00 L)")

except ValueError as e:
    print(f"\n❌ ERROR CRÍTICO EN LA EJECUCIÓN (P102): {e}")

# --- VERIFICACIÓN FINAL (Toda operación registrada) ---
print("\n" + "="*70)
print("### VERIFICACIÓN FINAL DE HISTORIALES ###")
mostrar_historiales(p1)
mostrar_historiales(p2)
print("\n=====================================================================")