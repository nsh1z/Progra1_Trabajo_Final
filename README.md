# Tienda de Celulares - Trabajo Final 📱
Este es nuestro trabajo final para la materia de Algoritmos. Es un sistema de gestión para una tienda de celulares por consola escrito en Python. 
El programa permite ver un catálogo de celulares, buscar por marca o precio, agregar cosas al carrito y generar una compra final con su recibo correspondiente.

## Funcionalidades principales
- **Catálogo e Inventario:** El stock de los celulares se guarda de forma persistente en un archivo `inventario.json`. Si compras un celular, el stock baja automáticamente.
- **Validación de Usuarios:** Te pide DNI, email y teléfono antes de comprar. Usamos **Expresiones Regulares (regex)** para asegurar que el mail tenga un formato válido (`@` y `.com`).
- **Carrito de Compras:** Podés ir agregando celulares. Si no hay stock suficiente, te avisa.
- **Generación de Recibos:** Al finalizar la compra, el programa te genera un archivo `.txt` con el resumen de todo lo que pagaste, a modo de factura.
- **Historial de Compras:** El sistema puede leer los `.txt` generados para mostrarte un historial de todo lo que compraste con tu DNI.

## ¿Cómo ejecutarlo?
1. Descargá o cloná este repositorio en tu computadora.
2. Asegurate de tener instalado Python.
3. Abrí una terminal, entrá a la carpeta del proyecto y corré el siguiente comando:
```bash
python trabajo_final.py
```
> **Nota:** Es importante ejecutarlo estando dentro de la misma carpeta para que el `inventario.json` y los recibos `.txt` se guarden en el lugar correcto.

---

## Trabajo Práctico Integrador – Parte 2
**Materia:** Programación 1 / Algoritmo y Estructura de Datos 1
**Profesores:** Lic. Gustavo E. Escandell / Ing. Melinda L. Selles

### Explicación de implementación de requisitos obligatorios:

#### • ¿Dónde utilizamos diccionarios?
Toda la estructura base de nuestra tienda (el inventario) está almacenada en memoria como un diccionario. La clave del diccionario principal es el ID numérico único del producto, y su valor correspondiente es un diccionario anidado que contiene toda su información detallada: `{"marca": "...", "modelo": "...", "precio": float, "stock": int}`.

#### • ¿Dónde utilizamos tuplas?
Utilizamos tuplas para almacenar información sensible que no debe modificarse durante la ejecución:
1. **En el perfil del cliente:** la función `validar_datos_usuario()` empaqueta y retorna una tupla inmutable `(dni, email, telefono)`.
2. **En el carrito de compras:** cada vez que el usuario selecciona comprar algo, el ítem se agrega a la lista del carrito como una tupla `(id, marca, modelo, cantidad, precio_unitario, subtotal)`, asegurando la inmutabilidad de la información contable.
3. **Al momento del pago:** usamos una tupla de valores válidos para comparar opciones: `if cuotas in (1, 3):`.

#### • ¿Dónde utilizamos conjuntos (Sets)?
Creamos el conjunto `marcas_permitidas` compuesto por elementos únicos `{"Samsung", "Apple", "Motorola", "Xiaomi", "Nokia", "LG"}`. Lo implementamos en la función de Alta (`agregar_producto_nuevo`) para verificar instantáneamente si la marca introducida por el operador pertenece a nuestro conjunto de marcas soportadas, evitando el ingreso de marcas inválidas o repetidas.

#### • ¿Dónde utilizamos excepciones?
Aplicamos bloques `try/except` a lo largo de todo el código para evitar que el programa se cuelgue:
1. `ValueError`: Lo capturamos extensivamente al hacer inputs de menús, DNI, precios, cantidad de stock, etc. Evita que ingresar una letra en vez de un número rompa el programa.
2. `FileNotFoundError`: Al intentar cargar el JSON de stock inicial si no existe, o al buscar un archivo de historial de compras que el usuario nunca generó.
3. `FileExistsError`: Lo aplicamos en la creación de recibos. Intentamos crear el `recibo_DNI.txt` con el modo de escritura exclusiva (`"x"`). Si ya existe y dispara la excepción, el bloque except la captura y le añade un contador al nombre (ej. `recibo_DNI_1.txt`) automáticamente.
4. `JSONDecodeError`: Por si el archivo de base de datos se corrompe.

#### • ¿Dónde utilizamos archivos?
El sistema tiene doble persistencia en archivos físicos (disco duro):
1. `inventario.json`: Se lee con `json.load()` al abrir el programa y se sobreescribe con `json.dump()` cada vez que se hace un alta, baja, modificación o compra (para descontar el stock de forma permanente).
2. `recibo_DNI.txt`: Cada vez que se finaliza un "checkout", se genera y escribe en disco un ticket físico `.txt` con el resumen de la compra. Luego, la función `ver_compras()` lee físicamente el disco duro en busca de estos archivos para parsearlos y mostrarle al usuario su Historial.

#### • ¿Dónde realizamos pruebas unitarias?
Al final del código, importamos el módulo `unittest` y creamos la clase `PruebasSistema(unittest.TestCase)`.
Implementamos pruebas lógicas automatizadas que asertan cálculos cruciales para el negocio: probamos mediante funciones (`test_descuento_efectivo` y `test_recargo_tarjeta`) que el descuento del 15% por pago en efectivo y el recargo del 10% por pagar en 6 cuotas con tarjeta arrojen exactamente el número esperado. Estas pruebas se pueden ejecutar desde el sub-menú de Administración (Opción 11).

---
**Integrantes del grupo:**
- Aguilera, Camila 
- Lurie, Ezequiel
- Moret, Lucas
- Ozbetich Murano, Franco
- Diaz Azuni, Ignacio
