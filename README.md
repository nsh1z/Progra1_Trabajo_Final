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
## Temas aplicados en el código
Para este trabajo aplicamos los temas vistos en la cursada:
- Manejo de Excepciones (`try... except` para evitar que el programa se caiga si ponés una letra en vez de un número).
- Archivos y Persistencia (JSON para el stock y TXT para los recibos).
- Expresiones Regulares (Librería `re` para validar correos).
- Programación Funcional (`filter`, `map` y funciones `lambda` para buscar productos y aplicar descuentos).
---
**Integrantes del grupo:**
- Aguilera, Camila 
- Lurie, Ezequiel
- Moret, Lucas
- Ozbetich Murano, Franco
- Diaz Azuni, Ignacio
