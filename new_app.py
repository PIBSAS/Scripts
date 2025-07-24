import os
import subprocess
import sys
import socket
import webbrowser
from threading import Timer

# Directorio donde están los PDFs y las carátulas (png)
BASE_DIRECTORY = os.getcwd()  # Usamos el directorio actual
BASE_PATH = f'/{os.path.basename(BASE_DIRECTORY)}'

def is_dependencies_installed():
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", "PyMuPDF", "Pillow"])
        return True
    except subprocess.CalledProcessError:
        return False

if not is_dependencies_installed():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF", "Pillow"])

# Comprobar si Flask está instalado
def is_flask_installed():
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", "flask"])
        return True
    except subprocess.CalledProcessError:
        return False

# Instalar Flask solo si no está instalado
if not is_flask_installed():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

import fitz, shutil
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template_string, send_from_directory, jsonify, Response, send_file, make_response, request, url_for
import json
import mimetypes
mimetypes.add_type('image/webp', '.webp')

def crear_service_worker(static_folder='static', base_path='/', folder_web='Revistas'):
    ruta_sw = os.path.join(static_folder, 'service-worker.js')
    if os.path.exists(ruta_sw):
        print(f"Archivo service-worker.js ya existe en {ruta_sw}")
        return

    # Archivos esenciales siempre cacheados
    urls_to_cache = [
        f"{base_path}/",
        f"/static/logo.webp",
        f"/static/favicon.ico",
        f"/static/site.webmanifest",
        f"/static/service-worker.js",
    ]

    # Agregar PDFs y miniaturas (webp)
    for archivo in os.listdir():
        if archivo.endswith('.pdf') or archivo.endswith('.webp'):
            url = f"/{folder_web}/{archivo.replace(' ', '%20')}"
            urls_to_cache.append(url)

    # Armar el contenido del service worker
    contenido_sw = f"""
const CACHE_NAME = "revistas-cache-v1";
const urlsToCache = {urls_to_cache};

self.addEventListener("install", (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {{
      return cache.addAll(urlsToCache);
    }})
  );
}});

self.addEventListener("fetch", (event) => {{
  event.respondWith(
    caches.match(event.request).then((response) => {{
      return response || fetch(event.request).catch(() => {{
        return new Response("No hay conexión y el recurso no está en caché.", {{
          headers: {{ "Content-Type": "text/plain" }}
        }});
      }});
    }})
  );
}});
"""

    os.makedirs(static_folder, exist_ok=True)
    with open(ruta_sw, 'w', encoding='utf-8') as f:
        f.write(contenido_sw.strip())
    print(f"Archivo service-worker.js creado en {ruta_sw}")


def crear_site_manifest(static_folder='static', base_path='/'):
    ruta_manifest = os.path.join(static_folder, 'site.webmanifest')
    if not os.path.exists(ruta_manifest):
        contenido_manifest = {
            "name": "Mi Web App PDF",
            "short_name": "PDFApp",
            "start_url": base_path + "/",
            "display": "standalone",
            "background_color": "#dc143c",
            "theme_color": "#dc143c",
            "description": "Visualizador de PDFs con miniaturas",
            "icons": [
                {
                    "src": "/static/logo.webp",
                    "sizes": "256x256",
                    "type": "image/webp"
                },
                {
                    "src": "/static/favicon.ico",
                    "sizes": "64x64 32x32 24x24 16x16",
                    "type": "image/x-icon"
                }
            ]
        }
        with open(ruta_manifest, 'w', encoding='utf-8') as f:
            json.dump(contenido_manifest, f, indent=4)
        print(f"Archivo site.webmanifest creado en {ruta_manifest}")
    else:
        print(f"Archivo site.webmanifest ya existe en {ruta_manifest}")


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

STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)
crear_service_worker(STATIC_FOLDER, base_path=BASE_PATH, folder_web=BASE_PATH.strip('/'))
crear_site_manifest(STATIC_FOLDER, base_path=BASE_PATH)
logo_path = os.path.join(STATIC_FOLDER, 'logo.webp')
favicon_path = os.path.join(STATIC_FOLDER, 'favicon.ico')

if not os.path.exists(logo_path):
    crear_logo_pdf()
    shutil.move('logo.webp', logo_path)

