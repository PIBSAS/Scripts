import os
import sys
import shutil
import subprocess
import time

total_start = time.perf_counter()
# Con uv:
def is_dependencies_installed():
    try:
        start = time.perf_counter()
        subprocess.check_output(["uv", "pip", "show", "PyMuPDF", "Pillow"])
        end = time.perf_counter()
        print(f"🔍 Verificación de dependencias tomó {end - start:.4f} segundos")
        return True
    except subprocess.CalledProcessError:
        return False

if not is_dependencies_installed():
    start = time.perf_counter()
    subprocess.check_call(["uv", "add", "PyMuPDF", "Pillow"])
    end = time.perf_counter()
    print(f"📦 Instalación de dependencias tomó {end - start:.4f} segundos")

import fitz
from PIL import Image

# 📂 Obtener la carpeta actual donde se ejecuta el script
folder_path = os.getcwd()

# 🔍 Buscar archivos PDF en la carpeta actual
pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("⚠️ No se encontraron archivos PDF en la carpeta actual.")
    sys.exit()

print(f"\n📂 Se encontraron {len(pdf_files)} archivos PDF. Procesando...\n")


# 🔧 Función para reescribir la estructura del PDF (posible reparación)
def rewrite_pdf(input_pdf):
    command = f'qpdf --replace-input "{input_pdf}" --'
    os.system(command)
    print(f"🔧 PDF reescrito: {input_pdf}")


# 🔓 Función para eliminar restricciones del PDF
def remove_pdf_restrictions(input_pdf):
    command = f'qpdf --replace-input --decrypt "{input_pdf}"'
    os.system(command)
    print(f"✅ Restricciones eliminadas: {input_pdf}")


# 🛑 Función para eliminar metadatos del PDF
def remove_metadata(input_pdf):
    try:
        pdf = fitz.open(input_pdf)
        pdf.set_metadata({})  # Eliminar metadatos

        temp_path = input_pdf + ".tmp"
        pdf.save(temp_path)
        pdf.close()

        shutil.move(temp_path, input_pdf)
        print(f"🗑️ Metadatos eliminados: {input_pdf}")

    except Exception as e:
        print(f"❌ Error eliminando metadatos en {input_pdf}: {e}")


# 🖼️ Función para extraer y redimensionar la carátula del PDF
def extraer_caratulas_y_redimensionar(pdf_path, ancho_deseado, alto_deseado):
    """
    Extrae las carátulas de los PDFs y las redimensiona a un tamaño fijo.
    
    :param directorio: Ruta al directorio con los PDFs.
    :param ancho_deseado: Ancho deseado en píxeles.
    :param alto_deseado: Alto deseado en píxeles.
    """
    try:
        # Medir el tiempo para esta tarea
        inicio = time.time()

        doc = fitz.open(pdf_path)
        pagina = doc[0]  # Primera página
        pix = pagina.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # Aumenta la resolución
        nombre_salida = os.path.splitext(os.path.basename(pdf_path))[0] + ".png"
        ruta_salida = os.path.join(os.path.dirname(pdf_path), nombre_salida)  # Guardar en el mismo directorio

        pix.save(ruta_salida)  # Guarda la imagen como PNG

        # Redimensionar la imagen usando Pillow
        imagen_pil = Image.open(ruta_salida)
        imagen_redimensionada = imagen_pil.resize((ancho_deseado, alto_deseado), Image.LANCZOS)
        imagen_redimensionada.save(ruta_salida)

        # Tiempo de la tarea
        fin = time.time()
        print(f"🖼 Carátula extraída y redimensionada: {ruta_salida} en {fin - inicio:.2f} segundos")
                                
        doc.close()
    except Exception as e:
        print(f"❌ Error procesando {archivo}: {e}")

# Configuración
ancho_deseado = 600  # Ancho deseado en píxeles
alto_deseado = 800  # Alto deseado en píxeles

# 🚀 Procesar cada PDF encontrado
for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)

    rewrite_pdf(pdf_path)  # Reparar PDF
    remove_pdf_restrictions(pdf_path)  # Eliminar restricciones
    remove_metadata(pdf_path)  # Eliminar metadatos
    extraer_caratulas_y_redimensionar(pdf_path, ancho_deseado, alto_deseado)

print("\n✅ ¡Proceso completado! Todos los PDFs han sido procesados.")
total_end = time.perf_counter()
print(f"⏱️ Tiempo total de ejecución: {total_end - total_start:.4f} segundos")
