import re
import json

def guardar_inventario(inv):
    with open("inventario.json", "w", encoding="utf-8") as f:
        json.dump(inv, f, indent=4)

def cargar_inventario():
    try:
        with open("inventario.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Stock inicial por defecto
        inv_inicial = [
            [1, "Samsung", "Galaxy S23", 1200000.0, 10],
            [2, "Apple", "iPhone 15", 1500000.0, 5],
            [3, "Motorola", "Edge 40", 800000.0, 15],
            [4, "Xiaomi", "Redmi Note 12", 500000.0, 20],
            [5, "Samsung", "Galaxy A54", 650000.0, 12]
        ]
        guardar_inventario(inv_inicial)
        return inv_inicial

# ==========================================
# ESTRUCTURAS DE DATOS AVANZADAS Y MATRICES
# ==========================================
# traigo el inventario
inventario = cargar_inventario()

carrito = []

# ==========================================
# EXCEPCIONES Y VALIDACION
# ==========================================
def validar_datos_usuario():
    print("\n--- Registro de Usuario ---")
    
    # valido el dni
    dni_valido = False
    dni = ""
    while not dni_valido:
        dni = input("Ingrese su DNI (sin puntos): ")
        try:
            int(dni) # trato de pasarlo a numero para ver si no puso letras
            if len(dni) == 7 or len(dni) == 8:
                dni_valido = True
            else:
                print("Error: DNI invalido. Debe contener 7 u 8 números.")
        except ValueError:
            print("Error: El DNI debe contener solo números.")

    # chequeo que el email este bien escrito 
    email_valido = False
    email = ""
    while not email_valido:
        email = input("Ingrese su correo electronico: ")
        
        # valido con regex que el correo sirva
        if re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            email_valido = True
            
            
            if re.search(r"@", email):
                pass
                
            
            partes = re.findall(r"[A-Za-z0-9._%+-]+|[A-Za-z0-9.-]+|[A-Za-z]{2,}", email)
            
            
            email_oculto = re.sub(r"^[A-Za-z0-9._%+-]+", "XXXX", email)
            
        else:
            print("Error: Correo electronico invalido. Intente nuevamente.")

    # compruebo que el telefono tenga los 10 numeros
    telefono_valido = False
    telefono = ""
    while not telefono_valido:
        telefono = input("Ingrese su telefono (10 digitos): ")
        try:
            int(telefono)
            if len(telefono) == 10:
                telefono_valido = True
            else:
                print("Error: Telefono invalido. Deben ser 10 números.")
        except ValueError:
            print("Error: El telefono debe contener solo números.")
        
    # armo la tupla y retorno los datos
    return (dni, email, telefono)

# ==========================================
# PROCESAMIENTO Y PROGRAMACION FUNCIONAL
# ==========================================

def mostrar_catalogo(lista_productos):
    print("\n--- Catalogo de Celulares ---")
    print(f"{'ID':<5} | {'Marca':<10} | {'Modelo':<15} | {'Precio':<12} | {'Stock':<5}")
    print("-" * 55)
    for prod in lista_productos:
        print(f"{prod[0]:<5} | {prod[1]:<10} | {prod[2]:<15} | ${prod[3]:<11} | {prod[4]:<5}")
def filtrar_por_precio():
    min_precio = float(input("\nPrecio minimo: "))
    max_precio = float(input("Precio maximo: "))
    
    # aplico un filtro rapido para buscar en el rango
    filtrados = list(filter(lambda x: min_precio <= x[3] <= max_precio, inventario))
    
    if filtrados:
        # ordeno de mas barato a mas caro
        filtrados.sort(key=lambda x: x[3])
        mostrar_catalogo(filtrados)
    else:
        print("No se encontraron celulares en ese rango de precio.")

def buscar_por_nombre():
    termino = input("\nIngrese la marca o modelo a buscar (ignorando mayúsculas): ").lower()
    
    # busco las coincidencias
    resultados = list(filter(lambda x: termino in x[1].lower() or termino in x[2].lower(), inventario))
    
    if resultados:
        mostrar_catalogo(resultados)
    else:
        print("No hay coincidencias.")

# ==========================================
# CARRITO Y COMPRAS
# ==========================================
def agregar_al_carrito():
    seguir = "s"
    while seguir == "s":
        mostrar_catalogo(inventario)
        
        id_prod_str = input("\nIngrese el ID del producto que desea agregar: ")
        cantidad_str = input("Ingrese la cantidad: ")
        
        try:
            id_prod = int(id_prod_str)
            cantidad = int(cantidad_str)
            
            encontrado = False
            for prod in inventario:
                if prod[0] == id_prod:
                    encontrado = True
                    if cantidad <= prod[4]:
                        # bajo el stock
                        prod[4] -= cantidad
                        guardar_inventario(inventario) # guardamos los cambios
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
            
        except ValueError:
            print("Entrada invalida . Ingrese solo números.")
            seguir = input("\n¿Desea intentar de nuevo? (s/n): ").lower()

def ver_carrito():
    if not carrito:
        print("\nEl carrito esta vacio.")
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
    base_nombre = f"recibo_{usuario[0]}"
    extension = ".txt"
    nombre_archivo = f"{base_nombre}{extension}"
    
    # si ya le generamos un recibo antes le sumo un numero al nombre
    contador = 1
    creado = False
    while not creado:
        try:
            # pruebo crear el txt
            with open(nombre_archivo, "x", encoding="utf-8") as f:
                f.write("=" * 40 + "\n")
                f.write(" RECIBO DE COMPRA - TIENDA DE CELULARES \n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Cliente DNI: {usuario[0]}\n")
                f.write(f"Email: {usuario[1]}\n")
                f.write(f"Telefono: {usuario[2]}\n\n")
                f.write("--- Detalle de la Compra ---\n")
                for item in carrito:
                    f.write(f"{item[2]}x {item[1]} - Precio Unitario: ${item[3]:.2f} - Subtotal: ${item[4]:.2f}\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total original: ${total:.2f}\n")
                f.write(f"Metodo de pago: {metodo_pago}\n")
                f.write(f"{detalles_pago}\n")
                f.write(f"TOTAL PAGADO: ${total_final:.2f}\n")
                f.write("=" * 40 + "\n")
                f.write(" ¡Gracias por su compra! \n")
            creado = True
        except FileExistsError:
            nombre_archivo = f"{base_nombre}_{contador}{extension}"
            contador += 1
            
    print(f"\n[+] Se ha generado un nuevo recibo: {nombre_archivo}")

def ver_compras(usuario):
    import re
    
    print("\n--- Mi Historial de Compras ---")
    print(f"{'Archivo':<25} | {'Productos Comprados':<40} | {'Total Pagado'}")
    print("-" * 85)
    
    compras_encontradas = False
    
    base_nombre = f"recibo_{usuario[0]}"
    extension = ".txt"
    nombre_archivo = f"{base_nombre}{extension}"
    contador = 1
    
    # busco en la carpeta todos los recibos que tengan mi dni
    buscando = True
    while buscando:
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                compras_encontradas = True
                contenido = f.read()
                items_match = re.search(r"--- Detalle de la Compra ---\n(.*?)\n-{10,}", contenido, re.DOTALL)
                total_match = re.search(r"TOTAL PAGADO: \$([0-9.]+)", contenido)
                
                if items_match and total_match:
                    lineas_items = items_match.group(1).strip().split('\n')
                    # saco los nombres 
                    productos = [linea.split(" - ")[0] for linea in lineas_items if linea]
                    resumen_productos = ", ".join(productos)
                    total = total_match.group(1)
                    
                    # corto el texto si es gigante para que no se deforme la tabla
                    if len(resumen_productos) > 37:
                        resumen_productos = resumen_productos[:34] + "..."
                        
                    print(f"{nombre_archivo:<25} | {resumen_productos:<40} | ${total}")
                else:
                    print(f"{nombre_archivo:<25} | (Recibo con formato antiguo o no reconocible)")
                    
            # Preparar siguiente nombre de archivo
            nombre_archivo = f"{base_nombre}_{contador}{extension}"
            contador += 1
            
        except FileNotFoundError:
            # Cuando ya no se encuentra el recibo, terminamos la busqueda
            buscando = False
        except IOError:
            print(f"{nombre_archivo:<25} | (Error al leer el recibo)")
            nombre_archivo = f"{base_nombre}_{contador}{extension}"
            contador += 1
                
    if not compras_encontradas:
        print("No tienes compras registradas aún.")

def procesar_pago(total, usuario):
    print("\n--- Checkout ---")
    respuesta = input("¿Posees un cupon de descuento magico? (s/n): ").lower()
    if respuesta == 's':
        codigo = input("Ingrese el codigo (escribe PROGRA10): ")
        if codigo.upper() == "PROGRA10":
            print("\n¡Cupon aceptado! Se aplica un 10% OFF en cada item .")
            # Uso map() para aplicar descuento al precio unitario y recalcular subtotal
            carrito[:] = list(map(lambda item: [item[0], item[1], item[2], item[3] * 0.9, (item[3] * 0.9) * item[2]], carrito))
            total = ver_carrito()
        else:
            print("Cupon invalido.")

    print("\n--- Metodos de Pago ---")
    print("1. Efectivo / Transferencia (15% de descuento sobre el total)")
    print("2. Tarjeta de Credito (Hasta 3 cuotas sin interes, 6 cuotas con 10% recargo)")
    
    opcion = input("Seleccione un metodo de pago: ")
    
    if opcion == "1":
        total_final = total * 0.85
        print(f"\nDescuento en efectivo aplicado. Total a pagar: ${total_final:.2f}")
        print("¡Compra realizada con exito!")
        print(f"Gracias por tu compra. Te enviaremos la factura al email: {usuario[1]}")
        generar_recibo_txt(usuario, "Efectivo / Transferencia", total, total_final, "Descuento 15% aplicado.")
        carrito.clear()
        
    elif opcion == "2":
        try:
            cuotas = int(input("Ingrese cantidad de cuotas (1, 3 o 6): "))
        except ValueError:
            print("Error: La cantidad de cuotas debe ser numerica. Cancelando pago...")
            return

        # Uso tupla para verificar cuotas validas
        if cuotas in (1, 3):
            valor_cuota = total / cuotas
            print(f"\nPagara el total en {cuotas} cuota(s) de ${valor_cuota:.2f} sin interes.")
            print("¡Compra realizada con exito!")
            print(f"Gracias por tu compra. Te enviaremos la factura al email: {usuario[1]}")
            generar_recibo_txt(usuario, "Tarjeta de Credito", total, total, f"{cuotas} cuota(s) sin interes.")
            carrito.clear()
        elif cuotas == 6:
            total_final = total * 1.10
            valor_cuota = total_final / cuotas
            print(f"\nRecargo aplicado. Pagara el total en {cuotas} cuotas de ${valor_cuota:.2f}.")
            print("¡Compra realizada con exito!")
            print(f"Gracias por tu compra. Te enviaremos la factura al email: {usuario[1]}")
            generar_recibo_txt(usuario, "Tarjeta de Credito", total, total_final, f"{cuotas} cuotas con 10% recargo.")
            carrito.clear()
        else:
            print("Cantidad de cuotas no valida. Cancelando pago...")
    else:
        print("Metodo de pago no reconocido.")

def agregar_producto_nuevo():
    print("\n--- Agregar Nuevo Producto ---")
    
    nuevo_id = max([p[0] for p in inventario]) + 1 if inventario else 1
    marca = input("Ingrese la marca del celular: ")
    modelo = input("Ingrese el modelo del celular: ")
    
    precio_valido = False
    while not precio_valido:
        try:
            precio = float(input("Ingrese el precio: "))
            if precio > 0:
                precio_valido = True
            else:
                print("Error: Precio invalido. Ingrese un numero positivo.")
        except ValueError:
            print("Error: Ingrese un valor numerico para el precio.")
            
    stock_valido = False
    while not stock_valido:
        try:
            stock = int(input("Ingrese el stock inicial: "))
            if stock >= 0:
                stock_valido = True
            else:
                print("Error: Stock invalido. Ingrese un numero positivo o cero.")
        except ValueError:
            print("Error: Ingrese un numero entero para el stock.")
            
    inventario.append([nuevo_id, marca, modelo, precio, stock])
    guardar_inventario(inventario)
    print(f"\n¡Producto '{marca} {modelo}' agregado con exito! (ID: {nuevo_id})")

# ==========================================
# MENÚ PRINCIPAL
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
        print("1. Ver catalogo completo")
        print("2. Buscar celular por nombre/marca")
        print("3. Filtrar celulares por precio")
        print("4. Agregar producto al carrito")
        print("5. Ver carrito")
        print("6. Finalizar Compra (Checkout)")
        print("7. Agregar producto al catalogo")
        print("8. Ver mis compras")
        print("9. Salir")
        
        try:
            opcion = int(input("Seleccione una opcion: "))
            
            if opcion == 1:
                mostrar_catalogo(inventario)
            elif opcion == 2:
                buscar_por_nombre()
            elif opcion == 3:
                filtrar_por_precio()
            elif opcion == 4:
                agregar_al_carrito()
            elif opcion == 5:
                ver_carrito()
            elif opcion == 6:
                total = ver_carrito()
                if total:
                    procesar_pago(total, usuario)
            elif opcion == 7:
                agregar_producto_nuevo()
            elif opcion == 8:
                ver_compras(usuario)
            elif opcion == 9:
                print("Gracias por visitar nuestra tienda. ¡Hasta luego!")
                continuar = False
            else:
                print("Opcion invalida. Intente de nuevo.")
        except ValueError:
            print("Error: Ingreso no valido. Por favor ingrese el numero de la opcion deseada.")

if __name__ == "__main__":
    menu_principal()
