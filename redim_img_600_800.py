import os
import subprocess
import sys
from PIL import Image

def is_dependencies_installed():
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", "Pillow"])
        return True
    except subprocess.CalledProcessError:
        return False

if not is_dependencies_installed():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

def redimensionar_imagenes(directorio, salida, ancho_deseado=600, alto_deseado=800):
    """
    Redimensiona todas las imágenes de un directorio a un tamaño fijo,
    pero se salta las imágenes que ya tienen el tamaño correcto.
    
    :param directorio: Ruta al directorio con las imágenes.
    :param salida: Ruta al directorio de salida para las imágenes redimensionadas.
    :param ancho_deseado: Ancho deseado en píxeles.
    :param alto_deseado: Alto deseado en píxeles.
    """
    if not os.path.exists(salida):
        os.makedirs(salida)

    formatos_validos = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

    for archivo in os.listdir(directorio):
        if archivo.lower().endswith(formatos_validos):
            ruta_original = os.path.join(directorio, archivo)
            ruta_salida = os.path.join(salida, archivo)

            try:
                with Image.open(ruta_original) as img:
                    if archivo in {"logo.png", "favicon.ico"}:
                        print(f"Saltando {archivo}, está en la lista de exclusión.")
                        continue 
                    
                    if img.size == (ancho_deseado, alto_deseado):
                        print(f"Saltando {archivo}, ya tiene el tamaño correcto.")
                        continue  # Omite esta imagen

                    img_redimensionada = img.resize((ancho_deseado, alto_deseado), Image.LANCZOS)
                    img_redimensionada.save(ruta_salida)
                
                print(f"Imagen redimensionada: {ruta_salida}")

            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

# Configuración
directorio_imagenes = "./"  # Cambia por tu directorio con imágenes
directorio_salida = "./"  # Cambia por tu directorio de salida

redimensionar_imagenes(directorio_imagenes, directorio_salida)
