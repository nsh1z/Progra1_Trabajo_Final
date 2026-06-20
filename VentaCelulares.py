
# ==========================================
# 1. ESTRUCTURAS DE DATOS AVANZADAS Y MATRICES
# ==========================================
# Matriz de stock pre-cargado: [ID, Marca, Modelo, Precio, Stock]
inventario = [
    [1, "Samsung", "Galaxy S23", 1200000, 10],
    [2, "Apple", "iPhone 15", 1500000, 5],
    [3, "Motorola", "Edge 40", 800000, 15],
    [4, "Xiaomi", "Redmi Note 12", 500000, 20],
    [5, "Samsung", "Galaxy A54", 650000, 12]
]

# Lista anidada para el carrito: [ID_Producto, Modelo, Cantidad, Precio_Unitario, Subtotal]
carrito = []

# ==========================================
# 2. EXPRESIONES REGULARES Y VALIDACIÓN
# ==========================================
def validar_datos_usuario():
    print("\n--- Registro de Usuario ---")
    
    # Validar DNI (7 u 8 dígitos) sin usar break
    dni_valido = False
    dni = ""
    while not dni_valido:
        dni = input("Ingrese su DNI (sin puntos): ")
        if dni.isdigit() and (len(dni) == 7 or len(dni) == 8):
            dni_valido = True
        else:
            print("Error: DNI inválido. Debe contener 7 u 8 números.")

    # Validar Email sin usar break
    email_valido = False
    email = ""
    while not email_valido:
        email = input("Ingrese su correo electrónico: ")
        if "@" in email and "." in email.split("@")[-1] and len(email) > 5:
            email_valido = True
        else:
            print("Error: Correo electrónico inválido.")

    # Validar Teléfono (10 dígitos) sin usar break
    telefono_valido = False
    telefono = ""
    while not telefono_valido:
        telefono = input("Ingrese su teléfono (10 dígitos): ")
        if telefono.isdigit() and len(telefono) == 10:
            telefono_valido = True
        else:
            print("Error: Teléfono inválido. Deben ser 10 números.")
        
    return {"dni": dni, "email": email, "telefono": telefono}

# ==========================================
# 3. PROCESAMIENTO Y PROGRAMACIÓN FUNCIONAL
# ==========================================

def mostrar_catalogo(lista_productos):
    print("\n--- Catálogo de Celulares ---")
    print(f"{'ID':<5} | {'Marca':<10} | {'Modelo':<15} | {'Precio':<12} | {'Stock':<5}")
    print("-" * 55)
    for prod in lista_productos:
        print(f"{prod[0]:<5} | {prod[1]:<10} | {prod[2]:<15} | ${prod[3]:<11} | {prod[4]:<5}")

def filtrar_por_precio():
    min_precio = float(input("\nPrecio mínimo: "))
    max_precio = float(input("Precio máximo: "))
    
    # Uso de filter() y lambda
    filtrados = list(filter(lambda x: min_precio <= x[3] <= max_precio, inventario))
    
    if filtrados:
        # Ordenar por precio (menor a mayor) usando sort y lambda
        filtrados.sort(key=lambda x: x[3])
        mostrar_catalogo(filtrados)
    else:
        print("No se encontraron celulares en ese rango de precio.")

def buscar_por_nombre():
    termino = input("\nIngrese la marca o modelo a buscar (ignorando mayúsculas): ").lower()
    
    # Procesamiento de texto y uso de filter()
    resultados = list(filter(lambda x: termino in x[1].lower() or termino in x[2].lower(), inventario))
    
    if resultados:
        mostrar_catalogo(resultados)
    else:
        print("No hay coincidencias.")

# ==========================================
# 4. CARRITO Y COMPRAS
# ==========================================
def agregar_al_carrito():
    seguir = "s"
    while seguir == "s":
        mostrar_catalogo(inventario)
        try:
            id_prod = int(input("\nIngrese el ID del producto que desea agregar: "))
            cantidad = int(input("Ingrese la cantidad: "))
        except ValueError:
            print("Entrada inválida. Ingrese números.")
            seguir = input("\n¿Desea intentar de nuevo? (s/n): ").lower()
            continue

        encontrado = False
        for prod in inventario:
            if prod[0] == id_prod:
                encontrado = True
                if cantidad <= prod[4]:
                    # Actualizar stock
                    prod[4] -= cantidad
                    subtotal = prod[3] * cantidad
                    carrito.append([prod[0], prod[2], cantidad, prod[3], subtotal])
                    print(f"\n¡{cantidad} x {prod[2]} agregado(s) al carrito!")
                else:
                    print("\nError: No hay suficiente stock disponible.")
                
        if not encontrado:
            print("\nError: ID de producto no encontrado.")
            
        print("\n--- Estado de tu carrito ---")
        ver_carrito()
        seguir = input("\n¿Desea seguir agregando productos? (s/n): ").lower()

