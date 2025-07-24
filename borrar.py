import fitz
import os
import shutil

folder_path = input("Ingrese la ruta de la carpeta con los PDFs: ").strip()

if not os.path.isdir(folder_path):
    print("\nError: La carpeta especificada no existe.")
    exit()

pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("\nNo se encontraron archivos PDF en la carpeta.")
    exit()

print(f"\nSe encontraron {len(pdf_files)} archivos PDF. Eliminando metadatos...\n")

for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    file_title = os.path.splitext(pdf_file)[0]
    
    try:
        # Abrir el PDF
        pdf = fitz.open(pdf_path)

        # Establecer metadatos vacíos explícitos
        empty_metadata = {
            "title": file_title,
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "",
            "modDate": ""
        }
        pdf.set_metadata(empty_metadata)

        # Guardar como nuevo archivo sin metadatos
        temp_path = pdf_path + ".tmp"
        pdf.save(temp_path, garbage=4, deflate=True, clean=True)
        pdf.close()

        # Reemplazar archivo original
        shutil.move(temp_path, pdf_path)

        print(f"Metadatos eliminados: {pdf_file}")

    except Exception as e:
        print(f"Error procesando {pdf_file}: {e}")

print("\nProceso finalizado.")