def convertir_a_ico(entrada='logo.webp', salida='favicon.ico', tamaño=(64, 64)):
    img = Image.open(entrada).convert("RGBA")
    img = img.resize(tamaño, Image.LANCZOS)
    img.save(salida, format='ICO')
    print(f"Favicon creado: {salida}")

if not os.path.exists(favicon_path):
    convertir_a_ico(entrada=logo_path, salida='favicon.ico')
    shutil.move('favicon.ico', favicon_path)

def eliminar_metadatos(ruta_pdf, nombre_base):
    pdf = fitz.open(ruta_pdf)
    metadata_actual = pdf.metadata or {}
            
    empty_metadata = {
        "title": nombre_base,
        "author": "",
        "subject": "",
        "keywords": "",
        "creator": "",
        "producer": "",
        "creationDate": "",
        "modDate": ""
    }

    ya_limpio = all(
        metadata_actual.get(clave, "") in ("", nombre_base if clave == "title" else "")
        for clave in empty_metadata
    )

    if ya_limpio:
        print(f"Metadatos ya estaban limpios: {os.path.basename(ruta_pdf)}")
        pdf.close()
        return False
    else:
        pdf.set_metadata(empty_metadata)
        temp_path = ruta_pdf + ".tmp"
        pdf.save(temp_path, garbage=4, deflate=True, clean=True)
        pdf.close()

        os.remove(ruta_pdf)
        shutil.move(temp_path, ruta_pdf)
        print(f"Metadatos eliminados: {os.path.basename(ruta_pdf)}")
        return True

    
def extraer_caratulas_y_redimensionar(directorio, salida, ancho_deseado, alto_deseado):
    """
    Extrae las carátulas de los PDFs y las redimensiona a un tamaño fijo.
    
    :param directorio: Ruta al directorio con los PDFs.
    :param salida: Ruta al directorio de salida para las carátulas.
    :param ancho_deseado: Ancho deseado en píxeles.
    :param alto_deseado: Alto deseado en píxeles.
    """
    if not os.path.exists(salida):
        os.makedirs(salida)

    pdf_files= [f for f in os.listdir(directorio) if f.lower().endswith('.pdf')]
    print(f"\nSe encontraron {len(pdf_files)} archivos PDF. Eliminando metadatos solo si es necesario...\n")
    
    for archivo in pdf_files:
        ruta_pdf = os.path.join(directorio, archivo)
        base = os.path.splitext(archivo)[0]
        ruta_salida_webp = os.path.join(salida, base + '.webp')            
            
        try:
            eliminar_metadatos(ruta_pdf, base)
                
            # Si ya existe la carátula, se omite
            if not os.path.exists(ruta_salida_webp):
                print(f"Extrayendo carátula de {archivo}")
                doc = fitz.open(ruta_pdf)
                pagina = doc[0]
                pix = pagina.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                # Redimensionar la imagen usando Pillow
                #imagen_pil = Image.open(ruta_salida_png)
                imagen_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagen_redimensionada = imagen_pil.resize((ancho_deseado, alto_deseado), Image.LANCZOS)
                imagen_redimensionada.save(ruta_salida_webp, "WEBP", quality=80, lossless=True)
                doc.close()
                print(f"Carátula extraída y redimensionada: {base}.webp")
            else:
                print(f" Miniatura ya existe: {base}.webp (omitido)")
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

# Configurar directorio y dimensiones
directorio_pdf = "./"  # Cambia por tu directorio con PDFs
directorio_salida = "./"  # Cambia por tu directorio de salida
ancho_deseado = 332  # Ancho deseado en píxeles
alto_deseado = 443  # Alto deseado en píxeles

app = Flask(__name__)

FAVICON_PATH = os.path.join(os.path.dirname(__file__), 'favicon.ico')

"""@app.route('/favicon.ico')
def favicon():
    response = make_response(send_file(FAVICON_PATH, mimetype='image/vnd.microsoft.icon'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response 
"""
# Ruta para generar el HTML dinámicamente
@app.route(f'{BASE_PATH}/')
def serve_index():
    # Obtener lista de archivos PDF en el directorio actual
    pdf_files = sorted([f for f in os.listdir(BASE_DIRECTORY) if f.endswith('.pdf')])
    # Generar HTML dinámicamente
    html_content = generate_html(pdf_files, BASE_PATH)

    # Renderizar el HTML generado desde una cadena
    return render_template_string(html_content)