def ver_carrito():
    if not carrito:
        print("\nEl carrito está vacío.")
        return False
    
    print("\n--- Mi Carrito ---")
    total = 0
    for item in carrito:
        print(f"{item[2]}x {item[1]} - Precio Unitario: ${item[3]} - Subtotal: ${item[4]}")
        total += item[4]
        
    print("-" * 30)
    print(f"TOTAL: ${total}")
    return total

def procesar_pago(total, usuario):
    print("\n--- Checkout ---")
    respuesta = input("¿Posees un cupón de descuento mágico? (s/n): ").lower()
    if respuesta == 's':
        codigo = input("Ingrese el código (escribe PROGRA10): ")
        if codigo.upper() == "PROGRA10":
            print("\n¡Cupón aceptado! Se aplica un 10% OFF en cada ítem (Demostración map).")
            # Uso de map() para aplicar descuento al precio unitario y recalcular subtotal
            carrito[:] = list(map(lambda item: [item[0], item[1], item[2], item[3] * 0.9, (item[3] * 0.9) * item[2]], carrito))
            total = ver_carrito()
        else:
            print("Cupón inválido.")

    print("\n--- Métodos de Pago ---")
    print("1. Efectivo / Transferencia (15% de descuento sobre el total)")
    print("2. Tarjeta de Crédito (Hasta 3 cuotas sin interés, 6 cuotas con 10% recargo)")
    
    opcion = input("Seleccione un método de pago: ")
    
    if opcion == "1":
        total_final = total * 0.85
        print(f"\nDescuento en efectivo aplicado. Total a pagar: ${total_final:.2f}")
        print("¡Compra realizada con éxito!")
        print(f"Gracias por tu compra. Te enviaremos la factura al email: {usuario['email']}")
        carrito.clear()
        
    elif opcion == "2":
        cuotas = int(input("Ingrese cantidad de cuotas (1, 3 o 6): "))
        if cuotas in [1, 3]:
            valor_cuota = total / cuotas
            print(f"\nPagará el total en {cuotas} cuota(s) de ${valor_cuota:.2f} sin interés.")
            print("¡Compra realizada con éxito!")
            print(f"Gracias por tu compra. Te enviaremos la factura al email: {usuario['email']}")
            carrito.clear()
        elif cuotas == 6:
            total_final = total * 1.10
            valor_cuota = total_final / cuotas
            print(f"\nRecargo aplicado. Pagará el total en {cuotas} cuotas de ${valor_cuota:.2f}.")
            print("¡Compra realizada con éxito!")
            print(f"Gracias por tu compra. Te enviaremos la factura al email: {usuario['email']}")
            carrito.clear()
        else:
            print("Cantidad de cuotas no válida. Cancelando pago...")
    else:
        print("Método de pago no reconocido.")

# ==========================================
# 5. MENÚ PRINCIPAL E INTERFAZ (UI)
# ==========================================
def menu_principal():
    print("=" * 40)
    print(" BIENVENIDO A LA TIENDA DE CELULARES ")
    print("=" * 40)
    
    usuario = validar_datos_usuario()
    print(f"\n¡Bienvenido/a! Datos verificados correctamente.")

    continuar = True
    while continuar:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Ver catálogo completo")
        print("2. Buscar celular por nombre/marca")
        print("3. Filtrar celulares por precio")
        print("4. Agregar producto al carrito")
        print("5. Ver carrito")
        print("6. Finalizar Compra (Checkout)")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            mostrar_catalogo(inventario)
        elif opcion == "2":
            buscar_por_nombre()
        elif opcion == "3":
            filtrar_por_precio()
        elif opcion == "4":
            agregar_al_carrito()
        elif opcion == "5":
            ver_carrito()
        elif opcion == "6":
            total = ver_carrito()
            if total:
                procesar_pago(total, usuario)
        elif opcion == "7":
            print("Gracias por visitar nuestra tienda. ¡Hasta luego!")
            continuar = False
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
