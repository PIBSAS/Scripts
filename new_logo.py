from PIL import Image, ImageDraw, ImageFont

def crear_logo_pdf(ruta_salida='logo.webp', tamaño=(256, 256)):
    fondo_rojo = (220, 20, 60)
    texto_blanco = (255, 255, 255)

    img = Image.new("RGB", tamaño, fondo_rojo)
    draw = ImageDraw.Draw(img)

    try:
        fuente = ImageFont.truetype("arialbd.ttf", size=int(tamaño[1] * 0.4))
    except:
        fuente = ImageFont.load_default()

    texto = "PDF"
    bbox = draw.textbbox((0, 0), texto, font=fuente)
    texto_ancho = bbox[2] - bbox[0]
    texto_alto = bbox[3] - bbox[1]
    posicion = ((tamaño[0] - texto_ancho) // 2, (tamaño[1] - texto_alto) // 2)

    draw.text(posicion, texto, fill=texto_blanco, font=fuente)

    img.save(ruta_salida, "WEBP")
    print(f"Logo PDF creado: {ruta_salida}")

def convertir_a_ico(entrada='logo.webp', salida='favicon.ico', tamaño=(64, 64)):
    img = Image.open(entrada).convert("RGBA")
    img = img.resize(tamaño, Image.LANCZOS)
    img.save(salida, format='ICO')
    print(f"Favicon creado: {salida}")

if __name__ == "__main__":
    crear_logo_pdf()
    convertir_a_ico()
