import os
import re

def renombrar_archivos_camelcase(directorio):
    """
    Renombra archivos siguiendo el orden específico:
    1. Separación CamelCase.
    2. Reemplazo "Mag Pi" por "MagPi".
    3. Reemplazo "Micro Python" por "MicroPython".
    4. Reemplazo guiones bajos por espacios.
    5. Agregar cero a números de dos dígitos.

    :param directorio: Ruta al directorio que contiene los archivos.
    """
    for archivo in os.listdir(directorio):
        if archivo.endswith('.pdf'):
            ruta_archivo = os.path.join(directorio, archivo)
            nombre_base, extension = os.path.splitext(archivo)

            # 1. Separación CamelCase
            nombre_base = re.sub(r'(?<=[a-z])(?=[A-Z0-9])', ' ', nombre_base)

            # 2. Reemplazo "Mag Pi" por "MagPi"
            nombre_base = nombre_base.replace("Mag Pi", "MagPi")

            # 3. Reemplazo "Micro Python" por "MicroPython"
            nombre_base = nombre_base.replace("Micro Python", "MicroPython")

            # 4. Reemplazo guiones bajos por espacios
            nombre_base = nombre_base.replace("_", " ")

            # 5. Agregar cero a números de dos dígitos
            nombre_base = re.sub(r'(\D)(\d{2})$', r'\1 0\2', nombre_base)

            # Eliminar espacios dobles y espacios al inicio/final
            nombre_base = re.sub(r'\s+', ' ', nombre_base).strip()

            nombre_completo_nuevo = nombre_base + extension
            ruta_archivo_nuevo = os.path.join(directorio, nombre_completo_nuevo)

            # Mostrar los cambios antes y después
            if archivo != nombre_completo_nuevo:
                print(f"Antes: {archivo}")
                print(f"Después: {nombre_completo_nuevo}")
                os.rename(ruta_archivo, ruta_archivo_nuevo)
            else:
                print(f"No se requiere renombrar: {archivo}")

# Configuración
directorio = os.getcwd()  # Cambia esto si necesitas otro directorio

renombrar_archivos_camelcase(directorio)