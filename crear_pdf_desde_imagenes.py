import os, subprocess, sys

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

# Ruta de la carpeta donde están las imágenes
carpeta_imagenes = "./"

# Obtener todas las imágenes de la carpeta, ordenadas alfabéticamente
imagenes = sorted([
    os.path.join(carpeta_imagenes, archivo)
    for archivo in os.listdir(carpeta_imagenes)
    if archivo.lower().endswith(('.png', '.jpg', '.jpeg'))
])

# Asegúrate de que hay imágenes en la carpeta
if not imagenes:
    print("No se encontraron imágenes en la carpeta.")
else:
    # Abrir las imágenes y convertirlas al modo RGB
    imagenes_procesadas = [Image.open(img).convert("RGB") for img in imagenes]

    # Guardar las imágenes como un PDF
    imagenes_procesadas[0].save(
        "tarea_universidad.pdf",  # Nombre del archivo PDF
        save_all=True,            # Guardar todas las imágenes
        append_images=imagenes_procesadas[1:]  # Agregar el resto de imágenes
    )

    print(f"PDF generado con éxito con {len(imagenes)} páginas.")
