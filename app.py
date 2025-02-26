import os
import subprocess
import sys
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

#subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# Directorio donde están los PDFs y las carátulas (png)
BASE_DIRECTORY = os.getcwd()  # Usamos el directorio actual

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(BASE_DIRECTORY, 'favicon.ico')

# Ruta para generar el HTML dinámicamente
@app.route('/')
def serve_index():
    # Obtener lista de archivos PDF en el directorio actual
    #pdf_files = [f for f in os.listdir(BASE_DIRECTORY) if f.endswith('.pdf')]
    pdf_files = sorted([f for f in os.listdir(BASE_DIRECTORY) if f.endswith('.pdf')])
    # Generar HTML dinámicamente
    html_content = generate_html(pdf_files)

    # Renderizar el HTML generado desde una cadena
    return render_template_string(html_content)

# Ruta para servir archivos PDF
@app.route('/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(BASE_DIRECTORY, filename)

# Ruta para servir las carátulas (PNG) de los PDFs
@app.route('/<filename>')
def serve_cover(filename):
    return send_from_directory(BASE_DIRECTORY, filename)

# Función para generar el HTML
def generate_html(pdf_files):
    pdf_list = ',\n            '.join([f'"{pdf}"' for pdf in pdf_files])  # Crear lista de PDFs en formato JavaScript

    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visor PDF</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
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
            width: 80%;
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
</head>
<body>
    <div id="logo">
        <img src="/logo.png" alt="Logo" style="max-width: 200px; height: auto;">
    </div>
    <div id="pdfs-container"></div>
    
    <script>
        const pdfFiles = [
            {pdf_list}
        ];

        const container = document.getElementById('pdfs-container');

        pdfFiles.forEach(pdfFile => {{
            const img = document.createElement('img');
            // Usamos la ruta correcta para las carátulas
            img.src = '/' + pdfFile.replace('.pdf', '.png');  // Ruta raíz para acceder directamente

            img.classList.add('pdf-thumbnail');

            // Al hacer clic en la carátula, se abrirá el PDF en el navegador
            img.onclick = function() {{
                window.open('/pdfs/' + pdfFile, '_blank');
            }};

            const div = document.createElement('div');
            div.appendChild(img);
            
            // Crear y añadir el subtitulo con el nombre del archivo PDF
            const subtitle = document.createElement('p');
            subtitle.classList.add('pdf-title');
            subtitle.textContent = pdfFile.replace('.pdf', ''); //Nopmbre sin la extensión
            div.appendChild(subtitle);
            
            container.appendChild(div);
        }});
    </script>
</body>
</html>
    """
    return html_content

if __name__ == '__main__':
    # Ejecutar Flask en el puerto 80
    app.run(debug=True, host='0.0.0.0', port=80)
