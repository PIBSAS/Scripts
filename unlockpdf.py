"""Requiere instalar qpdf en el sistema donde corra
   qpdf web: https://qpdf.sourceforge.io/
"""

import os

def rewrite_pdf(input_pdf):
    """
    Reescribe la estructura del PDF para corregir posibles problemas.
    Sobrescribe el archivo original.
    """
    command = f'qpdf --replace-input "{input_pdf}" --'
    os.system(command)
    print(f"🔧 PDF reescrito (posible reparación): {input_pdf}")

def remove_pdf_restrictions(input_pdf):
    """
    Elimina restricciones de un PDF sobrescribiendo el archivo original.
    """
    command = f'qpdf --replace-input --decrypt "{input_pdf}"'
    os.system(command)
    print(f"✅ Restricciones eliminadas (sobrescrito): {input_pdf}")

# Obtener la carpeta donde se ejecuta el script
folder = os.getcwd()

# Buscar todos los archivos PDF en la carpeta actual
pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("⚠️ No se encontraron archivos PDF en la carpeta actual.")
else:
    print(f"📂 Archivos encontrados: {len(pdf_files)} PDFs")

    # Reparar y luego desbloquear cada PDF encontrado
    for pdf in pdf_files:
        input_pdf = os.path.join(folder, pdf)
        rewrite_pdf(input_pdf)
        remove_pdf_restrictions(input_pdf)
