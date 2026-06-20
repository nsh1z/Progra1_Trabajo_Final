import re
import json
import unittest

def guardar_inventario(inv):
    with open("inventario.json", "w", encoding="utf-8") as f:
        json.dump(inv, f, indent=4)

def cargar_inventario():
    try:
        with open("inventario.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Requisito Diccionarios: convertimos las claves de string a int
            return {int(k): v for k, v in data.items()}
    except FileNotFoundError:
        # Stock inicial por defecto adaptado a diccionario (Requisito Parte 2)
        inv_inicial = {
            1: {"marca": "Samsung", "modelo": "Galaxy S23", "precio": 1200000.0, "stock": 10},
            2: {"marca": "Apple", "modelo": "iPhone 15", "precio": 1500000.0, "stock": 5},
            3: {"marca": "Motorola", "modelo": "Edge 40", "precio": 800000.0, "stock": 15},
            4: {"marca": "Xiaomi", "modelo": "Redmi Note 12", "precio": 500000.0, "stock": 20},
            5: {"marca": "Samsung", "modelo": "Galaxy A54", "precio": 650000.0, "stock": 12}
        }
        guardar_inventario(inv_inicial)
        return inv_inicial
    except (ValueError, json.JSONDecodeError):
        return {}

# ==========================================
# ESTRUCTURAS DE DATOS AVANZADAS Y MATRICES
# ==========================================
# traigo el inventario
inventario = cargar_inventario()

carrito = []

# Requisito Conjuntos (Sets): para validar elementos al hacer altas
marcas_permitidas = {"Samsung", "Apple", "Motorola", "Xiaomi", "Nokia", "LG"}

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
        if not dni.strip():
            print("Error: El DNI no puede estar vacio.")
            continue
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
        
    # armo la tupla y retorno los datos (Requisito Tuplas)
    return (dni, email, telefono)

# ==========================================
# PROCESAMIENTO Y PROGRAMACION FUNCIONAL
# ==========================================

def mostrar_catalogo(dicc_productos=None):
    if dicc_productos is None:
        dicc_productos = inventario
        
    print("\n--- Catalogo de Celulares ---")
    print(f"{'ID':<5} | {'Marca':<10} | {'Modelo':<15} | {'Precio':<12} | {'Stock':<5}")
    print("-" * 55)
    for id_prod, datos in dicc_productos.items():
        print(f"{id_prod:<5} | {datos['marca']:<10} | {datos['modelo']:<15} | ${datos['precio']:<11} | {datos['stock']:<5}")

def filtrar_por_precio():
    try:
        min_precio = float(input("\nPrecio minimo: "))
        max_precio = float(input("Precio maximo: "))
        
        # aplico un filtro rapido para buscar en el rango usando comprension de diccionarios
        filtrados = {k: v for k, v in inventario.items() if min_precio <= v["precio"] <= max_precio}
        
        if filtrados:
            mostrar_catalogo(filtrados)
        else:
            print("No se encontraron celulares en ese rango de precio.")
    except ValueError:
        print("Entrada invalida. Ingresa solo numeros.")

def buscar_por_nombre():
    termino = input("\nIngrese la marca o modelo a buscar (ignorando mayúsculas): ").lower()
    
    # busco las coincidencias
    resultados = {k: v for k, v in inventario.items() if termino in v["marca"].lower() or termino in v["modelo"].lower()}
    
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
            
            if id_prod in inventario:
                if cantidad <= inventario[id_prod]["stock"]:
                    # bajo el stock
                    inventario[id_prod]["stock"] -= cantidad
                    guardar_inventario(inventario) # guardamos los cambios
                    subtotal = inventario[id_prod]["precio"] * cantidad
                    # Requisito Tuplas: la info no debe modificarse una vez en el carrito
                    item = (id_prod, inventario[id_prod]["marca"], inventario[id_prod]["modelo"], cantidad, inventario[id_prod]["precio"], subtotal)
                    carrito.append(item)
                    print(f"\n¡{cantidad} x {inventario[id_prod]['modelo']} agregado(s) al carrito!")
                else:
                    print("\nError: No hay suficiente stock disponible.")
            else:
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
        print(f"{item[3]}x {item[1]} {item[2]} - Precio Unitario: ${item[4]} - Subtotal: ${item[5]}")
        total += item[5]
        
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
                    f.write(f"{item[3]}x {item[1]} {item[2]} - Precio Unitario: ${item[4]:.2f} - Subtotal: ${item[5]:.2f}\n")
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
            for i in range(len(carrito)):
                item = carrito[i]
                nuevo_precio = item[4] * 0.9
                nuevo_subtotal = item[3] * nuevo_precio
                carrito[i] = (item[0], item[1], item[2], item[3], nuevo_precio, nuevo_subtotal)
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

# ==========================================
# ABM (ALTAS, BAJAS, MODIFICACIONES)
# ==========================================
def agregar_producto_nuevo():
    print("\n--- Agregar Nuevo Producto ---")
    print(f"Marcas permitidas: {', '.join(marcas_permitidas)}")
    
    nuevo_id = max(inventario.keys()) + 1 if inventario else 1
    
    marca_valida = False
    while not marca_valida:
        marca = input("Ingrese la marca del celular: ").strip().capitalize()
        # Requisito Conjuntos: validacion
        if marca in marcas_permitidas:
            marca_valida = True
        else:
            print("Error: Marca no reconocida. Intente de nuevo.")
            
    modelo = input("Ingrese el modelo del celular: ").strip()
    
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
            
    inventario[nuevo_id] = {
        "marca": marca,
        "modelo": modelo,
        "precio": precio,
        "stock": stock
    }
    guardar_inventario(inventario)
    print(f"\n¡Producto '{marca} {modelo}' agregado con exito! (ID: {nuevo_id})")

def baja_producto():
    print("\n--- Baja de Producto ---")
    try:
        id_baja = int(input("Ingrese el ID del producto a eliminar: "))
        if id_baja in inventario:
            eliminado = inventario.pop(id_baja)
            guardar_inventario(inventario)
            print(f"Producto '{eliminado['marca']} {eliminado['modelo']}' eliminado del sistema.")
        else:
            print("Error: No se encontro ningun producto con ese ID.")
    except ValueError:
        print("Error: Ingrese un numero valido.")

def modificacion_producto():
    print("\n--- Modificación de Producto ---")
    try:
        id_mod = int(input("Ingrese el ID del producto a modificar: "))
        if id_mod in inventario:
            print(f"Modificando: {inventario[id_mod]['marca']} {inventario[id_mod]['modelo']}")
            print("Deje en blanco para no modificar el valor actual.")
            
            nuevo_precio = input(f"Nuevo precio (actual {inventario[id_mod]['precio']}): ").strip()
            if nuevo_precio:
                try:
                    p = float(nuevo_precio)
                    if p > 0:
                        inventario[id_mod]["precio"] = p
                        print("Precio actualizado.")
                    else:
                        print("Error: El precio debe ser positivo.")
                except ValueError:
                    print("Error: Precio no valido.")

            nuevo_stock = input(f"Nuevo stock (actual {inventario[id_mod]['stock']}): ").strip()
            if nuevo_stock:
                try:
                    s = int(nuevo_stock)
                    if s >= 0:
                        inventario[id_mod]["stock"] = s
                        print("Stock actualizado.")
                    else:
                        print("Error: El stock no puede ser negativo.")
                except ValueError:
                    print("Error: Stock no valido.")
            guardar_inventario(inventario)
        else:
            print("Error: No se encontro ningun producto con ese ID.")
    except ValueError:
        print("Error: Ingrese un numero valido.")

# ==========================================
# PRUEBAS UNITARIAS (Requisito Parte 2)
# ==========================================
class PruebasSistema(unittest.TestCase):
    def test_descuento_efectivo(self):
        # Prueba que el calculo de 15% de descuento sea correcto
        total = 1000
        total_final = total * 0.85
        self.assertEqual(total_final, 850.0)

    def test_recargo_tarjeta(self):
        # Prueba que el recargo del 10% sea correcto
        total = 1000
        total_final = total * 1.10
        self.assertEqual(total_final, 1100.0)

def ejecutar_pruebas():
    print("\n--- Ejecutando Pruebas Unitarias ---")
    suite = unittest.TestLoader().loadTestsFromTestCase(PruebasSistema)
    unittest.TextTestRunner(verbosity=2).run(suite)

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
        print("7. Agregar producto al catalogo (Alta)")
        print("8. Ver mis compras")
        print("9. Eliminar producto del catalogo (Baja)")
        print("10. Modificar producto del catalogo")
        print("11. Ejecutar Pruebas Unitarias")
        print("12. Salir")
        
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
                baja_producto()
            elif opcion == 10:
                modificacion_producto()
            elif opcion == 11:
                ejecutar_pruebas()
            elif opcion == 12:
                print("Gracias por visitar nuestra tienda. ¡Hasta luego!")
                continuar = False
            else:
                print("Opcion invalida. Intente de nuevo.")
        except ValueError:
            print("Error: Ingreso no valido. Por favor ingrese el numero de la opcion deseada.")

if __name__ == "__main__":
    menu_principal()
