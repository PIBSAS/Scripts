import fitz  # pip install PyMuPDF
import os
Materia='Java'
def extraer_caratulas(directorio, salida):
    """
    Extrae las carátulas (primera página) de todos los archivos PDF en un directorio.
    
    :param directorio: Ruta al directorio que contiene los PDFs.
    :param salida: Ruta al directorio donde se guardarán las carátulas.
    """
    if not os.path.exists(salida):
        os.makedirs(salida)

    for archivo in os.listdir(directorio):
        if archivo.lower().endswith('.pdf'):
            ruta_pdf = os.path.join(directorio, archivo)
            try:
                doc = fitz.open(ruta_pdf)
                pagina = doc[0]  # Primera página
                pix = pagina.get_pixmap()  # Renderiza la página como imagen
                nombre_salida = os.path.splitext(archivo)[0] + ".png"
                ruta_salida = os.path.join(salida, nombre_salida)
                pix.save(ruta_salida)  # Guarda la imagen como PNG
                print(f"Carátula extraída: {ruta_salida}")
                doc.close()
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

# Configuración
directorio_pdf = "./"  # Cambia por tu directorio con PDFs
directorio_salida = "./"  # Cambia por tu directorio de salida

extraer_caratulas(directorio_pdf, directorio_salida)
