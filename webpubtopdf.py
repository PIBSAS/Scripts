import zipfile
import json
import os
import shutil
import glob

# Buscar todos los archivos .webpub en la carpeta
archivos_webpub = glob.glob("*.webpub")

if not archivos_webpub:
    print("❌ No se encontró ningún archivo .webpub")
    exit()

# Procesar cada archivo .webpub encontrado
for archivo_webpub in archivos_webpub:
    print(f"🔍 Procesando: {archivo_webpub}")

    # Extraer el nombre base del archivo (sin extensión)
    nombre_base = os.path.splitext(os.path.basename(archivo_webpub))[0]

    # Carpeta de extracción única por archivo
    carpeta_salida = f"extraido_{nombre_base}"
    os.makedirs(carpeta_salida, exist_ok=True)

    # Extraer el .webpub (ZIP)
    with zipfile.ZipFile(archivo_webpub, "r") as z:
        z.extractall(carpeta_salida)

    # Leer el manifest.json
    manifest_path = os.path.join(carpeta_salida, "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"❌ No se encontró manifest.json en {archivo_webpub}, saltando...")
        continue

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Obtener título del libro desde el manifest
    titulo_libro = manifest["metadata"].get("title", "").strip()

    # Si el título es genérico ("file") o vacío, usar el nombre base del archivo
    if not titulo_libro or titulo_libro.lower() == "file":
        titulo_libro = nombre_base

    # Limpiar nombre (evitar caracteres problemáticos)
    titulo_libro = titulo_libro.replace(" ", "_")

    # Obtener rutas del PDF y la carátula
    pdf_nombre = manifest["readingOrder"][0]["href"]
    cover_nombre = manifest["resources"][0]["href"]

    pdf_ruta = os.path.join(carpeta_salida, pdf_nombre)
    cover_ruta = os.path.join(carpeta_salida, cover_nombre)

    # Definir nombres con el título extraído o base
    nuevo_pdf = f"{titulo_libro}.pdf"
    nueva_caratula = f"{titulo_libro}.png"

    # Mover archivos con el nuevo nombre
    if os.path.exists(pdf_ruta):
        shutil.move(pdf_ruta, nuevo_pdf)
        print(f"✅ PDF extraído como '{nuevo_pdf}'")
    else:
        print(f"❌ No se encontró el PDF en {archivo_webpub}")

    if os.path.exists(cover_ruta):
        shutil.move(cover_ruta, nueva_caratula)
        print(f"✅ Carátula extraída como '{nueva_caratula}'")
    else:
        print(f"❌ No se encontró la carátula en {archivo_webpub}")

    # 🔴 Borrar carpeta de extracción una vez terminada la conversión
    shutil.rmtree(carpeta_salida)
    print(f"🗑️ Carpeta de extracción eliminada: {carpeta_salida}")

print("🎉 ¡Proceso completado! Todas las carpetas de extracción fueron eliminadas.")
