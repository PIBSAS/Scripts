import fitz
import os
import shutil

# Pedir al usuario la ruta de la carpeta
folder_path = input("Ingrese la ruta de la carpeta con los PDFs: ").strip()

# Verificar si la carpeta existe
if not os.path.isdir(folder_path):
    print("\nError: La carpeta especificada no existe.")
    exit()

# Obtener la lista de archivos PDF en la carpeta
pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("\nNo se encontraron archivos PDF en la carpeta.")
    exit()

print(f"\nSe encontraron {len(pdf_files)} archivos PDF. Eliminando metadatos...\n")

for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)

    try:
        # Abrir el PDF
        pdf = fitz.open(pdf_path)

        # Eliminar todos los metadatos
        pdf.set_metadata({})

        # Guardar en un archivo temporal
        temp_path = pdf_path + ".tmp"
        pdf.save(temp_path)
        pdf.close()

        # Reemplazar el original con el archivo sin metadatos
        shutil.move(temp_path, pdf_path)

        print(f"✔ Metadatos eliminados: {pdf_file}")

    except Exception as e:
        print(f"✖ Error procesando {pdf_file}: {e}")

print("\nProceso finalizado.")