# Ruta para servir las carátulas (WEBP) de los PDFs
@app.route(f'{BASE_PATH}/<filename>')
def serve_cover(filename):
    return send_from_directory(BASE_DIRECTORY, filename)

@app.route('/static/site.webmanifest')
def serve_manifest():
    return send_file(os.path.join(STATIC_FOLDER, 'site.webmanifest'), mimetype='application/manifest+json')

@app.route('/static/service-worker.js')
def serve_sw():
    return send_from_directory(STATIC_FOLDER, 'service-worker.js', mimetype='application/javascript')

# Función para generar el HTML
def generate_html(pdf_files, base_path):
    pdf_list = ',\n            '.join([f'"{pdf}"' for pdf in pdf_files])  # Crear lista de PDFs en formato JavaScript
    folder_name = os.path.basename(os.getcwd())
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{folder_name}</title>
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="manifest" href="/static/site.webmanifest">
    <script src="/static/service-worker.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: brown;
        }}
        
        #logo {{
            margin: 20px 0;
            text-align: center;
        }}
        
        #pdfs-container {{
            background-color: orange;
            width: 100%;
            text-align: center;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            box-sizing: border-box;
            border: 2px solid #000000;
            margin: 0;
            padding: 0;
        }}
        
        .pdf-container {{
            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }}
        .pdf-thumbnail {{
            width: 332px;
            height: 443px;
            margin-top: 10px;
            box-sizing: border-box;
            object-fit: contain;
            cursor: pointer;
        }}
        
        .pdf-title {{
            text-align:center;
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }}
        
        @media (max-width: 768px) {{
            #pdfs-container {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
        
        @media (max-width: 480px) {{
            #pdfs-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    <script>
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', function() {{
        navigator.serviceWorker.register("/static/service-worker.js").then(function(registration) {{
          console.log('ServiceWorker registration successful with scope: ', registration.scope);
        }}, function(err) {{
          console.log('ServiceWorker registration failed: ', err);
        }});
      }});
    }}
  </script>
</head>
<body>
    <div id="logo">
        <img src="/static/logo.webp" alt={folder_name} style="max-width: 200px; height: auto;">
    </div>
    <div id="pdfs-container"></div>
    
    <script>
        const pdfFiles = [
            {pdf_list}
        ];

        const container = document.getElementById('pdfs-container');

        pdfFiles.forEach(pdfFile => {{
            const img = document.createElement('img');
            img.src = '{base_path}/' + pdfFile.replace('.pdf', '.webp');

            img.classList.add('pdf-thumbnail');
            
            const fileName = pdfFile.replace('.pdf', '');
            img.alt = 'Miniatura de ' + fileName;
            img.title = fileName;

            img.onclick = function() {{
                window.open('{base_path}/' + pdfFile, '_blank');
            }};

            const div = document.createElement('div');
            div.classList.add('pdf-container');
            div.appendChild(img);
            
            const subtitle = document.createElement('p');
            subtitle.classList.add('pdf-title');
            subtitle.textContent = pdfFile.replace('.pdf', '');
            div.appendChild(subtitle);
            
            container.appendChild(div);
        }});
    </script>
</body>
</html>
    """
    return html_content

def obtener_ip_local():
    # Obtener la IP local
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Conectar a una dirección externa para obtener la IP local
        s.connect(('10.254.254.254', 1))  # No importa la IP de destino
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # Fallback en caso de no poder obtenerla
    finally:
        s.close()
    return ip

def open_browser():
    ip_local = obtener_ip_local()
    url = f"http://{ip_local}{BASE_PATH}/"
    webbrowser.open_new(url)

if __name__ == '__main__':
    extraer_caratulas_y_redimensionar(directorio_pdf, directorio_salida, ancho_deseado, alto_deseado)
    Timer(1, open_browser).start()
    # Ejecutar Flask en el puerto 80
    app.run(debug=False, host='0.0.0.0', port=80, use_reloader=False)
