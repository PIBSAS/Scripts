"""
   Requiere instalar qpdf y Ghostscript en el sistema en el que se va a usar, ademas de instalarlo desde pip install ghostscript
   qpdf web: https://qpdf.sourceforge.io/
   Ghostscript web: https://www.ghostscript.com/
"""
import subprocess, sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "ghostscript"])


import os, ghostscript

def repair_pdf(input_pdf, output_pdf):
    """
    Repara un PDF dañado usando qpdf.
    
    :param input_pdf: Ruta del PDF original.
    :param output_pdf: Ruta donde se guardará el PDF reparado.
    """
    command = f'qpdf --linearize "{input_pdf}" "{output_pdf}"'
    os.system(command)
    print(f"✅ PDF reparado: {output_pdf}")

def compress_pdf(input_pdf, output_pdf, quality="ebook"):
    """
    Comprime un PDF usando Ghostscript después de repararlo con qpdf.

    :param input_pdf: Ruta del PDF original (reparado).
    :param output_pdf: Ruta donde se guardará el PDF comprimido.
    :param quality: Nivel de compresión (screen, ebook, printer, prepress).
    """
    gs_args = [
        "ps2pdf",
        "-dNOPAUSE", "-dBATCH", "-dSAFER",
        "-sDEVICE=pdfwrite",
        f"-dPDFSETTINGS=/{quality}",
        "-dFastWebView=true",  # Acelera la compresión
        "-dDetectDuplicateImages=true",  # Elimina imágenes repetidas
        "-dSubsetFonts=true",
        "-dCompressFonts=true",
        "-dEmbedAllFonts=true",
        "-dColorImageDownsampleType=/Bicubic",
        "-dColorImageResolution=72",
        "-dJPEGQ=50",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]
    
    try:
        ghostscript.Ghostscript(*gs_args)
        print(f"✅ PDF comprimido: {output_pdf}")
    except Exception as e:
        print(f"❌ Error al comprimir {input_pdf}: {e}")

# Obtener la carpeta donde el usuario está ejecutando el script
folder = os.getcwd()

# Buscar todos los archivos PDF en la carpeta actual
pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("⚠️ No se encontraron archivos PDF en la carpeta actual.")
else:
    print(f"📂 Archivos encontrados: {len(pdf_files)} PDFs")

    # Reparar y luego comprimir cada PDF encontrado
    for pdf in pdf_files:
        input_pdf = os.path.join(folder, pdf)
        repaired_pdf = os.path.join(folder, pdf.replace(".pdf", "_repaired.pdf"))
        compressed_pdf = os.path.join(folder, pdf.replace(".pdf", "_comp.pdf"))

        # Reparar el PDF primero
        repair_pdf(input_pdf, repaired_pdf)

        # Luego comprimir el PDF reparado
        compress_pdf(repaired_pdf, compressed_pdf)

        # Opcional: Eliminar el PDF reparado si no quieres ocupar espacio extra
        os.remove(repaired_pdf)
