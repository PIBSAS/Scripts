import fitz
import shutil

# Pedir al usuario el nombre del archivo PDF
filename = input("Ingrese el nombre del archivo PDF (sin necesidad de escribir .pdf): ").strip()

# Agregar la extensión si el usuario no la incluyó
if not filename.lower().endswith(".pdf"):
    filename += ".pdf"

try:
    # Abrir el archivo PDF
    pdf = fitz.open(filename)

    # Mostrar metadatos actuales
    metadata = pdf.metadata
    print("\nMetadatos actuales:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Preguntar si quiere modificar los metadatos
    modificar = input("\n¿Desea modificar los metadatos? (s/n): ").strip().lower()

    if modificar == "s":
        # Pedir nuevos valores al usuario
        nuevo_titulo = input("Nuevo título (dejar vacío para no cambiar): ")
        nuevo_autor = input("Nuevo autor (dejar vacío para no cambiar): ")
        nuevo_asunto = input("Nuevo asunto (dejar vacío para no cambiar): ")
        nuevas_palabras_clave = input("Nuevas palabras clave (separadas por comas, dejar vacío para no cambiar): ")
        nuevo_creador = input("Nuevo creador (dejar vacío para no cambiar): ")
        nuevo_productor = input("Nuevo productor (dejar vacío para no cambiar): ")

        # Crear un diccionario con los cambios
        new_metadata = {key: value for key, value in {
            "title": nuevo_titulo,
            "author": nuevo_autor,
            "subject": nuevo_asunto,
            "keywords": nuevas_palabras_clave,
            "creator": nuevo_creador,
            "producer": nuevo_productor
        }.items() if value}  # Solo incluir valores que no estén vacíos

        # Aplicar los cambios
        if new_metadata:
            pdf.set_metadata(new_metadata)

            # Guardar en un archivo temporal
            temp_filename = filename + ".tmp"
            pdf.save(temp_filename)
            pdf.close()

            # Reemplazar el archivo original con el modificado
            shutil.move(temp_filename, filename)

            print(f"\nMetadatos actualizados correctamente en '{filename}'.")
        else:
            print("\nNo se realizaron cambios en los metadatos.")
            pdf.close()

    else:
        pdf.close()

except Exception as e:
    print(f"\nError: No se pudo abrir el archivo. Verifique que el nombre es correcto.\n{e}")
