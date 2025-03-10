# Scripts

- Crear PDF desde Fotos para digitalizar la carpeta. Requiere Entorno Virtual Python y Pillow. Poner en carpeta donde se encuentran las imagenes previamente numeradas.
- Crear PDF asegurandose que el dato exif no altere la orientación, siendo siempre vertical. Requiere Entorno Virtual Python y Pillow.  Poner en carpeta donde se encuentran las imagenes previamente numeradas.
- Obtener Primer Hoja de PDF en Imagen. Util Para caratulas. Requiere Entorno virtual Python y ```pip install PyMuPDF```. Poner en carpeta donde se encuentra el PDF o los PDF.

## UV Package Manager
- **Requiere:**
   - **Windows:** ``winget install uv -s winget``
   - **Linux:** ``curl -LsSf https://astral.sh/uv/install.sh | sh``

En Windows se agrega automáticamente al PATH pero se indica como agregarlo.
En Linux se debe agregar la variable de entorno,  se indica al realizar la instalación. 

### Pasos:
- Crear un  directorio para que albergue el proyecto y entorno:
- ``mkdir proyecto``
- ``cd proyecto``
- ``uv init``
- Copiammos el contenido de ``caratulaUnlockDelMetaUv.py`` a ``main.py`` o renombramos el archivo.
- Nos movemos a donde se encuentran nuestros pdfs.
- ``cd $HOME/Downloads/``
- Ejecutamos el script:
- ``uv run $HOME/proyecto/main.py``
- o
- ``uv run ../proyecto/main.py``
- Listo!
