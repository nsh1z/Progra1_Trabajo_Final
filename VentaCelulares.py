import re
import json

# ==========================================
# 1. ESTRUCTURAS DE DATOS AVANZADAS Y MATRICES
# ==========================================
def guardar_inventario(inv):
    with open("inventario.json", "w", encoding="utf-8") as f:
        json.dump(inv, f, indent=4)

def cargar_inventario():
    try:
        with open("inventario.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        inv_inicial = [
            [1, "Samsung", "Galaxy S23", 1200000.0, 10],
            [2, "Apple", "iPhone 15", 1500000.0, 5],
            [3, "Motorola", "Edge 40", 800000.0, 15],
            [4, "Xiaomi", "Redmi Note 12", 500000.0, 20],
            [5, "Samsung", "Galaxy A54", 650000.0, 12]
        ]
        guardar_inventario(inv_inicial)
        return inv_inicial

# traigo el inventario
inventario = cargar_inventario()

# preparo el carrito vacio
carrito = []

# ==========================================
# 2. EXPRESIONES REGULARES Y VALIDACIÓN
# ==========================================
def validar_datos_usuario():
    print("\n--- Registro de Usuario ---")
    
    # valido el dni
    dni_valido = False
    dni = ""
    while not dni_valido:
        dni = input("Ingrese su DNI (sin puntos): ")
        if dni.isdigit() and (len(dni) == 7 or len(dni) == 8):
            dni_valido = True
        else:
            print("Error: DNI inválido. Debe contener 7 u 8 números.")

    # chequeo que el email este bien escrito
    email_valido = False
    email = ""
    while not email_valido:
        email = input("Ingrese su correo electronico: ")
        if re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            email_valido = True
        else:
            print("Error: El correo no tiene un formato valido.")

    # compruebo que el telefono tenga los 10 numeros
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
    
    # aplico un filtro rapido para buscar en el rango
    filtrados = list(filter(lambda x: min_precio <= x[3] <= max_precio, inventario))
    
    if filtrados:
        filtrados.sort(key=lambda x: x[3])
        mostrar_catalogo(filtrados)
    else:
        print("No se encontraron celulares en ese rango de precio.")

def buscar_por_nombre():
    termino = input("\nIngrese la marca o modelo a buscar: ").lower()
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
            print("Entrada invalida. Por favor, ingresa solo numeros.")
            seguir = input("\n¿Desea intentar de nuevo? (s/n): ").lower()
            continue

        encontrado = False
        for prod in inventario:
            if prod[0] == id_prod:
                encontrado = True
                if cantidad <= prod[4]:
                    prod[4] -= cantidad
                    guardar_inventario(inventario) # actualizo el json
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

def generar_recibo_txt(usuario, metodo_pago, total, total_final, detalles_pago):
    base_nombre = f"recibo_{usuario['dni']}"
    extension = ".txt"
    nombre_archivo = f"{base_nombre}{extension}"
    
    contador = 1
    creado = False
    while not creado:
        try:
            with open(nombre_archivo, "x", encoding="utf-8") as f:
                f.write(f"Cliente DNI: {usuario['dni']}\n")
                f.write(f"Email: {usuario['email']}\n\n")
                f.write(f"TOTAL PAGADO: ${total_final:.2f}\n")
            creado = True
        except FileExistsError:
            nombre_archivo = f"{base_nombre}_{contador}{extension}"
            contador += 1
            
    print(f"\n[+] Se ha generado un nuevo recibo: {nombre_archivo}")

def procesar_pago(total, usuario):
    print("\n--- Checkout ---")
    respuesta = input("¿Posees un cupón de descuento mágico? (s/n): ").lower()
    if respuesta == 's':
        codigo = input("Ingrese el código (escribe PROGRA10): ")
        if codigo.upper() == "PROGRA10":
            print("\n¡Cupón aceptado! Se aplica un 10% OFF en cada ítem.")
            carrito[:] = list(map(lambda item: [item[0], item[1], item[2], item[3] * 0.9, (item[3] * 0.9) * item[2]], carrito))
            total = ver_carrito()
        else:
            print("Cupón inválido.")

    print("\n--- Métodos de Pago ---")
    print("1. Efectivo / Transferencia")
    print("2. Tarjeta de Crédito")
    
    opcion = input("Seleccione un método de pago: ")
    
    if opcion == "1":
        total_final = total * 0.85
        print(f"\nTotal a pagar: ${total_final:.2f}")
        print(f"Factura enviada al email: {usuario['email']}")
        carrito.clear()
        
    elif opcion == "2":
        cuotas = int(input("Ingrese cantidad de cuotas (1, 3 o 6): "))
        if cuotas in [1, 3]:
            valor_cuota = total / cuotas
            print(f"\n{cuotas} cuota(s) de ${valor_cuota:.2f} sin interés.")
            carrito.clear()
        elif cuotas == 6:
            total_final = total * 1.10
            valor_cuota = total_final / cuotas
            print(f"\n{cuotas} cuotas de ${valor_cuota:.2f}.")
            carrito.clear()
        else:
            print("Cuotas no válidas.")
    else:
        print("Método no reconocido.")

def ver_compras(usuario):
    print("\n--- Mi Historial de Compras ---")
    base_nombre = f"recibo_{usuario['dni']}"
    extension = ".txt"
    nombre_archivo = f"{base_nombre}{extension}"
    contador = 1
    buscando = True
    while buscando:
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                print(f"Recibo encontrado: {nombre_archivo}")
            nombre_archivo = f"{base_nombre}_{contador}{extension}"
            contador += 1
        except FileNotFoundError:
            buscando = False

def menu_principal():
    usuario = validar_datos_usuario()
    continuar = True
    while continuar:
        print("\n1. Ver catálogo\n2. Buscar\n3. Filtrar\n4. Agregar al carrito\n5. Ver carrito\n6. Pagar\n7. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1": mostrar_catalogo(inventario)
        elif opcion == "2": buscar_por_nombre()
        elif opcion == "3": filtrar_por_precio()
        elif opcion == "4": agregar_al_carrito()
        elif opcion == "5": ver_carrito()
        elif opcion == "6": 
            total = ver_carrito()
            if total: procesar_pago(total, usuario)
        elif opcion == "7": continuar = False

if __name__ == "__main__":
    menu_principal()
