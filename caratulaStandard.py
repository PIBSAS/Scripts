import os
import subprocess
import sys

def is_dependencies_installed():
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", "PyMuPDF", "Pillow"])
        return True
    except subprocess.CalledProcessError:
        return False

if not is_dependencies_installed():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF", "Pillow"])

import fitz
from PIL import Image

def extraer_caratulas_y_redimensionar(directorio, salida, ancho_deseado, alto_deseado):
    """
    Extrae las carátulas de los PDFs y las redimensiona a un tamaño fijo.
    
    :param directorio: Ruta al directorio con los PDFs.
    :param salida: Ruta al directorio de salida para las carátulas.
    :param ancho_deseado: Ancho deseado en píxeles.
    :param alto_deseado: Alto deseado en píxeles.
    """
    if not os.path.exists(salida):
        os.makedirs(salida)

    for archivo in os.listdir(directorio):
        if archivo.lower().endswith('.pdf'):
            ruta_pdf = os.path.join(directorio, archivo)
            try:
                doc = fitz.open(ruta_pdf)
                pagina = doc[0]  # Primera página
                pix = pagina.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # Aumenta la resolución
                nombre_salida = os.path.splitext(archivo)[0] + ".png"
                ruta_salida = os.path.join(salida, nombre_salida)
                pix.save(ruta_salida)  # Guarda la imagen como PNG
                
                # Redimensionar la imagen usando Pillow
                imagen_pil = Image.open(ruta_salida)
                imagen_redimensionada = imagen_pil.resize((ancho_deseado, alto_deseado), Image.LANCZOS)
                imagen_redimensionada.save(ruta_salida)
                
                print(f"Carátula extraída y redimensionada: {ruta_salida}")
                doc.close()
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

# Configuración
directorio_pdf = "./"  # Cambia por tu directorio con PDFs
directorio_salida = "./"  # Cambia por tu directorio de salida
ancho_deseado = 600  # Ancho deseado en píxeles
alto_deseado = 800  # Alto deseado en píxeles

extraer_caratulas_y_redimensionar(directorio_pdf, directorio_salida, ancho_deseado, alto_deseado)