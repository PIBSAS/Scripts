import os
import subprocess
import sys
import socket
import webbrowser
from threading import Timer

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

import fitz
from PIL import Image
from flask import Flask, render_template_string, send_from_directory, jsonify, Response, send_file
import json
import mimetypes
mimetypes.add_type('image/webp', '.webp')

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

    for archivo in os.listdir(directorio):
        if archivo.lower().endswith('.pdf'):
            ruta_pdf = os.path.join(directorio, archivo)
            base = os.path.splitext(archivo)[0]
            ruta_salida_webp = os.path.join(salida, base + '.webp')            
            
            # Si ya existe la carátula, se omite
            if os.path.exists(ruta_salida_webp):
                print(f"Ya existe: {archivo}, se omite.")
                continue
            
            try:
                doc = fitz.open(ruta_pdf)
                pagina = doc[0]
                pix = pagina.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                
                # Redimensionar la imagen usando Pillow
                #imagen_pil = Image.open(ruta_salida_png)
                imagen_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagen_redimensionada = imagen_pil.resize((ancho_deseado, alto_deseado), Image.LANCZOS)
                imagen_redimensionada.save(ruta_salida_webp, "WEBP", quality=80, lossless=True)
                
                print(f"Carátula extraída y redimensionada: {base}.webp")
                doc.close()
                
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

# Configurar directorio y dimensiones
directorio_pdf = "./"  # Cambia por tu directorio con PDFs
directorio_salida = "./"  # Cambia por tu directorio de salida
ancho_deseado = 332  # Ancho deseado en píxeles
alto_deseado = 443  # Alto deseado en píxeles

app = Flask(__name__)

# Directorio donde están los PDFs y las carátulas (png)
BASE_DIRECTORY = os.getcwd()  # Usamos el directorio actual
BASE_PATH = f'/{os.path.basename(BASE_DIRECTORY)}'

@app.route(f'{BASE_PATH}/favicon.ico')
def favicon():
    return send_from_directory(BASE_DIRECTORY, 'favicon.ico')

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

@app.route(f'{BASE_PATH}/site.webmanifest')
def serve_manifest():
    return send_file(os.path.join(BASE_DIRECTORY, 'site.webmanifest'), mimetype='application/manifest+json')

@app.route(f'{BASE_PATH}/service-worker.js')
def serve_sw():
    return send_from_directory(BASE_DIRECTORY, 'service-worker.js', mimetype='application/javascript')

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
    <link rel="icon" type="image/x-icon" href="{base_path}/favicon.ico">
    <link rel="manifest" href="{base_path}/site.webmanifest">
    <script src="{base_path}/service-worker.js"></script>
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
        navigator.serviceWorker.register("{base_path}/service-worker.js").then(function(registration) {{
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
        <img src="{base_path}/logo.webp" alt="Logo" style="max-width: 200px; height: auto;">
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