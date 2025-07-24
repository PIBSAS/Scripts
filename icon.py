from PIL import Image

def convertir_a_ico(entrada='logo.webp', salida='favicon.ico', tamaño=(64, 64)):
    img = Image.open(entrada).convert("RGBA")
    img = img.resize(tamaño, Image.LANCZOS)
    img.save(salida, format='ICO')
    print(f"✅ Favicon creado: {salida}")

if __name__ == "__main__":
    convertir_a_ico()
