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
from PIL import Image, ExifTags  # pip install Pillow

# Ruta de la carpeta donde están las imágenes
carpeta_imagenes = "./"

# Obtener todas las imágenes de la carpeta, ordenadas alfabéticamente
imagenes = sorted([
    os.path.join(carpeta_imagenes, archivo)
    for archivo in os.listdir(carpeta_imagenes)
    if archivo.lower().endswith(('.png', '.jpg', '.jpeg'))
])

# Función para corregir la orientación según los metadatos EXIF
def corregir_orientacion(imagen):
    try:
        exif = imagen._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == "Orientation":
                    if value == 3:
                        return imagen.rotate(180, expand=True)
                    elif value == 6:
                        return imagen.rotate(270, expand=True)
                    elif value == 8:
                        return imagen.rotate(90, expand=True)
    except Exception as e:
        print(f"Error al procesar la orientación: {e}")
    return imagen

# Asegúrate de que hay imágenes en la carpeta
if not imagenes:
    print("No se encontraron imágenes en la carpeta.")
else:
    # Abrir las imágenes, corregir la orientación y convertirlas al modo RGB
    imagenes_procesadas = []
    for img_path in imagenes:
        with Image.open(img_path) as img:
            img = corregir_orientacion(img)
            img = img.convert("RGB")
            imagenes_procesadas.append(img)

    # Guardar las imágenes como un PDF
    imagenes_procesadas[0].save(
        "tarea_universidad.pdf",  # Nombre del archivo PDF
        save_all=True,            # Guardar todas las imágenes
        append_images=imagenes_procesadas[1:]  # Agregar el resto de imágenes
    )

    print(f"PDF generado con éxito con {len(imagenes)} páginas.")
