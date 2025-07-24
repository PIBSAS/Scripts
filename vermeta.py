import fitz  # PyMuPDF
import os

# Pedir ruta al usuario
folder_path = input("Ingrese la ruta de la carpeta con los PDFs: ").strip()

if not os.path.isdir(folder_path):
    print("❌ La carpeta no existe.")
    exit()

pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("⚠ No se encontraron archivos PDF.")
    exit()

print(f"\n📄 Se encontraron {len(pdf_files)} archivos PDF.\n")

for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    print(f"🔍 Metadatos de: {pdf_file}")

    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        doc.close()

        if metadata:
            for key, value in metadata.items():
                print(f"   {key}: {value}")
        else:
            print("   (Sin metadatos visibles)")
    except Exception as e:
        print(f"   ❌ Error leyendo metadatos: {e}")

    print("-" * 40)

print("\n✅ Lectura finalizada.")
